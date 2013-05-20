
import missile
import load_plan as lp
from itertools import izip, islice


class StepperConfigurationError(Exception):
    '''
    Raised when error in stepper configuration found.
    '''


class AmmoFactory(object):
    '''Link generators, filters and markers together'''
    def __init__(self, config):
        self.load_plan = lp.create(config.rps_schedule)
        if len(config.uris):
            self.missile_generator = missile.UriStyleGenerator(config.uris, config.headers)
        elif config.ammo_file:
            loop_limit = config.loop_limit or 0
            self.missile_generator = missile.AmmoFileReader(config.ammo_file, loop_limit)
        else:
            raise StepperConfigurationError('Neither URIs nor ammo file found')
        if config.ammo_limit:
            self.missile_generator = islice(self.missile_generator, config.ammo_limit)
        self.filter = lambda missile: True
        self.marker = lambda missile: "None"

    def __iter__(self):
        return ((timestamp, marker or self.marker(missile), missile) for timestamp, (missile, marker) in izip(self.load_plan, self.missile_generator))

    def __len__(self):
        #FIXME: what if we have limits set?
        return len(self.load_plan)

    def loop_count(self):
        return self.missile_generator.loop_count()
