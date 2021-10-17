import argparse
import sys
from encode_decode import decode_text_from_image, encode_text_into_image
from image_conversions import image_to_pixels


# ANSI escape sequence for terminal colors
class COLOR:
    GREEN: str = '\033[92m'
    RED: str = '\033[91m'
    RESET: str = '\033[0m'
    YELLOW: str = '\033[93m'
    PURPLE: str = '\033[95m'


# Sets the command-line interface
def set_cmd_parser() -> argparse.ArgumentParser:

    # Initialize constants
    USAGE: str = f'''{COLOR.GREEN}$ python main.py command "image_path" -msg "MESSAGE" -filename "FILENAME" 
        {COLOR.RESET}\nfor more information and help: {COLOR.GREEN}$ python main.py --help{COLOR.RESET}'''
    IMPORTANT_NOTICE: str = f"""{COLOR.RED}IMPORTANT NOTICE: {COLOR.RESET}Avoid the use of '~' in the message you want to hide as it leads to weird behaviours. Also avoid the use of Non Keyboard Characters."""
    COMMAND_HELP: str = f'''{COLOR.RED}REQUIRED FOR ENCODING/DECODING:{COLOR.RESET} decode or encode.
        E.g, for encoding {COLOR.GREEN}$ python main.py {COLOR.PURPLE}encode{COLOR.GREEN} "img.jpg" -msg "hidden message"{COLOR.RESET}
        E.g, for decoding {COLOR.GREEN}$ python main.py {COLOR.PURPLE}decode{COLOR.GREEN} "img.png"{COLOR.RESET}'''
    IMAGE_PATH_HELP: str = f'''{COLOR.RED}REQUIRED FOR ENCODING/DECODING:{COLOR.RESET} the path of the image you wish to encode/decode.
        E.g, for encoding {COLOR.GREEN}$ python main.py encode {COLOR.PURPLE}"img.jpg"{COLOR.GREEN} -msg "any message"{COLOR.RESET}
        E.g, for decoding {COLOR.GREEN}$ python main.py decode {COLOR.PURPLE}"img.png"{COLOR.RESET}'''
    MSG_HELP: str = f'''{COLOR.RED}REQUIRED FOR ENCODING:{COLOR.RESET} message to be encoded.
        E.g, for encoding {COLOR.GREEN}$ python main.py encode "img.jpg" {COLOR.PURPLE}-msg "hidden"{COLOR.RESET}'''
    FILENAME_HELP: str = f'''{COLOR.YELLOW}OPTIONAL FOR ENCODING:{COLOR.RESET} filename of the encoded image.
        E.g, for encoding {COLOR.GREEN}$ python main.py encode "img.png" -m "hidden" {COLOR.PURPLE}-filename "new_image"{COLOR.RESET}'''
    TEXTFILE_HELP: str = f'''{COLOR.YELLOW}OPTIONAL FOR DECODING:{COLOR.RESET} creates a text file that contains the decoded text.
        E.g, for decoding {COLOR.GREEN}$ python main.py decode "img.png" {COLOR.PURPLE}--textfile{COLOR.RESET}'''

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=IMPORTANT_NOTICE, prog='Image Steganography', usage=USAGE, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", type=str, help=COMMAND_HELP)
    parser.add_argument("image_path", type=str, help=IMAGE_PATH_HELP)
    parser.add_argument("-msg", type=str, help=MSG_HELP)
    parser.add_argument("-filename", type=str, default="", help=FILENAME_HELP)
    parser.add_argument("--textfile", action="store_true", help=TEXTFILE_HELP)
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
    MESSAGE: str = PARSER_RESULTS.msg
    FILENAME: str = PARSER_RESULTS.filename
    TEXTFILE: bool = PARSER_RESULTS.textfile

    # Check the cmd arguments and exit with a message if there are any invalid/missing arguments or 
    # internal errors. Otherwise, continue executing the function

    if COMMAND != "encode" and COMMAND != "decode":
        argument_error(PARSER)
        
    if COMMAND == "encode":
        if not MESSAGE:
            argument_error(PARSER)

        try:
            image_dict: dict = image_to_pixels(IMAGE_PATH)
            filename: str = encode_text_into_image(image_dict, MESSAGE + "~", FILENAME)
            print(f"\n{COLOR.GREEN}Image encoded successfully. Saved to {filename}{COLOR.RESET}\n")

        except BaseException:
            internal_error()
    
    else:
        if IMAGE_PATH.split(".")[-1] != "png":
            argument_error(PARSER)

        try:
            image_dict: dict = image_to_pixels(IMAGE_PATH)
            decoding_results: str = decode_text_from_image(image_dict, TEXTFILE)
            print(f"\n{COLOR.GREEN}Image decoded successfully. {decoding_results}{COLOR.RESET}\n")

        except BaseException:
            internal_error()



# Run the script
if __name__ == "__main__":
    main()






    

