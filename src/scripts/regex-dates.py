import re
from datetime import datetime
import numpy as np

FILE1 = "8pod-30ps-logs.log"
FILE2 = "8pod-30ps-k8s-logs.log"

time_format = "%H:%M:%S.%f"

with open(FILE1) as f:
    lines = f.readlines()
    r = re.compile(r"\d{2}:\d{2}:\d{2}\.\d{6}")
    f1_filtered_list = sorted([r.search(line).group() 
                               for line in lines if r.search(line)])


with open(FILE2) as f:
    lines = f.readlines()[1::2]
    r = re.compile(r"\d{2}:\d{2}:\d{2}\.\d{6}")
    f2_filtered_list = sorted([r.search(line).group() 
                               for line in lines if r.search(line)])

output = []

for i in range(len(f1_filtered_list)):
    output.append((datetime.strptime(f2_filtered_list[i], time_format) - 
                   datetime.strptime(f1_filtered_list[i], time_format))
                   .total_seconds())

print(np.median(output))
print(np.max(output))

