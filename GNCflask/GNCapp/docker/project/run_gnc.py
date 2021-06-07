from anytree import RenderTree
import json as js
import argparse
import nanolog as nl
import sys
from gennetconf.parsers import CiscoConfigParser, JuniperConfigParser
from gennetconf.config import Config
from gennetconf.generators import CiscoConfigGenerator, JuniperConfigGenerator 
import gennetconf.errors as err
from gennetconf.mainlog import initLogger, logger


def deserializeCLI(args):
    if args.input is None or args.input_format is None or args.output_format is None:
        return None

    map = {}
    map['config'] = args.input
    map['in_format'] = args.input_format
    map['out_format'] = args.output_format
    return map

def parseCLI():
    parser = argparse.ArgumentParser(description="parse configuration")
    # parser.add_argument('-c', '--config', action='store_const', help='config file path')
    parser.add_argument('-i', '--input', help='input file path')
    parser.add_argument('-if', '--input-format', choices=['json', 'juniper', 'cisco'], help='format of input file')
    parser.add_argument('-of', '--output-format', choices=['json', 'juniper', 'cisco'], help='format of output file')
    args = parser.parse_args()
    return deserializeCLI(args)


if __name__ == "__main__":
    initLogger()

    args = parseCLI()
    if args is None:
        logger.critical1("Error: Invalid args provided. See run_gnc help for more information.")
        sys.exit(err.CLI_ARGS_ERROR)

    print(args['config'])
    if args['in_format'] == 'cisco':
        config = CiscoConfigParser(args['config']).parse()
        transformer = Config(tree=config)
        transformer.parse_tree()
    elif args['in_format'] == 'juniper':
        config = JuniperConfigParser(args['config']).parse()
        transformer = Config(tree=config)
        transformer.parse_tree()
    elif args['in_format'] == 'json':
        json_file = open(args['config'], "r").read()
        print(json_file)
        config  = js.loads(json_file)
        transformer = Config(json=config)
        transformer.parse_json()
    else:
        logger.critical1("Error: Unexpected input format.")
        sys.exit(err.UNEXPECTED_IN_FORMAT)

    if args['out_format'] == 'json':
        result = transformer.get_json()
        output = open("project/out/output.txt", "w")
        output.write(result)
    elif args['out_format'] == 'cisco':
        root = transformer.get_tree()
        print(RenderTree(root).by_attr('name'))
        CiscoConfigGenerator(root).write_to_file("project/out/output.txt")
    elif args['out_format'] == 'juniper':
        root = transformer.get_tree()
        print(RenderTree(root).by_attr('name'))
        JuniperConfigGenerator(root).write_to_file("project/out/output.txt")
    else:
        logger.critical1("Error: Unexpected output format.")
        sys.exit(err.UNEXPECTED_OUT_FORMAT)

    
