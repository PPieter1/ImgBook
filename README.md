# ImgBook
#### A helper tool for adding AI-generated images to ebooks

## Instructions
1. Clone this repository
2. Install requirements from requirements.txt
3. See Example.ipynb for an example of the workflow:
    1. Import functions
    2. Create summarized book from ePub file
    3. Automatically or manually set indices of chapters in summarized_book object
    4. Generate JSON file that can be imported by sd-webui-agent-scheduler
    5. This repository currently does not offer support for the following steps:
       1. Setup a (local) Stable Diffusion server
       2. Import JSON file with sd-webui-agent-scheduler
       3. Generate all prompts
       4. Place all generated images into a seperate folder. e.g. for SD Next (https://github.com/vladmandic/automatic) the generated images are stored in the /outputs/text/ folder; copy/cut only the images that were generated from the JSON file and paste them in a seperate folder.
    6. Create book with images and enjoy!
