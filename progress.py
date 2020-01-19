import time, sys

for i in range(100):
    print(i, end="\r", flush=True)
    time.sleep(1)