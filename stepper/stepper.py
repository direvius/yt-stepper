
import missile
import load_plan as lp
from itertools import izip, islice
import format as fmt
from info import progress


class StepperConfigurationError(Exception):
    '''
    Raised when error in stepper configuration found.
    '''


class AmmoFactory(object):
    '''Link generators, filters and markers together'''
    def __init__(self, config):
        self.load_plan = lp.create(config.rps_schedule)
        self.ammo_limit = config.ammo_limit
        loop_limit = config.loop_limit or 0
        if len(config.uris):
            self.missile_generator = missile.UriStyleGenerator(config.uris, config.headers, loop_limit=loop_limit)
        elif config.ammo_file:
            self.missile_generator = missile.AmmoFileReader(config.ammo_file, loop_limit)
        else:
            raise StepperConfigurationError('Neither URIs nor ammo file found')
        if self.ammo_limit:
            self.missile_generator = islice(self.missile_generator, config.ammo_limit)
        self.filter = lambda missile: True
        self.marker = lambda missile: "None"

    def __iter__(self):
        return ((timestamp, marker or self.marker(missile), missile) for timestamp, (missile, marker) in izip(self.load_plan, self.missile_generator))

    def __len__(self):
        #FIXME: wrong ammo count when loop_limit is set
        lp_len = len(self.load_plan)
        if self.ammo_limit:
            return self.ammo_limit if self.ammo_limit < lp_len else lp_len
        else:
            return lp_len

    def loop_count(self):
        return self.missile_generator.loop_count()


class Stepper(object):
    def __init__(self, config):
        self.ammo = fmt.Stpd(progress(AmmoFactory(config), 'Ammo: '))

    def write(self, f):
        for missile in self.ammo:
            f.write(missile)
