#!/usr/bin/python3

# Date:  29/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

import click

from dqgen.services.html_templates_generator import generate_html_templates_from_csv


@click.command()
@click.argument("file_name")
def generate_html_templates(file_name):
    generate_html_templates_from_csv(file_name)


if __name__ == '__main__':
    generate_html_templates()
