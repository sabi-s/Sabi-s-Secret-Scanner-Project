import re
import sys
import os


# ==================================================
# Known Secret Patterns
# ==================================================

SECRET_PATTERNS = {
    "OpenAI API Key": r"sk-[A-Za-z0-9]{20,}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"ghp_[A-Za-z0-9]{20,}",
    "Generic API Key": r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
    "Password": r'password\s*=\s*["\'][^"\']+["\']',
}


# ==================================================
# Educational Explanations
# ==================================================

EXPLANATIONS = {
    "OpenAI API Key":
        "This key allows access to OpenAI services and could generate costs if exposed.",

    "AWS Access Key":
        "AWS credentials may provide access to cloud resources and infrastructure.",

    "GitHub Token":
        "GitHub tokens can grant repository access and code modification permissions.",

    "Generic API Key":
        "Hardcoded API keys can be exposed through source control systems.",

    "Password":
        "Hardcoded passwords are one of the most common security vulnerabilities."
}


# ==================================================
# Mask Secrets Before Displaying
# ==================================================

def mask_secret(secret):
    if len(secret) <= 8:
        return "*" * len(secret)

    return (
        secret[:4]
        + "*" * (len(secret) - 8)
        + secret[-4:]
    )


# ==================================================
# Heuristic Detection
# ==================================================

def detect_possible_secret(line):

    findings = []

    strings = re.findall(r'["\']([^"\']+)["\']', line)

    for value in strings:

        if len(value) < 20:
            continue

        has_letters = any(c.isalpha() for c in value)
        has_numbers = any(c.isdigit() for c in value)

        if has_letters and has_numbers:
            findings.append(value)

    return findings


# ==================================================
# File Scanner
# ==================================================

def scan_file(filename):

    findings = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):

        for secret_type, pattern in SECRET_PATTERNS.items():

            matches = re.findall(pattern, line)

            for match in matches:
                findings.append({
                    "type": secret_type,
                    "line": line_number,
                    "value": match,
                    "confidence": "High"
                })

        possible_secrets = detect_possible_secret(line)

        for secret in possible_secrets:
            findings.append({
                "type": "Possible Hardcoded Secret",
                "line": line_number,
                "value": secret,
                "confidence": "Medium"
            })

    return findings


# ==================================================
# Educational Section
# ==================================================

def print_security_lesson():

    print("\n" + "=" * 60)
    print("SECURITY LESSON")
    print("=" * 60)

    print("""
Why is hardcoding secrets dangerous?

BAD:
----------------------------------------
OPENAI_API_KEY = "my-secret-key"

Risks:
• Accidental GitHub commits
• Credential leaks
• Unauthorized API usage
• Financial loss
• Difficult secret rotation

GOOD:
----------------------------------------
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

Store secrets in:

.env

OPENAI_API_KEY=your-secret-key

The application reads the secret from the environment
instead of storing it directly in source code.
""")


# ==================================================
# Report Generator
# ==================================================

def print_report(findings):

    print("\n" + "=" * 60)
    print("SECRET GUARDIAN REPORT")
    print("=" * 60)

    if not findings:
        print("\n✅ No secrets detected.")
        print("\nExcellent! No obvious credentials were found.")
        return

    for idx, finding in enumerate(findings, start=1):

        print(f"\n[{idx}] Potential Secret Found")
        print("-" * 40)

        print(f"Type       : {finding['type']}")
        print(f"Line       : {finding['line']}")
        print(f"Confidence : {finding['confidence']}")
        print(f"Value      : {mask_secret(finding['value'])}")

        if finding["type"] in EXPLANATIONS:
            print("\nWhy this matters:")
            print(EXPLANATIONS[finding["type"]])

    print(f"\n⚠ Total Findings: {len(findings)}")

    print_security_lesson()


# ==================================================
# Main
# ==================================================

def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python secret_guardian.py <python_file>")
        return

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print("File not found.")
        return

    findings = scan_file(filename)

    print_report(findings)


if __name__ == "__main__":
    main()