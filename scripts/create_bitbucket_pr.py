#!/usr/bin/env python3
"""Create a Bitbucket Data Center pull request after manual approval.

Required environment variables: BITBUCKET_URL, BITBUCKET_PROJECT,
BITBUCKET_REPO, BITBUCKET_TOKEN. Token must have the required permissions.
"""
import argparse
import os
import sys
from pathlib import Path
from urllib.parse import quote
import requests


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--title', required=True)
    p.add_argument('--description-file', required=True)
    p.add_argument('--from-branch', required=True)
    p.add_argument('--to-branch', required=True)
    args = p.parse_args()
    env = {k: os.environ.get(k) for k in ('BITBUCKET_URL', 'BITBUCKET_PROJECT', 'BITBUCKET_REPO', 'BITBUCKET_TOKEN')}
    missing = [k for k, v in env.items() if not v]
    if missing:
        sys.exit('Missing environment variables: ' + ', '.join(missing))
    description = Path(args.description_file).read_text(encoding='utf-8')
    base = env['BITBUCKET_URL'].rstrip('/')
    url = (f"{base}/rest/api/1.0/projects/{quote(env['BITBUCKET_PROJECT'], safe='')}"
           f"/repos/{quote(env['BITBUCKET_REPO'], safe='')}/pull-requests")
    payload = {'title': args.title, 'description': description, 'state': 'OPEN',
               'open': True, 'closed': False,
               'fromRef': {'id': 'refs/heads/' + args.from_branch},
               'toRef': {'id': 'refs/heads/' + args.to_branch}}
    response = requests.post(url, json=payload, timeout=30,
                             headers={'Authorization': 'Bearer ' + env['BITBUCKET_TOKEN'],
                                      'Accept': 'application/json'},
                             verify=True)
    response.raise_for_status()
    data = response.json()
    links = data.get('links', {}).get('self', [])
    print(links[0]['href'] if links else f"Created PR ID: {data.get('id')}")

if __name__ == '__main__':
    main()
