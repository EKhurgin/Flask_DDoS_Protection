from flask import Flask, request, make_response
import time
import logging

ip_requests = {}

MAX_REQUESTS = 5
TIME_WINDOW = 10 #in seconds


app = Flask(__name__)


logging.basicConfig(
    filename='ip_requests.log',  
    level=logging.INFO,          
    format='%(asctime)s - %(message)s'  
)


def rate_limited(ip):
    now = time.time()
    if ip not in ip_requests:
        ip_requests[ip] = []

    ip_requests[ip] = [t for t in ip_requests[ip] if now - t < TIME_WINDOW]

    logging.info(f"IP: {ip}, requests in window: {len(ip_requests[ip]) +1}")


    if len(ip_requests[ip]) >= MAX_REQUESTS:
        return True
    ip_requests[ip].append(now)
    return False

@app.route("/secure")
def secure_area():
    ip = request.remote_addr
    if rate_limited(ip):
        return "Too many requests", 429

    auth = request.authorization
    if not auth or not (auth.username == "admin" and auth.password == "1234"):
        return make_response(
            "Login Required",
            401,
            {"WWW-Authenticate": 'Basic realm="Protected Area"'}
        )
    return "Welcome to the secure area!"

if __name__ == "__main__":
    app.run(debug=True)