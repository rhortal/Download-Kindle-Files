#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

if [ ! -d .venv ]; then
  python3 -m venv .venv;
  source .venv/bin/activate
  python3 -m pip install -r requirements.txt
fi

source .venv/bin/activate
print ("Running unit tests")
python3 -m unittest discover -s tests -v