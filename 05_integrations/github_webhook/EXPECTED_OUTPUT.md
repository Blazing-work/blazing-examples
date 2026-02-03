# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Processing Pull Request webhook...
[GITHUB] Signature validated successfully
[SLACK] Notified: New PR 'Add new feature' by developer123

  Action: opened
  PR Title: Add new feature
  Processed: True

Processing Push webhook...
[GITHUB] Signature validated successfully
[PUSH] developer456 pushed 2 commit(s) to refs/heads/main

  Branch: refs/heads/main
  Commits: 2
  Processed: True
```

## Notes

- Demonstrates GitHub webhook processing with signature verification
- Uses HMAC SHA256 for signature validation (simulated with test secret)
- Processes two webhook types: pull_request and push
- In production, would integrate with actual Slack/notification services
- Simulated responses use pre-defined test payloads
