import requests
import threading

URL = "http://127.0.0.1:5000/secure"

def hit_secure():
    try:
        requests.get(URL, auth=("admin","1234"))
    except:
        pass

threads = []
num_requests = 200  

for _ in range(num_requests):
    t = threading.Thread(target=hit_secure)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Finished")
