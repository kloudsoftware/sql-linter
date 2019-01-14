import sqlparse
import re

ignored = [
        "Whitespace", 
        "Wildcard",
        "Newline",
        "DML",
        "Punctuation",
        "Comparison",
        "Number",
        "Assignment",
]


allowed_keywords = ["UID"]

def get_token_list(parsed):
    for p in parsed:
        for t in p.flatten():
            if t._get_repr_name() not in ignored and filter_token(t):
                yield t


def token_repr(token):
    return token.__str__()

def clean_token(token):
    ret = token
    if token.startswith("`"):
        ret = token[1:]

    if token.endswith("`"):
        ret = ret[0:-1]

    return ret

def filter_token(token):
    ts = token.__str__()

    if len(ts) == 1:
        return False

    if token.is_keyword and ts in allowed_keywords:
        return True
    elif token.is_keyword:
        return False

    if ts == "ASC" or ts == "DESC" or ts == "RAND":
        return False

    if ts.startswith("\'"):
        return False

    p = re.compile(r"\d")
    if p.match(ts) is not None:
        return False

    return True

def parse_sql_statement(sql_string):
    parsed = sqlparse.parse(sql_string)
    tokens = get_token_list(parsed)

    mapped = map(lambda t: token_repr(t), tokens)
    clean = map(lambda t: clean_token(t), mapped)
    return clean
