# Audit findings

## SAGA-24142 — Malformed transaction files trigger unbounded retries

**Repository:** daas-trade-brs-producer

**Evidence:** KafkaCustomConfig configures `DefaultAfterRollbackProcessor` with `FixedBackOff(60000, FixedBackOff.UNLIMITED_ATTEMPTS)`. Some deterministic parsing failures (e.g., missing TRANSACTIONS element, malformed dates) may not be classified as non-retryable, potentially blocking partition progress.

**Expected remediation:** Verify the behavior in source, classify deterministic errors correctly, preserve retries for transient failures, review dead-letter/recovery behavior and add regression tests. Do not assume a DLT is already configured.

**Acceptance criteria:** Invalid date and missing TRANSACTIONS cases have a tested, non-infinite recovery outcome; transient errors retain intended retry behavior.
