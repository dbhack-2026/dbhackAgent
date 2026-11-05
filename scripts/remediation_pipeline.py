"""Local-only finding ingestion and remediation stage gates."""
import argparse
import hashlib
import json
import re
from pathlib import Path

STAGES = ("INGESTED", "CLASSIFIED", "CONTEXT_READY", "REMEDIATED", "CROSS_VALIDATED", "TECHNICALLY_VALIDATED", "HUMAN_APPROVED", "PR_CREATED", "CI_VALIDATED", "DEPLOYED", "LEARNING_CAPTURED")
STATUS = ("PENDING", "PASSED", "FAILED", "BLOCKED", "MANUAL", "PENDING_EXTERNAL")


def ingest(markdown):
    headings = list(re.finditer(r"^#{2,6} +(.+)$", markdown, re.M))
    findings = []
    for i, match in enumerate(headings):
        ids = re.findall(r"[A-Z][A-Z0-9]+-[0-9]+", match.group(1))
        if not ids:
            continue
        end = headings[i + 1].start() if i + 1 < len(headings) else len(markdown)
        evidence = markdown[match.end():end].strip()
        findings.append({"id": ids[0], "source_ids": sorted(set(ids)),
                         "title": match.group(1), "evidence": evidence,
                         "sha256": hashlib.sha256((match.group(1) + "\n" + evidence).encode()).hexdigest(),
                         "source": "audit/vulnerabilities.md", "classification": "UNREVIEWED", "status": "PENDING"})
    return findings


def consolidate(findings):
    by_id = {}
    for finding in findings:
        key = finding["id"]
        if key not in by_id:
            by_id[key] = dict(finding, source_hashes=[finding["sha256"]])
        elif finding["sha256"] not in by_id[key]["source_hashes"]:
            by_id[key]["source_hashes"].append(finding["sha256"])
            by_id[key]["evidence"] += "\n---\n" + finding["evidence"]
            by_id[key]["classification"] = "REVIEW_CONFLICT"
    return list(by_id.values())


def initial_state(findings):
    return {"schema_version": 1, "findings": {f["id"]: {"stage": "INGESTED", "status": "PASSED", "attempts": 0, "evidence": [f["source"]], "history": []} for f in findings}}


def advance(state, issue_id, stage, status, evidence, approval=False):
    if issue_id not in state["findings"] or stage not in STAGES or status not in STATUS:
        raise ValueError("Unknown issue, stage or status")
    entry = state["findings"][issue_id]
    previous = STAGES.index(entry["stage"])
    target = STAGES.index(stage)
    if target > previous + 1:
        raise ValueError("Cannot skip stages")
    if target > previous and entry["status"] != "PASSED":
        raise ValueError("Previous stage has not passed")
    if stage in ("HUMAN_APPROVED", "PR_CREATED", "DEPLOYED") and not approval:
        raise ValueError("Explicit human approval required")
    if status == "PASSED" and stage in ("CROSS_VALIDATED", "TECHNICALLY_VALIDATED", "CI_VALIDATED", "PR_CREATED") and not evidence:
        raise ValueError("Evidence required")
    if status == "FAILED":
        entry["attempts"] += 1
    entry.update(stage=stage, status=status, evidence=evidence)
    entry["history"].append({"stage": stage, "status": status, "evidence": evidence})
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="audit/vulnerabilities.md")
    parser.add_argument("--output", default=".agent-state")
    args = parser.parse_args()
    findings = consolidate(ingest(Path(args.input).read_text(encoding="utf-8")))
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    state_path = output / "remediation-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else initial_state(findings)
    for finding in findings:
        state["findings"].setdefault(finding["id"], initial_state([finding])["findings"][finding["id"]])
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"Prepared {len(findings)} finding(s). No external actions performed.")


if __name__ == "__main__":
    main()
