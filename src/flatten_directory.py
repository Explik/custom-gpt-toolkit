import click
import os

from shared.util import flatten_directory 

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output_dir', default=None, type=click.Path(), help='Directory to save the converted files.')
def flatten_files_command(input_path, output_dir):
    """
    Flattens the directory structure by copying all nested files to a single output directory.
    Each file is renamed to match its original path.
    """
    if output_dir is None: 
        output_dir = input_path if os.path.isdir(input_path) else os.path.dirname(input_path)

    click.echo(f"Flattening files from '{input_path}' to '{output_dir}'...")
    flatten_directory(input_path, output_dir)
    click.echo(f"Flattened files from '{input_path}' to '{output_dir}'.")

if __name__ == "__main__":
    flatten_files_command()