#!/usr/bin/python3

# Date:  29/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import pathlib

import click

from dqgen.services.html_templates_generator import generate_html_templates_from_csv


@click.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_folder", type=click.Path(dir_okay=True, file_okay=False))
def generate_html_templates(file_path, output_folder):
    generate_html_templates_from_csv(pathlib.Path(file_path), pathlib.Path(output_folder))


if __name__ == '__main__':
    generate_html_templates()
