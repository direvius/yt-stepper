
import missile
import load_plan as lp
from itertools import izip


class StepperConfigurationError(Exception):
    '''
    Raised when error in stepper configuration found.
    '''


class Factory(object):
    '''Link generators, filters and markers together'''
    def __init__(self, config):

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

        self.load_plan = lp.create(self.rps_schedule)
        if len(self.uris):
            self.missile_generator = missile.UriStyleGenerator(self.uris, self.headers)
        elif self.ammo_file:
            self.missile_generator = missile.AmmoFileReader(self.ammo_file)
        else:
            raise StepperConfigurationError('Neither URIs nor ammo file found')
        self.filter = lambda missile: True
        self.marker = lambda missile: "None"

    def __iter__(self):
        return ((timestamp, marker or self.marker(missile), missile) for timestamp, (missile, marker) in izip(self.load_plan, self.missile_generator))
