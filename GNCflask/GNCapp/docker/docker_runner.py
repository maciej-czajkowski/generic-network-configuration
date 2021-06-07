# How to:
# Build docker image by running command below in the dir with Dockerfile
# docker build -t gnc .
#
# We run docker every time with the following command that will be generate by script and run in a subprocess
#
# docker run --rm -v $(pwd)/input.txt:/input.txt -v $(pwd)/config.py:/project/gennetconf/config.py -v $(pwd)/out/:/project/out/ gnc 
# --input input.txt --input-format cisco --output-format juniper
#
# config.py - configuration file, input.txt - input file
# the parsed configuration will be placed in /out folder

import argparse
import os
import subprocess

def deserializeCLI(args):
   if args.input is None or args.input_format is None or args.output_format is None:
      return None

   map = {}
   map['input'] = args.input
   map['config'] = args.config
   map['in_format'] = args.input_format
   map['out_format'] = args.output_format
   return map

def parseCLI():
   parser = argparse.ArgumentParser(description="parse configuration")
   parser.add_argument('-c', '--config', help='config.py file path')
   parser.add_argument('-i', '--input', help='input file path')
   parser.add_argument('-if', '--input-format', choices=['json', 'juniper', 'cisco'], help='format of input file')
   parser.add_argument('-of', '--output-format', choices=['json', 'juniper', 'cisco'], help='format of output file')
   args = parser.parse_args()
   return deserializeCLI(args)


if __name__ == "__main__":
   args = parseCLI()

   dir_path = os.path.dirname(os.path.realpath(__file__))

   CMD = ["docker",
          "run", 
          "--rm", 
          "-v", dir_path + "/" + args["input"] + ":/input.txt",
          "-v", dir_path + "/" + args["config"] + ":/project/gennetconf/config.py",
          "-v", dir_path + "/out/:/project/out/",
          "gnc",
          "--input", "input.txt",
          "--input-format", args["in_format"],
          "--output-format", args["out_format"]]

   print("Calling subprocess with CMD =", CMD)

   returnCode = subprocess.run(CMD).returncode

   print("Return: ", returnCode)

   exit(returnCode)
