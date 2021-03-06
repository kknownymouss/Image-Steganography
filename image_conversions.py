from PIL import Image
from random import choices
from string import ascii_letters


# Return a dict containing some image references and values
def image_to_pixels(image_path: str) -> dict:
    IMG = Image.open(image_path)
    image_dict: dict = {
        "pixel_access": IMG.load(),
        "original_image": IMG,
        "width": IMG.size[0],
        "height": IMG.size[1]
    }
    return image_dict


# If there is no given filename, generates a random image name and saves it to local directory
def save_image(image, given_filename: str, command: str) -> str:
    if given_filename:
        filename: str = f"{given_filename}_{command}.png" 
    else:
        random_name: function = lambda letters: "".join(choices(letters, k=6))
        filename: str = f"{random_name(ascii_letters)}_{command}.png" 

    image.save(filename)
    return filename
    


