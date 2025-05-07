import click
import os
from shared.util import extract_md

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output_dir', default=None, type=click.Path(), help='Directory to save the converted markdown files.')
def extract_md_command(input_path, output_dir):
    if output_dir is None: 
        output_dir = input_path if os.path.isdir(input_path) else os.path.dirname(input_path)

    click.echo(f"Extracting markdown from '{input_path}'...")
    extract_md(input_path, output_dir)
    click.echo(f"Extracted markdown from '{input_path}' to '{output_dir}'.")