# Custom GPT toolkit 
Transform your slides, notes, and documents into a custom GPT with ease.

## Installation 
```sh
pip install -r requirements.txt
```

## Features 
### Convert all your documents into .MD files
MD files do not have any advanced formatting, so they are easy to parse for the model.

Expample:
```sh 
py ./src/convert_to_md.py ./files/input --output_dir ./files/temp
py ./src/remove_md_images.py ./files/temp --output_dir ./files/temp
py ./src/extract_md.py ./files/temp --output_dir ./files/output
```

## Commands 
### `convert_to_md`
Convert all .pdf, .pptx documents into .MD files.

```sh 
convert_to_md <input_file/directory>
```

Flags 
- ```--output_dir <output_directory>```: Specify the output directory for the converted files. If not provided, the default is the input directory.

### `extract_md` 