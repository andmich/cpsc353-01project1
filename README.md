# Project 1
- By Andrew Michel

# Project Description
- Language used: python3
- Libraries used: PIL, sys, argparse
- My program consists of three function. The first is the main function. The next two are the encrypt and decrypt functions. Depending on the arguments used, main will either encrypt or decrypt and in addition will give an error message if the message to embed is larger than the size of the image.

# How to execute
- To encrypt

```
python3 <PROJECT_NAME> -e <MESSAGE> -i <INPUT_IMAGE> -o <OUTPUT_IMAGE>
```

- to decrypt

```
python3 <PROJECT_NAME> -d <INPUT_IMAGE>
```

- PROJECT_NAME - name of project  
- -e - encrypt option
- MESSAGE - message to embed in picture
- -i - image option
- INPUT_IMAGE - image to embed message
- -o - output image option
- OUTPUT_IMAGE - name of output image in PNG format
