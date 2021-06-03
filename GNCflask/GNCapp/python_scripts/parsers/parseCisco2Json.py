
import argparse
import json
import ciscoConfigParser as ccp
import configurationTranslator as ct
 

# --- parsing input arguments
cli = argparse.ArgumentParser(description='Scripts parses CISCO configuration file.')
cli.add_argument("-p", "--path", nargs=1, required=True, help="path to CISCO configuration file")

# if __name__ == "__main__":

# -- getting filename
args = cli.parse_args()
filePath = args.path[0]

# --- creating config parser object
# --- it will parse the config into list of lists (every entry in the list is a list which containt every line between ! in config)
parser = ccp.ciscoConfigParser()
parser.parseConfig(filePath)

# --- uncomment to see the content of the parsed config
# print(parser.config)

# --- here we begin to translate the parsed config into a generic one
translator = ct.ciscoGenericTranslator()
# --- this class method will return Json dictionary base string
parsedData = ct.configurationTranslator().parseCisco2GenericJson(parser.config)

# print(parsedData)
# for line in parser.config:
#     for entry in line:
#         for key in translator.dictionary.keys():
#             if entry.startswith(key):
#                 parsedData[key] = entry.replace(key, "")

# --- we create a json string
genericJson = json.dumps(parsedData, indent=4)

outputFile = open("exampleOutput.json", 'w')
outputFile.write(genericJson)