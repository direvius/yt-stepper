import stepper.stepper as stepper
import matplotlib.pyplot as plt
import numpy as np
from stepper.info import progress

#TODO: instances_schedule
# ammo without timestamp

#TODO: descending linear load

#TODO: error messages

#TODO: logging

#TODO: stepper results

#TODO: fractional load
# use float for parameters


class Config:
    def __init__(self):
        # per-shoot params
        self.rps_schedule = [
            #'const(5, 10)',
            'line(1, 5000, 10m)',
            #'step(100, 10, 10, 1m)',
        ]
        self.http_ver = '1.0'
        self.ammo_file = 'ammo'
        self.instances_schedule = ''
        self.loop_limit = None
        self.ammo_limit = None
        self.uris = [
            #'/',
            #'/list',
        ]
        self.headers = ['Host: www.yandex.ru']
        self.autocases = 0
        self.use_caching = True
        self.force_stepping = None


def test_lp():
    import stepper.load_plan as lp
    ts = list(progress(lp.create(Config().rps_schedule)))
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

with open('ammo.stpd', 'w') as f:
    stepper.Stepper(Config()).write(f)
