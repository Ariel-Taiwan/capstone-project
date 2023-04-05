import psutil
print(psutil.pids())
p = psutil.Process(2782686)
p.name()
p.status()  #程序狀態
p.create_time()
print("------------")
p.cpu_times()
#psutil.cpu_times()
