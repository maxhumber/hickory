import datetime
import time

stamp = datetime.datetime.now().strftime("%H:%M:%S")
time.sleep(5)

print(f"Foo - {stamp} + 5 seconds")
