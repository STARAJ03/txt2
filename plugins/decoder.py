# plugins/decoder.py
import base64

def decode(encoded_url: str) -> str:
    try:
        # Base64 decode
        decoded_bytes = base64.b64decode(encoded_url)
        decoded_url = decoded_bytes.decode("utf-8")
        return decoded_url
    except Exception as e:
        print(f"[ERROR] Failed to decode URL: {e}")
        return encoded_url  # fallback: return as-is
