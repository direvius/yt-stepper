'''
Missile generator
'''
from itertools import cycle


class HttpAmmo(object):
    def __init__(self, uri, headers, method='GET'):
        self.method = method
        self.uri = uri
        self.proto = "HTTP/1.1"
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
    def __init__(self, uris, headers):
        self.missiles = cycle([(HttpAmmo(uri, headers).to_s(), None) for uri in uris])

    def __iter__(self):
        return self.missiles


class AmmoFileReader(object):
    '''Read missiles from ammo file'''
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, 'rb') as ammo_file:
            chunk_header = ammo_file.readline()
            while chunk_header:
                fields = chunk_header.split()
                chunk_size = int(fields[0])
                marker = fields[1] if len(fields) > 1 else None
                yield (ammo_file.read(chunk_size), marker)
                chunk_header = self.ammo_file.readline()
