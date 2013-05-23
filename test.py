import stepper.stepper as stepper
import matplotlib.pyplot as plt
import numpy as np
from stepper.info import progress
from stepper.config import ComponentFactory

#TODO: instances_schedule
# ammo without timestamp

#TODO: descending linear load

#TODO: error messages

#TODO: logging

#TODO: stepper results

#TODO: fractional load
# use float for parameters


cft = ComponentFactory(
    rps_schedule=[
        'const(10, 2m)',
        #'line(1, 5000, 10m)',
        #'step(100, 10, 10, 1m)',
    ],
    http_ver='1.0',
    ammo_file='ammo',
    instances_schedule='',
    loop_limit=None,
    ammo_limit=None,
    uris=[
        #'/',
        #'/list',
    ],
    headers=['Host: www.yandex.ru'],
    autocases='uniq',
)


def test_lp():
    ts = list(progress(cft.get_load_plan()))
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
    stepper.Stepper(cft).write(f)
