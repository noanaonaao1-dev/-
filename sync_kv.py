import os
import json
import http.client

def sync_kv():
    token = os.environ.get('CLOUDFLARE_API_TOKEN')
    account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
    namespace_id = os.environ.get('CLOUDFLARE_KV_NAMESPACE_ID')

    if not all([token, account_id, namespace_id]):
        print("Missing Cloudflare credentials, skipping KV sync.")
        return

    with open('dist/metadata.json', 'r') as f:
        metadata = f.read()

    conn = http.client.HTTPSConnection("api.cloudflare.com")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Update 'metadata' key in KV
    conn.request("PUT", f"/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/metadata", metadata, headers)
    res = conn.getresponse()
    print(f"KV Sync Status: {res.status} {res.reason}")

if __name__ == '__main__':
    sync_kv()
