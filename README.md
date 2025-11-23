Flask DDoS Protection Project

app.py
-Implements a Flask app with a secure route /secure.
-Adds rate limiting to prevent too many requests from the same IP.
-Logs IP addresses and timestamps of requests.
-Uses HTTP Basic Authentication to protect the secure route.

load_test.py
-A script to simulate multiple requests to the Flask app.
-Useful for testing rate limiting.
-Do not use for real attacks, only for local testing.

How to Run
Start the Flask app: bash python3 app.py
To test, use http://127.0.0.1:5000/secure to go to the secure route
To test the rate limiter bash python load_test.py
