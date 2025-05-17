import click
import os 
from dotenv import load_dotenv
from openai import OpenAI
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_explanation(image_path):
    image_base64 = encode_image(image_path)

    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "Forklar det følgende billede. Konteksten er et System Udviklings kursus" },
                    { "type": "input_image", "image_url": f"data:image/jpg;base64,{image_base64}", "detail": "low" }
                ]
            }
        ]
    )

    return f"==== Billede ====\n {response.output_text} \n=========\n" 

def replace_image_in_markdown(markdown_file, image_explanations_map):
    # Replace images with explanations in the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()

    for image_path, explanation in image_explanations_map.items():
        image_filename = os.path.basename(image_path)
        content = content.replace(f"![]({image_filename})", explanation)

    with open(markdown_file, 'w', encoding='utf-8') as file:
        file.write(content)

def replace_images_with_explanation(input_path):
    # Find all images files in input_path folder 
    image_files = []
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))

    image_explations = {
        image_file: generate_explanation(image_file) for image_file in image_files
    }

    # Replace images with explanations in markdown files
    md_files = []
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.md'):
                md_files.append(os.path.join(root, file))

    for md_file in md_files:
        replace_image_in_markdown(md_file, image_explations)

    # Delete the images
    for image_file in image_files:
        os.remove(image_file)
    
@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def replace_images_with_explanation_command(input_path):
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None:
        click.echo("Please set the OPENAI_API_KEY environment variable.")
        return
    
    click.echo(f"Replacing images with explanations in markdown files in '{input_path}'...")
    replace_images_with_explanation(input_path)
    click.echo(f"Replaced images with explanations in markdown files in '{input_path}'.")

if __name__ == "__main__":
    replace_images_with_explanation_command()