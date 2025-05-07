import click
import os
from shared.util import convert_to_md

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output_dir', default=None, type=click.Path(), help='Directory to save the converted markdown files.')
def convert_to_md_command(input_path, output_dir):
    if output_dir is None: 
        output_dir = input_path

    click.echo(f"Converting '{input_path}' to markdown files...")
    convert_to_md(input_path, output_dir)
    click.echo(f"Converted '{input_path}' to markdown files in '{output_dir}'.")

if __name__ == "__main__":
    convert_to_md_command()
