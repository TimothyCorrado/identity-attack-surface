from googleapiclient.discovery import build
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def extract_messages(service, query):
    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=100
    ).execute()

    messages = results.get('messages', [])
    data = []

    for msg in messages:
        m = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = m['payload']['headers']

        subject = next(
            h['value'] for h in headers if h['name'] == 'Subject'
        )

        sender = next(
            h['value'] for h in headers if h['name'] == 'From'
        )

        data.append({
            "subject": subject,
            "sender": sender
        })

    return data