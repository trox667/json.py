import sys

WHITESPACES = [
    ' ',
    '\n',
    '\t'
]
RESERVED = [
    '"',
    ':',
    '[',
    ']',
    '{',
    '}',
    ','
]


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __repr__(self):
        return "Token('%s', %s)" % (self.type, self.value)


def lex(characters):
    tokens = []
    text = ''
    for char in characters:
        if char in WHITESPACES:
            continue
        elif char in RESERVED:
            if len(text) > 0:
                tokens.append(Token(text, 'TEXT'))
                text = ''
            tokens.append(Token(char, 'RESERVED'))
        else:
            text += char

    return tokens


def is_bool(token):
    if token.value == 'true':
        return True
    elif token.value == 'false':
        return False
    return None


def is_float(token):
    try:
        return True, float(token.value)
    except:
        return False, None


def is_int(token):
    try:
        return True, int(token.value)
    except:
        return False, None


def parse_bool(tokens):
    value = is_bool(tokens[0])
    return (value, 1) if value is not None else (None, 0)


def parse_number(tokens):
    result, value = is_float(tokens[0])
    if result:
        return value, 1
    else:
        result, value = is_int(tokens[0])
        return (value, 1) if result else (None, 0)


def parse_string(tokens):
    if len(tokens) < 3:
        return None, 0
    if tokens[0].value == '"' and tokens[1].type == 'TEXT' and tokens[2].value == '"':
        return tokens[1].value, 3
    else:
        return None, 0


def parse_value(tokens):
    result, pos = parse_bool(tokens)
    if result is not None:
        return result, pos

    result, pos = parse_number(tokens)
    if result is not None:
        return result, pos

    return parse_string(tokens)


def parse_array(tokens):
    pos = 0
    if not tokens[pos].value == '[':
        return None, pos

    pos = 1
    arr = []
    while pos < len(tokens):
        if tokens[pos].value == ']':
            return arr, pos+1
        elif tokens[pos].value == ',':
            pos += 1
            continue
        result, new_pos = parse_value(tokens[pos:])
        if result is not None:
            arr.append(result)
            pos += new_pos
        else:
            sys.exit(-1)
            pass

    return arr, pos


def parse_key(tokens):
    if tokens[3].value == ':':
        result, pos = parse_string(tokens)
        pos += 1
        return result, pos
    else:
        return None, 0


def parse_object(tokens):
    pos = 0
    if not tokens[pos].value == '{':
        return None, pos

    pos = 1
    obj = {}
    while pos < len(tokens):
        if tokens[pos].value == '}':
            return obj, pos + 1
            pass
        elif tokens[pos].value == ';':
            pos += 1
            continue
        key, new_pos = parse_key(tokens[pos:])
        if key:
            pos += new_pos
            value, new_pos = parse(tokens[pos:])
            if value is not None:
                obj[key] = value
                pos += new_pos
        else:
            sys.exit(-1)
            pass

    pass


def parse(tokens):
    pos = 0
    while pos < len(tokens):
        if tokens[pos].value == '{':
            result, new_pos = parse_object(tokens[pos:])
            pos += new_pos
            return result, pos
        elif tokens[pos].value == '[':
            result, new_pos = parse_array(tokens[pos:])
            pos += new_pos
            return result, pos
        elif tokens[pos].value == '"' or tokens[pos].type == 'TEXT':
            result, new_pos = parse_value(tokens[pos:])
            pos += new_pos
            return result, pos
        else:
            pos += 1
    return None, pos


if __name__ == '__main__':
    json_array = '''
    [
      "q", "w", "e", true, 123, 1e-2, false
    ]
    '''
    tokens = lex(json_array)
    print(parse(tokens))

    json_object = '''
    {
        "abc": "def";
        "bcd": "efg";
        "cde": ["c", "e", "d", 1, 1e-2];
        "edf": false
    }
    '''
    tokens = lex(json_object)
    print(parse(tokens))

    pass
