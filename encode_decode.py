from io import TextIOWrapper
from PIL.JpegImagePlugin import JpegImageFile
from PIL import Image, PyAccess
from binary_conversions import convert
from random import choice
from image_conversions import save_image
from binary_conversions import merge_rgb, unmerge_rgb
from AesEverywhere import aes256

# Manipulates the LSB in each pixel based on the user's message 8-bit binary representation
# Returns the file name
def encode_text_into_image(image_dict: dict, message: str, given_filename: str, key: str) -> str:

    # Encrypt if key is valid, and add stop char "~"
    if key:
        message = str(aes256.encrypt(message, key), "utf-8") + "~"
    else:
        message += "~"

    # Initialize constants
    ENCODED_MESSAGE: str = convert("string", "8-bit binary", message)
    COUNTER_LIMIT: int = len(ENCODED_MESSAGE)

    # Initialize variables
    original_image: JpegImageFile = image_dict["original_image"]
    pixel_access: PyAccess = image_dict["pixel_access"]
    counter: int = 0

    for w_pixel in range(image_dict["width"]):
        for h_pixel in range(image_dict["height"]):
            if counter == COUNTER_LIMIT:
                break

            r, g, b = pixel_access[w_pixel, h_pixel]
            pixel_iter: list[int] = [r, g, b]
            # Change the pixel value in pixel_iter according to its parity
            for i in range(3):
                if counter == COUNTER_LIMIT:
                    break
                if pixel_iter[i] % 2 == 0 and int(ENCODED_MESSAGE[counter]) == 0: 
                    counter += 1
                elif pixel_iter[i] % 2 != 0 and int(ENCODED_MESSAGE[counter]) == 1:
                    counter += 1
                else:
                    if pixel_iter[i] == 0:
                        pixel_iter[i] += 1
                    elif pixel_iter[i] == 255:
                        pixel_iter[i] -= 1
                    else:
                        pixel_iter[i] += choice([-1, 1])
                    counter += 1

            # Apply changes to the pixel_access object after looping over the 3 RGB values.
            pixel_access[w_pixel, h_pixel] = tuple(pixel_iter)
        else:
            continue
        break
    
    # Get filename from save_image() and return it
    filename: str = save_image(original_image, given_filename, "ENCODED")
    return filename



# Decode the image by extracting the 8-bit binary numbers based on the pixel's value parity
# Returns the decoded text
def decode_text_from_image(image_dict: dict, textfile: bool, key: str) -> str:
    
    # Initialize constants
    COUNTER_LIMIT: int = 8
    STOP_CHAR: str = "~" # A special char to know when to stop looping. Added to message by the encoder.
    PIXEL_ACCESS: PyAccess = image_dict["pixel_access"]

    # Initialize variables
    counter: int = 0
    _8bit_binary_stream: str = ""
    _8bit_binary: str = ""

    for w_pixel in range(image_dict["width"]):
        for h_pixel in range(image_dict["height"]):
            r, g, b = PIXEL_ACCESS[w_pixel, h_pixel]
            pixel_iter: list[int] = [r, g, b]

            # Adds 0 or 1 to the _8it_binary after checking the RGB value in the pixel
            for i in pixel_iter:

                # If _8bit_binary length becomes 8 (8-bits), check if it matches STOP_CHAR, add it
                # to _8bit_binary_stream, reset it and continue looping
                if counter >= COUNTER_LIMIT:
                    if convert("8-bit binary", "string", _8bit_binary) == STOP_CHAR:
                        break
                    counter = 0
                    _8bit_binary_stream += _8bit_binary
                    _8bit_binary = ""
                if i % 2 == 0:
                    _8bit_binary += "0"
                elif i % 2 != 0:
                    _8bit_binary += "1"
                counter += 1
            else: 
                continue
            break                
        else:
            continue
        break

    # Convert the _8bit_binary_stream to a char string and return it in the specified form
    decoded_text: str = convert("8-bit binary", "string", _8bit_binary_stream)

    # If there is a key, decrypt the encrypted message
    if key:
        try:
            decrypted_text: str = str(aes256.decrypt(decoded_text, key), "utf-8")
        except BaseException:
            decrypted_text: str = "The message is not encrypted. Please remove the decryption key."

    else:
        decrypted_text: str = decoded_text

    if textfile:
        new_textfile: TextIOWrapper = open("text_DECODED.txt", "w")
        new_textfile.write(decrypted_text)
        return f"Decoded text file saved to text_DECODED.txt"

    else:
        return f"Hidden text: {decrypted_text}"


# Image 1 is the parent image, image 2 is the to be encoded image.
def encode_image_into_image(image1_dict: dict, image2_dict: dict, given_filename: str) -> str:

    # Initialize constants
    ENCODED_IMAGE_PIXEL_ACCESS: PyAccess = image2_dict["pixel_access"]
    
    # Initialize variables
    original_image = image1_dict["original_image"]
    original_image_pixel_access: PyAccess = image1_dict["pixel_access"]

    # Loop through rgb values in each image and merge them to a tuple so that original image stays
    # dominant. Use that tuple to change original image pixels.
    for i in range(image1_dict['width']):
        for j in range(image1_dict['height']):

            # Initialize color tuples for each loop
            encoded_image_rgb_tuple: tuple = (255 ,220, 172) # Used to know crop dimensions in decoding
            original_image_rgb_tuple: tuple = original_image_pixel_access[i, j]

            # Change the default color to the encoded image colors 
            # if the index is greater than the hidden image size
            if i < image2_dict['width'] and j < image2_dict['height']:
                encoded_image_rgb_tuple: tuple = ENCODED_IMAGE_PIXEL_ACCESS[i, j]

            # Merge the colors and assign it to original image
            original_image_pixel_access[i, j] = merge_rgb(original_image_rgb_tuple, encoded_image_rgb_tuple)

    # Get filename from save_image() and return it
    filename: str = save_image(original_image, given_filename, "ENCODED")
    return filename

    

def decode_image_from_image(image_dict: dict, given_filename: str) -> str:
    
    # Initialize constants
    ORIGINAL_IMAGE_PIXEL_ACCESS: PyAccess = image_dict["pixel_access"]

    # Initialize variables
    result_image: Image.Image = Image.new("RGB", (image_dict["width"], image_dict["height"]))
    result_image_pixel_access: PyAccess = result_image.load()
    crop_dimensions: list[int] = [0, 0]

    # Loop through rgb values in each image and unmerge them to a tuple so that encoded image stays
    # dominant. Use that tuple to change new image pixels.
    for i in range(image_dict["width"]):
        for j in range(image_dict["height"]):
            
            # Unmerge the colors and assign it to result_image
            result_image_pixel_access[i, j] = unmerge_rgb(ORIGINAL_IMAGE_PIXEL_ACCESS[i, j])

            # set crop dimensions to last valid width and height where condition is not satisfied
            if unmerge_rgb(ORIGINAL_IMAGE_PIXEL_ACCESS[i, j]) != (240, 208, 160):
                crop_dimensions: int = [i, j]


    result_image: Image.Image = result_image.crop((0, 0, crop_dimensions[0], crop_dimensions[1]))
    filename: str = save_image(result_image, given_filename, 'DECODED')
    return filename