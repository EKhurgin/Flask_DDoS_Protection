from flask import Flask, request, make_response
import time
import logging
import threading

ip_requests = {}

MAX_REQUESTS = 5
TIME_WINDOW = 10 #in seconds

lock = threading.Lock()


app = Flask(__name__)


logging.basicConfig(
    filename='ip_requests.log',  
    level=logging.INFO,          
    format='%(asctime)s - %(message)s'  
)


def rate_limited(ip):
    now = time.time()
    with lock:
        if ip not in ip_requests:
            ip_requests[ip] = []

        ip_requests[ip] = [t for t in ip_requests[ip] if now - t < TIME_WINDOW]

        ip_requests[ip].append(now)

        count = len(ip_requests[ip])
    
        if count > MAX_REQUESTS:
            print(f"IP {ip} blocked! {count} requests in last {TIME_WINDOW} seconds")
            logging.info(f"IP: {ip} blocked! {count} requests in window")
        else:
            print(f"IP {ip} allowed: {count} requests in last {TIME_WINDOW} seconds")
            logging.info(f"IP: {ip}, requests in window: {count}")
        for handler in logging.getLogger().handlers:
            handler.flush()

        return count > MAX_REQUESTS



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