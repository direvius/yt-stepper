from itertools import izip
import format as fmt
from info import progress
from config import ComponentFactory


class AmmoFactory(object):
    '''Link generators, filters and markers together'''
    def __init__(self, factory):
        self.factory = factory
        self.load_plan = factory.get_load_plan()
        self.ammo_generator = factory.get_ammo_generator()
        self.filter = lambda missile: True
        self.marker = factory.get_marker()

    def __iter__(self):
        return (
            (timestamp, marker or self.marker(missile), missile)
            for timestamp, (missile, marker)
            in izip(self.load_plan, self.ammo_generator)
        )

    def __len__(self):
        #FIXME: wrong ammo count when loop_limit is set
        lp_len = len(self.load_plan)
        ammo_len = len(self.ammo_generator)
        return min(lp_len, ammo_len) or max(lp_len, ammo_len)

    def loop_count(self):
        return self.ammo_generator.loop_count()


class Stepper(object):
    def __init__(self, **kwargs):
        self.ammo = fmt.Stpd(progress(AmmoFactory(ComponentFactory(**kwargs)), 'Ammo: '))

    def write(self, f):
        for missile in self.ammo:
            f.write(missile)
