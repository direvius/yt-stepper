import stepper.ammo as ammo
import stepper.format as f
import matplotlib.pyplot as plt
import numpy as np

class Config:
    def __init__(self):
        # per-shoot params
        self.rps_schedule = [
            #'const(5, 10)',
            'line(1, 5, 10)',
            #'step(100, 10, 10, 1m)',
        ]
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
#import itertools as itt

#load_plan = lp.create(Config().rps_schedule)
#data = [(k, len(list(g))) for k, g in itt.groupby(ts/1000000 for ts in load_plan)]
ts = list(lp.create(Config().rps_schedule))
#rps = [(ts[i], len(list(itt.takewhile(lambda x: x < ts[i] + 1000000, ts[i:])))) for i in xrange(0, len(ts))]
rps = []
delta = 0
while len(ts) > 1:
    while delta < len(ts) and (ts[0] + 1000000 > ts[delta]):
        delta += 1
    curr_ts = ts.pop(0)
    rps.append((curr_ts, delta))
    delta -= 1
data = np.array(rps)
fig = plt.figure()
qq = fig.add_subplot(111)
qq.grid(True)
qq.plot(np.divide(data[:, 0], 1000000), data[:, 1])
plt.xlabel("Time, s")
plt.ylabel("RPS")
plt.title("Load plan")
plt.show()
plt.savefig("load.png")
plt.close()
