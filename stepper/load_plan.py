'''
Load Plan generators
'''
import math
import re

MULTIPLIERS = {
    'h': 3600,
    'm': 60,
    's': 1,
}


def normalize_time(duration, multiplier):
    if multiplier:
        if multiplier in MULTIPLIERS:
            return int(duration) * MULTIPLIERS[multiplier]
        else:
            raise RuntimeError('No such multiplier: %s', multiplier)
    else:
        return int(duration)


class ConstLoadPlan(object):
    '''Load plan with constant load'''

    TEMPLATE = re.compile('(\d+),\s*(\d+)([dhms])')

    @staticmethod
    def create(config):
        rps, duration, multiplier = ConstLoadPlan.TEMPLATE.search(config).groups()
        return ConstLoadPlan(int(rps), normalize_time(duration, multiplier))

    def __init__(self, rps, duration):
        self.rps = rps
        self.duration = duration

    def __iter__(self):
        interval = 1000000 / self.rps
        return (i * interval for i in xrange(0, self.rps * self.duration))

    def rps_at(self, t):
        '''Return rps for second t'''
        if t <= self.duration:
            return self.rps
        else:
            return 0

    def duration(self):
        '''Return step duration'''
        self.duration


class LineLoadPlan(object):
    '''Load plan with linear load'''

    TEMPLATE = re.compile('(\d+),\s*(\d+),\s*(\d+)([dhms])')

    @staticmethod
    def create(config):
        minrps, maxrps, duration, multiplier = LineLoadPlan.TEMPLATE.search(config).groups()
        return LineLoadPlan(int(minrps), int(maxrps), normalize_time(duration, multiplier))

    def __init__(self, minrps, maxrps, duration):
        self.minrps = minrps
        self.maxrps = maxrps
        self.duration = duration

    def __iter__(self):
        k = float(self.maxrps - self.minrps) / self.duration
        b = 1 + 2 * self.minrps / k

        '''
        Solve equation:
        n(t) = k/2 * t^2 + (k/2 + r0) * t
        where r(t) = k(t + 1/2) + r0 -- rps
        r0 is initial rps.
        '''
        def timestamp(n):
            return int((math.sqrt(b * b + 8 * n / k) - b) * 500000)  # (sqrt(b^2 + 8 * n / k) - b) / 2 -- time in seconds

        ''' Find ammo number given the time '''
        def number(t):
            return int(k * (t ** 2) / 2 + (k / 2 + self.minrps) * self.duration)
        return (timestamp(n) for n in xrange(0, number(self.duration)))

    def rps_at(self, t):
        '''Return rps for second t'''
        if t <= self.duration:
            return self.minrps + float(self.maxrps - self.minrps) * t / self.duration
        else:
            return 0

    def duration(self):
        '''Return step duration'''
        self.duration


class CompositeLoadPlan(object):
    '''Load plan with multiple steps'''
    def __init__(self, steps):
        self.steps = steps

    def __iter__(self):
        base = 0
        for step in self.steps:
            for ts in step:
                yield ts + base
            base += step.duration * 1000000

    def duration(self):
        return sum(step.duration for step in self.steps)

PLANS = {
    'line': LineLoadPlan,
    'const': ConstLoadPlan,
}


def create_load_plan(config):
    load_type, params = config.split('(')
    if load_type in PLANS:
        return PLANS[load_type].create(params)
    else:
        raise NotImplemented('No such load type implemented: %s', load_type)


def create(rps_schedule):
    '''Load Plan factory method'''
    if len(rps_schedule) > 1:
        return CompositeLoadPlan([create_load_plan(config) for config in rps_schedule])
    else:
        return create_load_plan(rps_schedule[0])
