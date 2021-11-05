# Table of contents
1. [Description](#Description)
2. [Background](#Background)
3. [Guide](#Guide)
    1. [Encoding Text In Image](#Encoding-text-in-image)
        1. [Using -filename Option](#using_filename_text_encode)
        2. [Using -encrypt Option](#using_encrypt_text_encode)
    2. [Encoding Image In Image](#Encoding-image-in-image)
        1. [Using -filename Option](#using_filename_image_encode)
    3. [Decoding Text From Image](#Decoding-text-from-image)
        1. [Using --textfile Option](#using_textfile_text_decode)
        2. [Using -decrypt Option](#using_decrypt_text_decode)
    4. [Decoding Image From Image](#Decoding-image-from-image)
        1. [Using -filename Option](#using_filename_image_decode)
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

<a name="Encoding-text-in-image"></a>
## Encoding Text In Image
Encoding text in image is when you hide a message in an image file. The required and optional arguments to encode are as following:

**General Usage:** `python main.py encode "any_image.jpg" -msg "the message i want to hide" -filename "custom_name" -encrypt "custom_key"`
1. **command:** `encode`
2. **path of the used image:** `"any_image.jpg"`
3. **message to hide:** `-msg "the message i want to hide"`
  > **Note:**
  > 
  > Please avoid the use of "~" in your message and any other Non Keyboard Characters or the script may not function as expected.
4. **file name of the new image (Optional):** `-filename "custom_name"`
5. **encryption/decryption key for the encoded text (Optional):**
    1. **Custom Encryption Key:** `-encrypt "custom_key"`
    2. **Random Encryption Key:** `-encrypt`

<a name="using_filename_text_encode"></a>
### Using the -filename option:

**Usage:** `python main.py encode "any_image.jpg" -msg "the message i want to hide" -filename "custom_name"`

In this case, the encoded image will get the name **custom_name** and get saved to the current working directory. If the `-filename "custom_name"` argument was **removed**, the encoded image will get a **random name** and get saved to the working directory.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/filename_text_encode.gif)

<a name="using_encrypt_text_encode"></a>
### Using the -encrypt option:

**Usage:**

**Custom Encryption Key**: `python main.py encode "any_image.jpg" -msg "the message i want to hide" -encrypt "custom_key"`

In this case, the encoded text will be encrypted (AES256) with a **custom key** of your choice. This means that **no one** without your custom key can view the text encoded in the image

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/encrypt_custom_text_encode.gif)

**Random Encryption Key**: `python main.py encode "any_image.jpg" -msg "the message i want to hide" -encrypt`

In this case, the encoded text will be encrypted with a **random key** chosen by the program itself (Recommended). This means that **no one** without the random key can view the text encoded in the image. The generated random key will be displayed after encoding is done successfully.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/encrypt_random_text_encode.gif)

<a name="Encoding-image-in-image"></a>
## Encoding Image In Image
Encoding image in image is when you hide an image in another image file. The required and optional arguments to encode are as following:

**General Usage:** `python main.py encode "any_image.jpg" -img "hidden_img.jpg" -filename "custom_name"`
1. **command:** `encode`
2. **path of the used image:** `"any_image.jpg"`
3. **image to hide:** `-img "hidden_img.jpg"`
  > **Note:**
  > 
  > Please avoid the use of highly different image colors and sizes. The use of black images may not perfectly work and is discouraged.
4. **file name of the new image (Optional):** `-filename "custom_name"`

<a name="using_filename_image_encode"></a>
### Using the -filename option:
**Usage:** `python main.py encode "any_image.jpg" -img "hidden_img.jpg" -filename "custom_name"`

In this case, the encoded image will get the name **custom_name** and get saved to the current working directory. If the `-filename "custom_name"` argument was **removed**, the encoded image will get a **random name** and get saved to the working directory.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/filename_image_encode.gif)

<a name="Decoding-text-from-image"></a>
## Decoding Text From Image
Decoding Text from image is when you extract the hidden message from an image file. The required and optional arguments to encode are as following:

**General Usage:** `python main.py decode "custom_name.png" --text --textfile`
1. **command:** `decode`
2. **path of the used image:** `"any_image.png"`
3. **kind of decoding result:** `--text`
4. **saves the hidden text to a new text file (Optional):** `--textfile`
5. **decryption key for encoded txt (Optional):** `-decrypt "decryption_key"`
> **Note** 
> 
> Using this argument `-decrypt` for images that has normal text encoded and not encrypted ones may lead to weird behaviours.
> 
> If the used decryption key is not right, the script may display that the text encoded is not encrypted. (rarely happens)


<a name="using_textfile_text_decode"></a>
### Using the --textfile option:
**Usage:** `python main.py decode "custom_name.png" --text --textfile`

In this case, the extracted text will be **saved to a new text file**. If the `--textfile` argument was **removed**, the hidden text will get **displayed in the terminal**.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/textfile_text_decode.gif)

<a name="using_decrypt_text_decode"></a>
### Using the -decrypt option:
**Usage:** `python main.py decode "custom_name.png" --text -decrypt "custom_key"`

In this case, we will use the **random or custom encryption key** we got when we encrypted our message to **decrypt the decoded text** from image. If the `-decrypt` option is not used and we try to decode an encoded encrypted message, we will see an AES256 encrypted message. Also, if we try a **wrong decryption key**, we will see an **emtpy message.**

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/decrypt_text_decode.gif)


<a name="Decoding-image-from-image"></a>
## Decoding Image From Image
Decoding Image from image is when you extract the hidden image from an image file. The required and optional arguments to encode are as following:

**General Usage:** `python main.py decode "custom_image.png" --image -filename "new_image"`
1. **command:** `decode`
2. **path of the used image:** `"any_image.png"`
3. **kind of decoding result:** `--image`
4. **file name of the new image (Optional):** `-filename "new_image"`


<a name="using_filename_image_decode"></a>
### Using the -filename option:
**Usage:** `python main.py decode "custom_name.png" --image -filename "custom_name"`

In this case, the extracted image will get the name **custom_name** and get saved to the current working directory.If the `-filename "custom_name"` argument was **removed**, the decoded image will get a **random name** and get saved to the working directory.

![image](https://github.com/kknownymouss/Image-Steganography/blob/master/README_media/filename_image_decode.gif)

<a name="Extras"></a>
# Extras
If you find any bugs or issues, it will be appreciated if you report them. Also any additions or improvement to the current script are welcome !
