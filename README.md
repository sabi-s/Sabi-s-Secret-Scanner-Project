# Secret Guardian 🔐

A beginner-friendly Python tool that scans source code for **hardcoded secrets** such as API keys, access tokens and passwords, and explains why each one is a security risk.

Built as part of my first-week work in the DAE 6-month program, covering Python, version control and cybersecurity basics.

## Why this matters

Hardcoding credentials in source code is one of the most common security mistakes. Once a secret is committed to Git and pushed to GitHub, it can be found by anyone, including bots that scan public repositories for leaked keys. That can lead to unauthorized access, data leaks and unexpected cloud bills.

## Features

- **Pattern-based detection (High confidence)** for:
  - OpenAI API keys (`sk-...`)
  - AWS access keys (`AKIA...`)
  - GitHub personal access tokens (`ghp_...`)
  - Generic API keys (`api_key = "..."`)
  - Hardcoded passwords (`password = "..."`)
- **Heuristic detection (Medium confidence)**: flags quoted strings that are 20+ characters long and mix letters and numbers, which are common traits of tokens and keys
- **Secret masking**: shows only the first and last 4 characters of a match (e.g. `sk-a****3456`), so the report doesn't leak the secret itself
- **Explanations**: says why each type of secret is dangerous
- **Built-in security lesson**: shows the bad and the good way to handle secrets (environment variables / `.env` files)

## Project structure

```
<module>/sabitha-1-week/Secrets-Finder/
├── secret_guardian.py      # The scanner
└── vulnerable_example.py   # A deliberately insecure file to test the scanner on
```

The same project was submitted for three program modules: `python_1`, `version_control_1` and `cybersecurity_basics_1`.

## Requirements

- Python 3.x
- No third-party packages needed (uses only `re`, `sys` and `os`)

## Usage

```bash
cd python_1/sabitha-1-week/Secrets-Finder
python secret_guardian.py vulnerable_example.py
```

### Sample output

```
============================================================
SECRET GUARDIAN REPORT
============================================================

[1] Potential Secret Found
----------------------------------------
Type       : OpenAI API Key
Line       : 14
Confidence : High
Value      : sk-a***************************3456

Why this matters:
This key allows access to OpenAI services and could generate costs if exposed.
...
⚠ Total Findings: 8
```

## About `vulnerable_example.py`

This file is **intentionally insecure** and exists only for testing. All credentials in it are **fake placeholders**. The AWS key is Amazon's official documentation example (`AKIAIOSFODNN7EXAMPLE`). No real secrets are stored in this repository.

## The right way to handle secrets

```python
# ❌ Bad
OPENAI_API_KEY = "sk-my-real-key"

# ✅ Good
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

Keep secrets in a `.env` file or your system environment, and add `.env` to `.gitignore` so it is never committed.

## Possible improvements

- Scan whole directories recursively, not just one file
- Add more patterns (Slack tokens, Stripe keys, private keys, JWTs)
- Use entropy scoring to reduce false positives
- Export reports as JSON for CI pipelines
- Run as a Git pre-commit hook to block secrets before they're committed

## Author

**Sabitha S Karanavar** ([@sabi-s](https://github.com/sabi-s))
