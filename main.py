import functools
import string


class ParseResult:
    def __init__(self):
        self.is_ok = False
        self.value = ''

    def __repr__(self):
        return '%s (%s, %s)' % (self.__class__, self.is_ok, self.value)


class Success(ParseResult):
    def __init__(self, value):
        super().__init__()
        self.is_ok = True
        self.value = value


class Failure(ParseResult):
    def __init__(self, msg):
        super().__init__()
        self.is_ok = False
        self.value = msg


class Parser:
    def __init__(self, parser_func):
        self.parser_func = parser_func


def run(parser, input):
    return parser(input)


def combine(parser_a, parser_b):
    def inner(characters):
        result_a = run(parser_a, characters)
        if not result_a.is_ok:
            return result_a
        else:
            (value_a, remaining_a) = result_a.value
            result_b = run(parser_b, remaining_a)
            if not result_b.is_ok:
                return result_b
            else:
                (value_b, remaining_b) = result_b.value
                new_value = (value_a, value_b)
                return Success((new_value, remaining_b))

    return inner


def or_else(parser_a, parser_b):
    def inner(characters):
        result_a = run(parser_a, characters)
        if result_a.is_ok:
            return result_a
        else:
            return run(parser_b, characters)
        pass
    return inner


def choice(parsers):
    return functools.reduce(or_else, parsers)


def any_of(characters):
    return choice([parse_char(char) for char in characters])


def parse_char(char):
    def inner(characters):
        if not characters:
            return Failure('No more input')
        else:
            first = characters[0]
            if first is char:
                return Success((char, characters[1:]))
            else:
                return Failure('Expecting "%c". Got "%c"' % (char, first))

    return inner


if __name__ == '__main__':
    parse_lowercase = any_of(string.ascii_lowercase)
    parse_digit = any_of('0123456789')

    print(run(parse_lowercase, 'aBC'))
    print(run(parse_lowercase, 'ABC'))

    print(run(parse_digit, '1ABC'))
    print(run(parse_digit, '9ABC'))
    print(run(parse_digit, '|ABC'))
    pass
