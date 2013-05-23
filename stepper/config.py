from exceptions import StepperConfigurationError
from itertools import islice
import load_plan as lp
import missile


class ComponentFactory():
    def __init__(
        self,
        rps_schedule=None,
        http_ver='1.1',
        ammo_file=None,
        instances_schedule=None,
        loop_limit=0,
        ammo_limit=0,
        uris=None,
        headers=None,
        autocases=None,
    ):
        self.rps_schedule = rps_schedule
        self.http_ver = http_ver
        self.ammo_file = ammo_file
        self.instances_schedule = instances_schedule
        self.loop_limit = loop_limit
        self.ammo_limit = ammo_limit
        self.uris = uris
        self.headers = headers
        self.autocases = autocases

    def get_load_plan(self):
        """
        return load plan (timestamps generator)
        """
        if self.rps_schedule and self.instances_schedule:
            raise StepperConfigurationError('Both rps and instances schedules specified. You must specify only one of them')
        elif self.rps_schedule:
            return lp.create(self.rps_schedule)
        elif self.instances_schedule:
            raise NotImplementedError('We have no support for instances_schedule yet')
        else:
            raise StepperConfigurationError('Schedule is not specified')

    def get_ammo_generator(self):
        """
        return ammo generator
        """
        if self.uris and self.ammo_file:
            raise StepperConfigurationError('Both uris and ammo file specified. You must specify only one of them')
        else:
            if self.uris:
                gen = missile.UriStyleGenerator(self.uris, self.headers, loop_limit=self.loop_limit, http_ver=self.http_ver)
                return gen if not self.ammo_limit else islice(gen, self.ammo_limit)
            elif self.ammo_file:
                gen = missile.AmmoFileReader(self.ammo_file, loop_limit=self.loop_limit)
                return gen if not self.ammo_limit else islice(gen, self.ammo_limit)
            else:
                raise StepperConfigurationError('Ammo not found. Specify uris or ammo file')
