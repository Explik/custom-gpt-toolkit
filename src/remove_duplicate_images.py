import click
import os
import imagehash
from PIL import Image
from collections import defaultdict
from shared.util import get_markdown_workspaces

def find_near_duplicates(image_paths, hash_threshold=5):
    file_hashes = {}

    for image_path in image_paths:
        try:
            img = Image.open(image_path)
            img_hash = imagehash.phash(img)

            file_name = os.path.basename(image_path)
            file_hashes[file_name] = img_hash
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    # Group similar images
    groups = []
    used = set()

    for f1, h1 in file_hashes.items():
        if f1 in used:
            continue
        group = [f1]
        for f2, h2 in file_hashes.items():
            if f1 != f2 and f2 not in used and h1 - h2 <= hash_threshold:
                group.append(f2)
                used.add(f2)
        used.add(f1)
        if len(group) > 1:
            groups.append(group)

    return groups

def delete_duplicates(image_directory, groups, keep_first=True):
    deleted_files = []
    for group in groups:
        to_delete = group[1:] if keep_first else group[:-1]
        for file_name in to_delete:
            try:
                os.remove(os.path.join(image_directory, file_name))
                deleted_files.append(file_name)
                print(f"Deleted: {file_name}")
            except Exception as e:
                print(f"Failed to delete {file_name}: {e}")
    return deleted_files

def replace_images_in_markdown(markdown_file_path, groups):
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for group in groups:
        original = group[0]

        for duplicate in group[1:]:
            content = content.replace(f"![]({duplicate})", f"![]({original})")
            
    with open(markdown_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def remove_duplicate_images(workspace): 
    """
    Removes duplicate images from markdown files in the specified directory.
    """
    directory = workspace["directory"]
    markdown_file = workspace["markdown_file"]
    image_files = workspace["image_files"]

    groups = find_near_duplicates(image_files, 15)
    print(f"Found {len(groups)} groups of similar images.")
    
    replace_images_in_markdown(markdown_file, groups)
    deleted = delete_duplicates(directory, groups, keep_first=True)
    print(f"Deleted {len(deleted)} duplicate files.")

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def remove_duplicate_images_command(input_path):
    click.echo(f"Removing duplicate images from markdown files in '{input_path}'...")
    
    # Assert that the input path exists as a directory
    assert os.path.exists(input_path), f"Directory {input_path} does not exist."
    assert os.path.isdir(input_path), f"Path {input_path} is not a directory."

    # Get/process all markdown workspaces 
    workspaces = get_markdown_workspaces(input_path)
    for workspace in workspaces:
        click.echo(f"Processing markdown folder: {workspace["directory"]}")
        remove_duplicate_images(workspace)
    if not workspaces:
        click.echo(f"No markdown files found in '{input_path}'.")

    click.echo(f"Removed duplicate images from markdown files in '{input_path}'")

if __name__ == "__main__":
    remove_duplicate_images_command()