import click
import os
from shared.util import remove_md_images

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output_dir', default=None, type=click.Path(), help='Directory to save the converted markdown files.')
def remove_md_images_command(input_path, output_dir):
    if output_dir is None: 
        output_dir = input_path if os.path.isdir(input_path) else os.path.dirname(input_path)

    click.echo(f"Removing images from markdown files in '{input_path}'...")
    remove_md_images(input_path, output_dir)
    click.echo(f"Removed images from markdown files in '{input_path}' to '{output_dir}'.")

if __name__ == "__main__":
    remove_md_images_command()