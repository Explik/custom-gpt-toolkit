import click
import os
import re

from shared.util import get_markdown_workspaces

def remove_image_references(markdown_text):
    return re.sub(r'!\[.*?\]\(.*?\)', '', markdown_text)  

def remove_image_references_from_md_file(input_path: str, output_directory: str) -> None:
    destination = os.path.join(output_directory, os.path.basename(input_path))
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = remove_image_references(content)
    with open(destination, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_md_images_from_workspace(workspace, output_directory: str) -> None:
    """
    Removes all images from markdown files in the input directory and saves them to the output directory.
    """

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Delete all images from the markdown file
    markdown_file = workspace["markdown_file"]
    remove_image_references_from_md_file(markdown_file, output_directory)

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output_dir', default=None, type=click.Path(), help='Directory to save the converted markdown files.')
def remove_md_images_command(input_path, output_dir):
    if output_dir is None: 
        output_dir = input_path if os.path.isdir(input_path) else os.path.dirname(input_path)

    # Assert that the input path exists as a directory
    assert os.path.exists(input_path), f"Directory {input_path} does not exist."
    assert os.path.isdir(input_path), f"Path {input_path} is not a directory."

    # Get/process all markdown workspaces
    click.echo(f"Removing images from markdown files in '{input_path}'...")
    workspaces = get_markdown_workspaces(input_path) 
    for workspace in workspaces:
        click.echo(f"Processing markdown folder: {workspace['directory']}")
        remove_md_images_from_workspace(workspace, output_dir)
    if not workspaces: 
        click.echo(f"No markdown files found in '{input_path}'.")

    click.echo(f"Removed images from markdown files in '{input_path}' to '{output_dir}'.")

if __name__ == "__main__":
    remove_md_images_command()