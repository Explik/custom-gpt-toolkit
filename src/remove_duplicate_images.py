import click
import os
import imagehash
from PIL import Image
from collections import defaultdict

def find_near_duplicates(image_dir, hash_threshold=5):
    hashes = []
    files = [f for f in os.listdir(image_dir) if f.lower().endswith('.jpeg')]
    file_hashes = {}

    for filename in files:
        filepath = os.path.join(image_dir, filename)
        try:
            img = Image.open(filepath)
            img_hash = imagehash.phash(img)
            file_hashes[filename] = img_hash
        except Exception as e:
            print(f"Error processing {filename}: {e}")

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

def delete_duplicates(image_dir, groups, keep_first=True):
    deleted_files = []
    for group in groups:
        to_delete = group[1:] if keep_first else group[:-1]
        for filename in to_delete:
            try:
                os.remove(os.path.join(image_dir, filename))
                deleted_files.append(filename)
                print(f"Deleted: {filename}")
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")
    return deleted_files

def replace_images_in_markdown(markdown_file_path, groups):
    with open(markdown_file_path, 'r') as file:
        content = file.read()

    for group in groups:
        original = group[0]

        for duplicate in group[1:]:
            content = content.replace(f"![Image]({duplicate})", f"![Image]({original})")
            
    with open(markdown_file_path, 'w') as file:
        file.write(content)


def remove_duplicate_images(input_path): 
    """
    Removes duplicate images from markdown files in the specified directory.
    """
    assert os.path.exists(input_path), f"Directory {input_path} does not exist."

    groups = find_near_duplicates(input_path, 15)
    print(f"Found {len(groups)} groups of similar images.")
    deleted = delete_duplicates(input_path, groups)
    print(f"Deleted {len(deleted)} duplicate files.")

    # Process markdown files
    md_files = [f for f in os.listdir(input_path) if f.lower().endswith('.md')]
    for md_file in md_files:
        md_file_path = os.path.join(input_path, md_file)
        replace_images_in_markdown(md_file_path, groups)

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def remove_duplicate_images_command(input_path):
    click.echo(f"Removing duplicate images from markdown files in '{input_path}'...")
    remove_duplicate_images(input_path)
    click.echo(f"Removed duplicate images from markdown files in '{input_path}'")

if __name__ == "__main__":
    remove_duplicate_images_command()