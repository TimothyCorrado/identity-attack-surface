import os
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.gmail_scanner import extract_messages

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def build_gmail_service() -> object:
    """
    Uses an OAuth token file mounted into the container.
    token.json is created once on your host via Google OAuth flow.
    """
    token_path = os.getenv("GMAIL_TOKEN_PATH", "/secrets/token.json")
    if not os.path.exists(token_path):
        raise FileNotFoundError(
            f"Missing {token_path}. Mount your token.json into the container."
        )

    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    return build("gmail", "v1", credentials=creds)

def run_scan(service: object) -> None:
    queries = [
        "subject:welcome",
        "subject:verify",
        "subject:receipt",
        "subject:\"password reset\"",
        "subject:\"security alert\"",
        "unsubscribe",
    ]

    exposures = []
    for q in queries:
        exposures.extend(extract_messages(service, q))

    os.makedirs("/app/output", exist_ok=True)
    df = pd.DataFrame(exposures).drop_duplicates()
    df.to_csv("/app/output/exposures.csv", index=False)
    print(f"Scan complete. Rows: {len(df)}. Wrote /app/output/exposures.csv")

if __name__ == "__main__":
    print("Start scan")
    svc = build_gmail_service()
    run_scan(svc)