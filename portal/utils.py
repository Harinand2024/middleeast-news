# portal/utils/auth.py
import hmac, hashlib, time, json
from django.conf import settings
from django.core.cache import cache  # using Redis or DB cache

API_CREDENTIALS = {
    "hub-456": settings.HUB_SECRET_KEY,
}

def verify_signature(request):
    api_key = request.headers.get("X-API-KEY")
    timestamp = request.headers.get("X-TIMESTAMP")
    signature = request.headers.get("X-SIGNATURE")

    if not api_key or not timestamp or not signature:
        return False, "Missing authentication headers"

    if api_key not in API_CREDENTIALS:
        return False, "Invalid API key"

    secret_key = API_CREDENTIALS[api_key]

    try:
        timestamp = int(timestamp)
    except ValueError:
        return False, "Invalid timestamp"

    if abs(time.time() - timestamp) > 300:
        return False, "Timestamp expired"

    # ✅ calculate HMAC on raw bytes
    body_bytes = request.body or b""
    msg = f"{timestamp}.".encode() + body_bytes
    expected_sig = hmac.new(secret_key.encode(), msg, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
        return False, "Invalid signature"

    # ✅ prevent replay attacks
    req_id = hashlib.sha256(f"{api_key}:{msg}".encode()).hexdigest()
    if cache.get(req_id):
        return False, "Replay attack detected"
    cache.set(req_id, True, timeout=300)

    return True, None


def success_response(data, message = None):
    return {"status": True, "data":data, "message":message}

def error_response(message):
    return {"status": False, "message":message}

