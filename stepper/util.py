'''
Utilities: parsers, converters, etc.
'''
import re


def parse_duration(duration):
    '''
    Parse duration string, such as '3h2m3s'
    '''
    _re_token = re.compile("(\d+)([dhms]?)")

    def parse_token(time, multiplier):
        multipliers = {
            'h': 3600,
            'm': 60,
            's': 1,
        }
        if multiplier:
            if multiplier in multipliers:
                return int(time) * multipliers[multiplier]
            else:
                raise RuntimeError('No such multiplier: %s', multiplier)
        else:
            return int(time)

    return sum(parse_token(*token) for token in _re_token.findall(duration))
