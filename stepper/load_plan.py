'''
Load Plan generators
'''
import math
import re
from util import parse_duration


class Const(object):
    '''Load plan with constant load'''
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


class Line(object):
    '''Load plan with linear load'''
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


class Composite(object):
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


class StepFactory(object):

    @staticmethod
    def line(params):
        template = re.compile('(\d+),\s*(\d+),\s*(\d+[dhms]?)+\)')
        minrps, maxrps, duration = template.search(params).groups()
        return Line(int(minrps), int(maxrps), parse_duration(duration))

    @staticmethod
    def const(params):
        template = re.compile('(\d+),\s*(\d+[dhms]?)+\)')
        rps, duration = template.search(params).groups()
        return Const(int(rps), parse_duration(duration))

    @staticmethod
    def produce(step_config):
        _plans = {
            'line': StepFactory.line,
            'const': StepFactory.const,
        }
        load_type, params = step_config.split('(')
        if load_type in _plans:
            return _plans[load_type](params)
        else:
            raise NotImplemented('No such load type implemented: %s', load_type)


def create(rps_schedule):
    '''Load Plan factory method'''
    if len(rps_schedule) > 1:
        return Composite([StepFactory.produce(step_config) for step_config in rps_schedule])
    else:
        return StepFactory.produce(rps_schedule[0])
