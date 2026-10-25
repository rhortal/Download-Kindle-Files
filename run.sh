#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

# Rebuild the venv if it is missing or broken (e.g. the system Python was
# upgraded and the packages no longer match the interpreter).
if [ ! -d .venv ] || ! .venv/bin/python3 -c "import requests, imap_tools, dotenv, bs4" &> /dev/null; then
  rm -rf .venv
  python3 -m venv .venv;
  source .venv/bin/activate
  python3 -m pip install -r requirements.txt
fi

source .venv/bin/activate
python3 main.py
