import argparse
import sys
from encode_decode import decode_image_from_image, decode_text_from_image, encode_image_into_image, encode_text_into_image
from image_conversions import image_to_pixels
import string, random, base64


# ANSI escape sequence for terminal colors
class COLOR:
    GREEN: str = '\033[92m'
    RED: str = '\033[91m'
    RESET: str = '\033[0m'
    YELLOW: str = '\033[93m'
    PURPLE: str = '\033[95m'



# A random key generator for encryption
def generate_key() -> str:
    chars: str = string.ascii_letters + string.digits
    random_chars: str = "".join(random.choices(chars, k=10))
    return str(base64.b64encode(bytes(random_chars, "utf-8")), "utf-8")

# This is used for the default argument for encrypt where a random key is chosen
CONSTANT_ENCRYPTION_ARGUMENT: str = generate_key()

# Sets the command-line interface
def set_cmd_parser() -> argparse.ArgumentParser:

    # Initialize constants
    USAGE: str = f'''{COLOR.GREEN}$ python main.py command "image_path" -msg "MESSAGE" -filename "FILENAME" 
        {COLOR.RESET}\nfor more information and help: {COLOR.GREEN}$ python main.py --help{COLOR.RESET}'''
    IMPORTANT_NOTICE: str = f"""{COLOR.RED}IMPORTANT NOTICE: {COLOR.RESET}(TEXT ENCODING) Avoid the use of '~' in the message you want to hide as it leads to weird behaviours. Also avoid the use of Non Keyboard Characters. (IMAGE ENCODING) Avoid the use of highly different image colors and sizes. Also the use of highly dark images is not encouraged."""
    COMMAND_HELP: str = f'''{COLOR.RED}REQUIRED FOR ENCODING/DECODING:{COLOR.RESET} decode or encode.
        E.g, for encoding {COLOR.GREEN}$ python main.py {COLOR.PURPLE}encode{COLOR.GREEN} "img.jpg" -msg "hidden message"{COLOR.RESET}
        E.g, for decoding {COLOR.GREEN}$ python main.py {COLOR.PURPLE}decode{COLOR.GREEN} "img.png" --text{COLOR.RESET}'''
    IMAGE_PATH_HELP: str = f'''{COLOR.RED}REQUIRED FOR ENCODING/DECODING:{COLOR.RESET} the path of the image you wish to encode/decode.
        E.g, for encoding {COLOR.GREEN}$ python main.py encode {COLOR.PURPLE}"img.jpg"{COLOR.GREEN} -img "img1.jpg"{COLOR.RESET}
        E.g, for decoding {COLOR.GREEN}$ python main.py decode {COLOR.PURPLE}"img.png"{COLOR.RESET}{COLOR.GREEN} --image{COLOR.RESET}'''
    MSG_HELP: str = f'''{COLOR.RED}REQUIRED FOR ENCODING TEXT IN IMAGE:{COLOR.RESET} message to be encoded.
        E.g, for encoding {COLOR.GREEN}$ python main.py encode "img.jpg" {COLOR.PURPLE}-msg "hidden"{COLOR.RESET}'''
    IMG_HELP: str = f'''{COLOR.RED}REQUIRED FOR ENCODING IMAGE IN IMAGE:{COLOR.RESET} image to be encoded.
        E.g, for encoding {COLOR.GREEN}$ python main.py encode "img.jpg" {COLOR.PURPLE}-img "img2.jpg"{COLOR.RESET}'''
    TEXT_HELP: str = f'''{COLOR.RED}REQUIRED FOR DECODING TEXT FROM IMAGE:{COLOR.RESET} displays decoded text from image on screen.
        E.g, for decoding {COLOR.GREEN}$ python main.py decode "img.png" {COLOR.PURPLE}--text{COLOR.RESET}'''
    IMAGE_HELP: str = f'''{COLOR.RED}REQUIRED FOR DECODING IMAGE FROM IMAGE:{COLOR.RESET} creates an image file that contains the decoded image.
        E.g, for decoding {COLOR.GREEN}$ python main.py decode "img.png" {COLOR.PURPLE}--image{COLOR.RESET}'''
    FILENAME_HELP: str = f'''{COLOR.YELLOW}OPTIONAL FOR ENCODING/DECODING:{COLOR.RESET} filename of the encoded/decoded image.
        E.g, for encoding {COLOR.GREEN}$ python main.py encode "img.png" -msg "hidden" {COLOR.PURPLE}-filename "new_image"{COLOR.RESET}
        E.g, for decoding {COLOR.GREEN}$ python main.py decode "img.png" --image {COLOR.PURPLE}-filename "new_image"{COLOR.RESET}'''
    TEXTFILE_HELP: str = f'''{COLOR.YELLOW}OPTIONAL FOR DECODING TEXT FROM IMAGE:{COLOR.RESET} creates a text file that contains the decoded text.
        E.g, for decoding {COLOR.GREEN}$ python main.py decode "img.png" --text {COLOR.PURPLE}--textfile{COLOR.RESET}'''
    DECRYPT_HELP: str = f'''{COLOR.YELLOW}OPTIONAL FOR DECODING TEXT FROM IMAGE:{COLOR.RESET} The decryption key if the hidden message was encrypted.
        E.g, for decoding {COLOR.GREEN}$ python main.py decode "img.png" --text {COLOR.PURPLE}-decrypt "decryption_key"{COLOR.RESET}'''
    ENCRYPT_HELP: str = f'''{COLOR.YELLOW}OPTIONAL FOR ENCODING TEXT IN IMAGE:{COLOR.RESET} The encryption key. If no key is specified, a random key will be chosen.
        E.g, for encoding with custom encryption key{COLOR.GREEN} $ python main.py encode "img.png" -msg "random message" {COLOR.PURPLE}-encrypt "encryption_key"{COLOR.RESET}
        E.g, for encoding with random encryption key{COLOR.GREEN} $ python main.py encode "img.png" -msg "random message" {COLOR.PURPLE}-encrypt{COLOR.RESET}'''

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=IMPORTANT_NOTICE, prog='Image Steganography', usage=USAGE, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", type=str, help=COMMAND_HELP)
    parser.add_argument("image_path", type=str, help=IMAGE_PATH_HELP)
    parser.add_argument("-msg", type=str, help=MSG_HELP)
    parser.add_argument("-img", type=str, help=IMG_HELP)
    parser.add_argument("--image", action="store_true", help=IMAGE_HELP)
    parser.add_argument("--text", action="store_true", help=TEXT_HELP)
    parser.add_argument("--textfile", action="store_true", help=TEXTFILE_HELP)
    parser.add_argument("-filename", type=str, default="", help=FILENAME_HELP)
    parser.add_argument("-encrypt", nargs="?", type=str, default="", const=CONSTANT_ENCRYPTION_ARGUMENT, help=ENCRYPT_HELP)
    parser.add_argument("-decrypt", type=str, default="", help=DECRYPT_HELP)
    return parser


# Exit the main function due to invalid arguments
def argument_error(parser: argparse.ArgumentParser) -> None:
    print(f"\n{COLOR.YELLOW}Please make sure the passed arguments are valid.{COLOR.RESET}\n")
    parser.print_help()
    sys.exit()


# Exit the main function due to encode/decoding internal errors
def internal_error() -> None:
    print(f"\n{COLOR.YELLOW}Something went wrong. Please try again and check for any spelling mistakes.{COLOR.RESET}\n")
    sys.exit()


# Main function of the script
def main() -> None:

    # Initialize constants
    PARSER: argparse.ArgumentParser = set_cmd_parser()
    PARSER_RESULTS: argparse.Namespace = PARSER.parse_args()
    COMMAND: str = PARSER_RESULTS.command
    IMAGE_PATH: str = PARSER_RESULTS.image_path
    MSG: str = PARSER_RESULTS.msg
    IMG: str = PARSER_RESULTS.img
    FILENAME: str = PARSER_RESULTS.filename
    TEXTFILE: bool = PARSER_RESULTS.textfile
    TEXT: bool = PARSER_RESULTS.text
    IMAGE: bool = PARSER_RESULTS.image
    ENCRYPT: str = PARSER_RESULTS.encrypt
    DECRYPT: str = PARSER_RESULTS.decrypt

    # Check the cmd arguments and exit with a message if there are any invalid/missing arguments or 
    # internal errors. Otherwise, continue executing the function

    if COMMAND != "encode" and COMMAND != "decode":
        argument_error(PARSER)
        
    if COMMAND == "encode":
        if bool(MSG) == bool(IMG):
            argument_error(PARSER)

        try:
            if MSG:
                image_dict: dict = image_to_pixels(IMAGE_PATH)

                # Check if encrypt argument is there and then check if its the constant argument (for random key generation) or a user custom key.
                if ENCRYPT:
                    if ENCRYPT == CONSTANT_ENCRYPTION_ARGUMENT: # constant argument (random encryption key)
                        key: str = generate_key()
                    
                    else: # custom encryption key
                        key: str = ENCRYPT
                        
                    filename: str = encode_text_into_image(image_dict, MSG, FILENAME, key)
                    print(f"\n{COLOR.GREEN}Image encoded successfully. Saved to {filename}\nEncryption/Decryption Key: {key}{COLOR.RESET}\n")
                else:
                    key: str = ""
                    filename: str = encode_text_into_image(image_dict, MSG + "~", FILENAME, key)
                    print(f"\n{COLOR.GREEN}Image encoded successfully. Saved to {filename}{COLOR.RESET}\n")
            elif IMG:
                image1_dict: dict = image_to_pixels(IMAGE_PATH)
                image2_dict: dict = image_to_pixels(IMG)
                filename: str = encode_image_into_image(image1_dict, image2_dict, FILENAME)
                print(f"\n{COLOR.GREEN}Image encoded successfully. Saved to {filename}{COLOR.RESET}\n")

        except BaseException:
            internal_error()
    
    else:
        if IMAGE_PATH.split(".")[-1] != "png":
            argument_error(PARSER)
        
        if TEXT == IMAGE:
            argument_error(PARSER)

        try:
            if TEXT:
                image_dict: dict = image_to_pixels(IMAGE_PATH)

                # If decrypt argument is there, set key to its value, otherwise key and value will be ""
                key: str = DECRYPT

                decoding_results: str = decode_text_from_image(image_dict, TEXTFILE, key)
                print(f"\n{COLOR.GREEN}Image decoded successfully.\n{decoding_results}{COLOR.RESET}\n")
            elif IMAGE:
                image_dict: dict = image_to_pixels(IMAGE_PATH)
                decoding_results: str = decode_image_from_image(image_dict, FILENAME)
                print(f"\n{COLOR.GREEN}Image decoded successfully. Saved to {decoding_results}{COLOR.RESET}\n")


        except BaseException:
            internal_error()



# Run the script
if __name__ == "__main__":
    main()






    

