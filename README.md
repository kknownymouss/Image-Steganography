# Table of contents
1. [Description](#Description)
2. [Background](#Background)
3. [Guide](#Guide)
    1. [Encoding](#Encoding)
        1. [Encoding without the filename option](#encoding_no_filename)
        2. [Encoding with the filename option](#encoding_filename)
    3. [Decoding](#Decoding)
        1. [Decoding without the textfile option](#decoding_no_textfile)
        2. [Decoding with the textfile option](#decoding_textfile)
4. [Extras](#Extras)

<a name="Description"></a>
# Description
A python CLI for image-steganography using the Pillow library.

<a name="Background"></a>
# Background
The Least Significant Bit (LSB) steganography is one such technique in which least significant bit of the image is replaced with data bit.
In this method, the least significant bits of some or all of the bytes inside an image is replaced with a bits of the secret message.

<a name="Guide"></a>
# Guide 
The following CLI is fairly simple to use. Just use the right arguments and the right image names and paths.

You can always type `python main.py --help` or `python main.py -h` to get help.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/help.png)

<a name="Encoding"></a>
## Encoding
Encoding is when you hide a message in an image file. The required and optional arguments to encode are as following:

**General Usage:** `python main.py encode "any_image.jpg" -msg "the message i want to hide" -filename "custom_name"`
1. **command:** `encode`
2. **path of the used image:** `"any_image.jpg"`
3. **message to hide:** `-msg "the message i want to hide"`
  > **Note:**
  > 
  > Please avoid the use of "~" in your message and any other Non Keyboard Characters or the script may not function as expected.
4. **file name of the new image (Optional):** `-filename "custom_name"`

<a name="encoding_no_filename"></a>
### Encoding without the filename option:
**Usage:** `python main.py encode "any_image.jpg" -msg "the message i want to hide"`

In this case, the encoded image will get a **random name** and get saved to the current working directory.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/encode.gif)

<a name="encoding_filename"></a>
### Encoding with the filename option:
**Usage:** `python main.py encode "any_image.jpg" -msg "the message i want to hide" -filename "custom_name"`

In this case, the encoded image will get the name **custom_name** and get saved to the current working directory.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/encode_filename.gif)

<a name="Decoding"></a>
## Decoding
Decoding is when you extract the hidden message from an image file. The required and optional arguments to encode are as following:

**General Usage:** `python main.py decode "custom_name.png" --textfile`
1. **command:** `decode`
2. **path of the used image:** `"any_image.png"`
3. **saves the hidden text to a new text file (Optional):** `--textfile`

<a name="decoding_no_textfile"></a>
### Decoding without the textfile option:
**Usage:** `python main.py decode "custom_name.png"`

In this case, the extracted text will be **displayed in the terminal**.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/decode.gif)
                                                   
<a name="decoding_textfile"></a>
### Decoding with the textfile option:
**Usage:** `python main.py decode "custom_name.png" --textfile`

In this case, the extracted text will be **saved to a new text file**.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/decode_textfile.gif)

<a name="Extras"></a>
# Extras
If you find any bugs or issues, it will be appreciated if you report them. Also any additions or improvement to the current script are welcome !
