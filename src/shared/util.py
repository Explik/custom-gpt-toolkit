from subprocess import Popen, PIPE, STDOUT
import os
import shutil
import re

def run_cli_command(command):
    process = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            try:
                print(line.decode("utf-8").strip())
            except UnicodeDecodeError:
                print("Error decoding the output.")

    return process.wait()

def convert_pdf_to_md(input_path: str, output_path: str) -> None:
    assert os.path.exists(input_path), f"File {input_path} does not exist."

    # Convert PDF to Markdown
    run_cli_command([
        "marker_single", 
        input_path, 
        "--output_dir", output_path
    ])

def convert_pdfs_to_mds(input_directory: str, output_directory: str) -> None:
    assert os.path.exists(input_directory), f"Directory {input_directory} does not exist."

    # Convert PDFs to Markdown
    run_cli_command([
        "marker", 
        input_directory, 
        "--output_dir", output_directory
    ])

def convert_to_md(input_path: str, output_directory: str) -> None:    
    assert os.path.exists(input_path), f"File/directory {input_path} does not exist."

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Convert a single PDF to Markdown
    if os.path.isfile(input_path):
        convert_pdf_to_md(input_path, output_directory)
    elif os.path.isdir(input_path):
        convert_pdfs_to_mds(input_path, output_directory)

def extract_md(input_path: str, output_directory: str) -> None:
    """
    Copies all nested markdown files from the input directory to the output directory.
    """

    assert os.path.exists(input_path), f"Directory {input_path} does not exist."

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Copy all markdown files from the input directory to the output directory
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(".md"):
                source = os.path.join(root, file)
                destination = os.path.join(output_directory, file)
                shutil.copy2(source, destination)
                print(f"Copied {source} to {destination}")

def remove_images(markdown_text):
    return re.sub(r'!\[.*?\]\(.*?\)', '', markdown_text)  

def remove_images_from_md_file(input_path: str, output_directory: str) -> None:
    destination = os.path.join(output_directory, os.path.basename(input_path))
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = remove_images(content)
    with open(destination, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_md_images(input_path: str, output_directory: str) -> None:
    """
    Removes all images from markdown files in the input directory and saves them to the output directory.
    """

    assert os.path.exists(input_path), f"File/directory {input_path} does not exist."

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # If input_path is a file, process it directly
    if os.path.isfile(input_path):
        if input_path.endswith(".md"):
            remove_images_from_md_file(input_path, output_directory)
    # If input_path is a directory, process all markdown files within it
    elif os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".md"):
                    source = os.path.join(root, file)
                    remove_images_from_md_file(source, output_directory)

def flatten_directory(input_path: str, output_directory: str) -> None:
    # Copy all nested files to a single output directory
    # Ex. [input_path]/dir/file.text -> [output_directory]/dir_file.text
    assert os.path.exists(input_path), f"Directory {input_path} does not exist."

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Copy all files from the input directory to the output directory
    for root, _, files in os.walk(input_path):
        for file in files:
            source_path = os.path.join(root, file)
            source_relative_path = os.path.relpath(source_path, input_path)

            destination_file_name = source_relative_path.replace(os.path.sep, "_")
            destination_path = os.path.join(output_directory, destination_file_name)

            shutil.copy2(source_path, destination_path)