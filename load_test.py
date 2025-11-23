import requests
import threading

URL = "http://127.0.0.1:5000/secure"

def hit_secure():
    try:
        requests.get(URL)
    except:
        pass

threads = []
num_requests = 200  # try 500, 2000 later

for _ in range(num_requests):
    t = threading.Thread(target=hit_secure)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Finished")
