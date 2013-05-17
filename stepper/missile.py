'''
Missile generator
'''
from itertools import cycle


class HttpAmmo(object):
    def __init__(self, uri, headers, method='GET', http_ver='1.1'):
        self.method = method
        self.uri = uri
        self.proto = 'HTTP/%s' % http_ver
        self.headers = headers
        self.body = []

    def to_s(self):
        return "%s %s %s\n%s" % (self.method, self.uri, self.proto, '\n'.join(self.headers))


class SimpleGenerator(object):
    '''Generates ammo based on given sample'''
    def __init__(self, missile_sample):
        self.missiles = cycle([(missile_sample.to_s(), None)])

    def __iter__(self):
        return self.missiles


class UriStyleGenerator(object):
    '''Generates GET ammo based on given URI list'''
    def __init__(self, uris, headers, http_ver='1.1'):
        self.missiles = cycle([(HttpAmmo(uri, headers, http_ver).to_s(), None) for uri in uris])

    def __iter__(self):
        return self.missiles


class AmmoFileReader(object):
    '''Read missiles from ammo file'''
    def __init__(self, filename, loop_limit=0):
        self.filename = filename
        self.loops = 0
        self.loop_limit = loop_limit

    def __iter__(self):
        with open(self.filename, 'rb') as ammo_file:
            chunk_header = ammo_file.readline()
            while chunk_header:
                fields = chunk_header.split()
                chunk_size = int(fields[0])
                marker = fields[1] if len(fields) > 1 else None
                yield (ammo_file.read(chunk_size), marker)
                chunk_header = self.ammo_file.readline()
                if not chunk_header and (self.loops < self.loop_limit or self.loop_limit == 0):
                    self.loops += 1
                    ammo_file.seek(0)
                    chunk_header = ammo_file.readline()
