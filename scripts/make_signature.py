import hmac, hashlib, sys

secret = "test_secret"
path = sys.argv[1]

with open(path, "rb") as f:
    body = f.read()

sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
print(sig)