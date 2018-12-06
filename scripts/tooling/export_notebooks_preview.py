#!/usr/bin/env python3
import os
import os.path

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
NOTEBOOKS_DIR = THIS_DIR + "/../examples/notebooks"

def find_notebooks():
  result = [f for f in os.listdir(NOTEBOOKS_DIR) if f.endswith(".ipynb")]
  return result

print(find_notebooks())
