"""
A deliberately vulnerable application.

DO NOT USE IN PRODUCTION.
"""

import requests


# ==================================================
# Hardcoded Secrets
# ==================================================

OPENAI_API_KEY = "sk-abcdefghijklmnopqrstuvwxyz123456"

AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

GITHUB_TOKEN = "ghp_abcdefghijklmnopqrstuvwxyz123456"

password = "SuperSecretAdminPassword"

SESSION_TOKEN = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4"


# ==================================================
# Fake Services
# ==================================================

def fetch_ai_response(prompt):

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    print("Calling OpenAI...")
    print(headers)

    return {
        "response": "Hello from AI"
    }


def upload_to_cloud():

    print("Uploading file to AWS")

    print("Using access key:")
    print(AWS_ACCESS_KEY)


def push_code():

    print("Connecting to GitHub")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    print(headers)


def login(username, user_password):

    if user_password == password:
        return True

    return False


# ==================================================
# Application Entry Point
# ==================================================

def main():

    user = "admin"

    if login(user, "SuperSecretAdminPassword"):
        print("Login Successful")

    fetch_ai_response("hello")

    upload_to_cloud()

    push_code()


if __name__ == "__main__":
    main()