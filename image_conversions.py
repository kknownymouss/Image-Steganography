from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from random import choices
from string import ascii_letters


# Return a dict containing some image references and values
def image_to_pixels(image_path: str) -> dict:
    IMG: JpegImageFile = Image.open(image_path)
    image_dict: dict = {
        "pixel_access": IMG.load(),
        "original_image": IMG,
        "width": IMG.size[0],
        "height": IMG.size[1]
    }
    return image_dict


# If there is no given filename, generates a random image name and saves it to local directory
def save_image(image: JpegImageFile, given_filename: str) -> str:
    if given_filename:
        filename: str = f"{given_filename}_ENCODED.png" 
    else:
        random_name: function = lambda letters: "".join(choices(letters, k=6))
        filename: str = f"{random_name(ascii_letters)}_ENCODED.png" 

    image.save(filename)
    return filename
    


