#!/usr/bin/python3

# additions_query_generator.py
# Date:  29/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

import click

from dqgen.services.queries_generator import generate_from_csv


@click.command()
@click.argument("file_name")
def generate_queries(file_name):
    generate_from_csv(file_name)


if __name__ == '__main__':
    generate_queries()
