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

def get_files_of_type(input_path: str, file_types: list) -> list:
    """
    Returns a list of files of the specified types in the given directory.
    """
    assert os.path.exists(input_path), f"Directory {input_path} does not exist."
    
    files = []
    for root, _, filenames in os.walk(input_path):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in file_types):
                files.append(os.path.join(root, filename))
    return files

def get_markdown_workspaces(input_path: str) -> list:
    md_files = get_files_of_type(input_path, ['.md'])

    folder_infos = []
    for md_file in md_files:
        folder = os.path.dirname(md_file)
        image_files = get_files_of_type(folder, ['.jpg', '.jpeg'])

        folder_infos.append({
            "directory": folder,
            "markdown_file": md_file,
            "image_files": image_files
        })

    return folder_infos

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