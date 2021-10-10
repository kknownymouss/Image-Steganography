from io import TextIOWrapper
from PIL.JpegImagePlugin import JpegImageFile
from PIL import PyAccess
from binary_conversions import convert
from random import choice
from image_conversions import save_image


# Manipulates the LSB in each pixel based on the user's message 8-bit binary representation
# Returns the file name
def encode_image(image_dict: dict, message: str, given_filename: str) -> JpegImageFile:

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
    filename: str = save_image(original_image, given_filename)
    return filename



# Decode the image by extracting the 8-bit binary numbers based on the pixel's value parity
# Returns the decoded text
def decode_image(image_dict: dict, textfile: bool) -> str:
    
    # Initialize constants
    COUNTER_LIMIT: int = 8
    STOP_CHAR: str = "~" # A special char to know when to stop looping. Added to message by the encoder.

    # Initialize variables
    pixel_access: PyAccess = image_dict["pixel_access"]
    counter: int = 0
    _8bit_binary_stream: str = ""
    _8bit_binary: str = ""

    for w_pixel in range(image_dict["width"]):
        for h_pixel in range(image_dict["height"]):
            r, g, b = pixel_access[w_pixel, h_pixel]
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

    if textfile:
        new_textfile: TextIOWrapper = open("text_DECODED.txt", "w")
        new_textfile.write(decoded_text)
        return f"Decoded text file saved to text_DECODED.txt"

    else:
        return f"Hidden text: {decoded_text}"


