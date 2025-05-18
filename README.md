# Custom GPT toolkit 
Transform your slides, notes, and documents into a custom GPT with ease.

## Installation 
Install the required packages using pip. 
```sh
pip install -r requirements.txt
```

Also, install the dependencies of the [marker-pdf](https://github.com/VikParuchuri/marker?tab=readme-ov-file#installation) pacakge

## Usage 
### Flatten directory structure 
This command will flatten a directory structure by renaming files to include their parent directory names. 
```sh
py flatten_directory_structure <input_directory> --output_dir <output_directory>
```

Example:
```
\directory
    \subdirectory1
        file1.pdf
        file2.pdf
    \subdirectory2
        file3.pdf
        file4.pdf

becomes

\directory
    subdirectory1_file1.pdf
    subdirectory1_file2.pdf
    subdirectory2_file3.pdf
    subdirectory2_file4.pdf
```

### Convert docments into .MD files
This command will convert all .pdf documents into .MD folders. 
```sh 
convert_to_md <input_file/directory> --output_dir <output_directory>
```

Example: 
```
\directory
    file1.pdf
    file2.pdf

becomes

\directory
    \file1
        file1.md
        image1.png
        image2.png
    \file2
        file2.md
        image1.png
        image2.png
```

### Remove all images from .MD files
This command will remove all images from .MD files while keeping the .MD files intact. 
```sh
remove_all_images <input_file> --output_dir <output_directory>
```

Example:
```
\directory
    \file1
        file1.md
        image1.jpg
        image2.jpg
    \file2
        file2.md
        image1.jpg
        image2.jpg

becomes
\directory
    \file1
        file1.md
    \file2
        file2.md
```


### Remove duplicate images from .MD files
This command will remove all duplicate images from .MD files while keeping the .MD files intact. 
```sh
remove_duplicate_images <input_file> --output_dir <output_directory>
```

Example:
```
\directory
    \file1
        file1.md
        image1.jpg
        image2.jpg (duplicate)
    \file2
        file2.md
        image1.jpg
        image2.jpg (duplicate)

becomes

\directory
    \file1
        file1.md
        image1.jpg
    \file2
        file2.md
        image1.jpg
```

### Replace images with explanations in .MD files
This command will replace all images in .MD files with explanations. 
```sh
replace_images_with_explanation <input_folder> --output_dir <output_directory>
```

Example:
```
\directory
    \file1
        file1.md
        image1.jpg
        image2.jpg
    \file2
        file2.md
        image1.jpg
        image2.jpg

becomes
\directory
    \file1
        file1.md (with image explanations)
    \file2
        file2.md (with image explanations)
```

### Extract .MD files from directory structure
This command will extract all .MD files from a directory structure and save them in a single directory. 
```sh
extract_md_files <input_directory> --output_dir <output_directory>
```

Example:
```
\directory
    \file1
        file1.md
        image1.jpg
    \file2
        file2.md
        image1.jpg

becomes

\directory
    file1.md
    file2.md
```