
import argparse
import json



# --- parsing input arguments
parser = argparse.ArgumentParser( description='Scripts parses CISCO configuration file.' )
parser.add_argument( "-p", "--path", nargs=1, required=True, help="path to CISCO configuration file" )

# if __name__ == "__main__":
args = parser.parse_args()
filePath = args.path[0]

# --- opening file
file = open( filePath, "r" )

config = file.readlines()

print(config)

example_dict = {'name': "cisco", 'number': 2}

result = json.dumps(example_dict, indent=3)
print(result)

