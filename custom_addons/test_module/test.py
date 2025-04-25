#!/usr/bin/env python3

from __future__ import annotations


def add(x: float, y: float) -> int | float:
    """Add two numbers together.

    Args:
    ----
        x: First number to add
        y: Second number to add

    Returns:
    -------
        The sum of x and y

    """
    return x + y

# Unused variable
unused = "This will be flagged"

# Line too long
very_long_string = (
    "This string is intentionally long to trigger line length "
    "warnings in most Python linters like flake8"
)
