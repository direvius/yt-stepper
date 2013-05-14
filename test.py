import stepper.ammo as ammo
import stepper.format as f
import matplotlib.pyplot as plt
import numpy as np

class Config:
    def __init__(self):
        # per-shoot params
        self.rps_schedule = ['line(1, 10, 5m)', 'step(0,5,1,3m)']
        self.http_ver = '1.0'
        self.ammo_file = None
        self.instances_schedule = ''
        self.loop_limit = None
        self.ammo_limit = None
        self.uris = ['/', '/list']
        self.headers = ['Host: www.yandex.ru']
        self.autocases = 0
        self.use_caching = True
        self.force_stepping = None

#for missile in (f.Stpd(ammo.Factory(Config()))):
#    print missile

import stepper.load_plan as lp
import itertools as itt

load_plan = lp.create(Config().rps_schedule)
data = [(k, len(list(g))) for k, g in itt.groupby(ts/1000000 for ts in load_plan)]
data = np.array(data)
fig = plt.figure()
qq = fig.add_subplot(111)
qq.grid(True)
qq.plot(data[:, 0], data[:, 1])
plt.xlabel("Time, ms")
plt.ylabel("RPS")
plt.title("Load plan")
plt.show()
plt.savefig("load.png")
plt.close()
