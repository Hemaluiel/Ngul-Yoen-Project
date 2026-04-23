from parser.bob_parser import parse_bob
from parser.bnb_parser import parse_bnb
from parser.dk_parser import parse_dk
from parser.table_parser import parse_table

def route_parser(bank, file):

    if bank == "BOB":
        return parse_bob(file)

    elif bank == "BNB":
        return parse_bnb(file)

    elif bank == "DK":
        return parse_dk(file)

    else:
        return parse_table(file)