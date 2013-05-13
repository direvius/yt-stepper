
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
        self.load_plan = lp.create(config.rps_schedule)
        if len(config.uris):
            self.missile_generator = missile.UriStyleGenerator(config.uris, config.headers)
        elif config.ammo_file:
            self.missile_generator = missile.AmmoFileReader(config.ammo_file)
        else:
            raise StepperConfigurationError('Neither URIs nor ammo file found')
        self.filter = lambda missile: True
        self.marker = lambda missile: "None"

    def __iter__(self):
        return ((timestamp, marker or self.marker(missile), missile) for timestamp, (missile, marker) in izip(self.load_plan, self.missile_generator))
