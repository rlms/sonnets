def is_symbol(string):
    return string.startswith("<") and string.endswith(">")

def is_literal(string):
    return string.startswith('"') and string.endswith('"')

def symbol_evaluations(symbol, symbol_dict):
    possibilities = parse_

def evaluate_expression(parsed_expression, symbol_dict):
    result = []
    for part in parsed_expression:
        if is_symbol(part):
            result.append(evaluate_symbol(symbol_dict[part], symbol_dict))
        elif is_literal(part):
            result.append(part[1:-1])

    return " ".join(result)


def parse_possible_expression(expression):
    parts = expression.split(" ")

def parse_line(line):
    symbol, expression = line.split("::=")
    symbol = symbol.strip()
    expression = expression.strip()
    possibile = expression.split("|")

def parse_grammar(string):
    lines = string.splitlines()

