from fastapi import Request, HTTPException
from time import time

requests_log = {}

def rate_limit(request: Request):
    ip = request.client.host
    now = time()

    if ip not in requests_log:
        requests_log[ip] = []

    requests_log[ip] = [t for t in requests_log[ip] if now - t < 60]

    if len(requests_log[ip]) > 60:
        raise HTTPException(status_code=429, detail="Too many requests")

    requests_log[ip].append(now)
