import requests

resp = requests.get(
    "http://localhost:8050/",
    headers={"Referer": "https://fondosoldichom.com/"}
)
print(resp.status_code)    # should print 403
print(resp.headers.get("X-Frame-Options"))
print(resp.headers.get("Content-Security-Policy"))
