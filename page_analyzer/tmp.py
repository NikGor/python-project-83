#!/usr/bin/env python3
import os


def print_var(var_name):
    DATABASE_URL = os.environ.get(var_name)
    print(DATABASE_URL)


if __name__ == '__main__':
    print_var('DATABASE_URL')
