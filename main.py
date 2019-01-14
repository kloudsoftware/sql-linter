#!/usr/bin/env python3

import sys
from sql_parser import parse_sql_statement
from php_parser import parse_php_for_mysql_statements

def print_error(fd, n, ident):
    s = "SQL LINTER ERROR: Unknown column / table name '%s' in '%s' on line %d" % (ident, fd, n)
    print(s)

def main():
    if len(sys.argv) != 3:
        print("Please supply filename and path to file with valid indetifiers")
        exit(1)
    valid = []
    
    vifd = sys.argv[2]
    with open(vifd, 'r') as fd:
        c = fd.read()
        valid = c.split('\n')

    fd = sys.argv[1]
    print("Checking '%s'..." % fd)
    statements = parse_php_for_mysql_statements(fd)

    has_error = False
    for lineNr, line in statements.items():
        for p in parse_sql_statement(line):
            if not p in valid:
                print_error(fd, lineNr, p)
                has_error = True

    if has_error:
        exit(1)
    else:
        print("No errors found!")

if __name__ == '__main__':
    main()
