#!/usr/bin/env python3
# small_lint_sample.py

import os, sys     # Multiple imports on one line (usually flagged)

def add(x,y):      # Missing space after comma
    result=x+y     # Missing spaces around operator
    return result  

# Unused variable
unused = "This will be flagged"

# Line too long
very_long_string = "This string is intentionally long to trigger line length warnings in most Python linters like flake8"