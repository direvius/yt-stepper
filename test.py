import stepper.ammo as ammo
import stepper.format as f


class Config:
    def __init__(self):
        # per-shoot params
        self.rps_schedule = ['const(1,3m)', 'line(1,10,2m)']
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

for missile in (f.Stpd(ammo.Factory(Config()))):
    print missile
