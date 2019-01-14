import re

sql_beginnings = [
  "CREATE",
  "ALTER",
  "DROP",
  "ALTER",
  "TABLE",
  "GRANT",
  "REVOKE",
  "ANALYZE",
  "AUDIT",
  "COMMENT",
  "DBMS_SQL",
  "ALTER",
  "ALTER",
  "ANALYZE",
  "ASSOCIATE",
  "STATISTICS",
  "AUDIT",
  "COMMENT",
  "CREATE",
  "CREATE",
  "DISASSOCIATE",
  "STATISTICS",
  "DROP",
  "DROP",
  "FLASHBACK",
  "FLASHBACK",
  "GRANT",
  "NOAUDIT",
  "PURGE",
  "RENAME",
  "REVOKE",
  "TRUNCATE",
  "CALL",
  "DELETE",
  "EXPLAIN PLAN",
  "INSERT",
  "LOCK TABLE",
  "MERGE",
  "SELECT",
  "UPDATE",
  "SELECT",
  "CALL",
  "EXPLAIN",
  "PLAN",
  "COMMIT",
  "ROLLBACK",
  "SAVEPOINT",
  "SET",
  "TRANSACTION",
  "COMMIT",
  "ROLLBACK",
  "ALTER SESSION",
  "SET ROLE",
  "ALTER",
  "SYSTEM"
] 

def _parse_inner(regex, line):
    m = regex.match(line)
    if m is not None:
        return m.group(1)
    return None

def _parse_for_mysql_calls(line):
    regex = re.compile(r".*mysql[i]?_query\(\"([a-zA-Z\n$\d\s\t%'*=_(),`{}<>.]*)[\",]")
    return _parse_inner(regex, line)

def _parse_for_sprintf(line):
    regex = re.compile(r".*sprintf\(\"([a-zA-Z\n$\d\s\t%'*=_(),`{}<>.]*)[\",]")
    return _parse_inner(regex, line)

def _parse_for_variable_declaration(line):
    regex = re.compile(r".*\$.+\s=\s\"([a-zA-Z\n$\d\s\t%'*=_(),`{}<>.]*)[\",]")
    return _parse_inner(regex, line)

    
parser = [
    _parse_for_mysql_calls, 
    _parse_for_sprintf,
    _parse_for_variable_declaration
]

def _parse(line):
    for p in parser:
        m = p(line)
        if m is not None:
            return m
    return None

SEMICOLON = ";"
def parse_php_for_mysql_statements(fd):
    content = ""
    with open(fd, 'r') as f:
        content = f.read()
    lines = content.split('\n')

    found_raw = {}
    markedN = None
    markedLines = []
    for n, line in enumerate(lines, 1):
            if not markedN:
                for beginning in sql_beginnings:
                    if beginning in line:
                        if SEMICOLON in line:
                            found_raw[n] = line
                        else:
                            markedN = n
                            markedLines.append(line)
            elif SEMICOLON in line:
                found_raw[markedN] = ' '.join(markedLines)
                markedN = None
                markedLines = []
            elif not SEMICOLON in line:
                markedLines.append(line)
            else:
                raise ValueError('Unknown State! markedN: %d' % markedN)

    found = {}
    for n, line in found_raw.items():
        parsed = _parse(line)
        if parsed is not None:
            found[n] = parsed

    return found

