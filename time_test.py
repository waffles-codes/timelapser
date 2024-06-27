import time

print(time.strftime('%m-%d-%Y %H-%M-%S'))
ms = time.time_ns()


spf = 0
int_spf = int(spf)
for i in range(int_spf):
    # check exit condition; break
    print("subtracting 1 from counter")
    time.sleep(1)
remaining_time = spf - int_spf
print(remaining_time)
time.sleep(remaining_time)