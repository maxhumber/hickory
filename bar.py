import time
import datetime

time_stamp = datetime.datetime.now().strftime("%H:%M:%S")

time.sleep(5)

print(f"Bar - {time_stamp} + 5 seconds")
