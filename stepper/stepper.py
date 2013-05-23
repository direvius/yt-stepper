from itertools import izip
import format as fmt
from info import progress


class AmmoFactory(object):
    '''Link generators, filters and markers together'''
    def __init__(self, factory):
        self.load_plan = factory.get_load_plan()
        self.missile_generator = factory.get_ammo_generator()
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
