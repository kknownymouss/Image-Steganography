# Conversion file responsible for conversions to and from 8-bit binary.

# Converts an integer to an 8-bit binary
def integer_to_8bit_binary(integer: int) -> str:
    return format(integer, "08b")


# Converts an 8-bit binary to an integer
def _8bit_binary_to_integer(_8bit_binary: str) -> int:
    return int(_8bit_binary, 2)


# Converts a tuple of rgb values to a tuple of 8-bit binaries
def rgb_to_8bit_binary(rgb: tuple) -> tuple:
    return tuple(map(integer_to_8bit_binary, rgb))


# Converts a tuple of 8-bit binaries to a tuple of rgb values
def _8bit_binary_to_rgb(_8bit_binary: tuple) -> tuple:
    return tuple(map(_8bit_binary_to_integer, _8bit_binary))


# Converts a char to 8-bit binary
def char_to_8bit_binary(char: str) -> str:
    return format(ord(char), "08b")


# Converts a string (multiple chars) to 8-bit binary:
def string_to_8bit_binary(string: str) -> str:
    return "".join(list(map(char_to_8bit_binary, string)))


# Converts an 8-bit binary number to a char
def _8bit_binary_to_char(_8_bit_binary : str) -> str:
    return chr(int(_8_bit_binary, 2))


# Converts a string of 8-bit binary numbers to a string of chars (8-bits for each char)
def _8bit_binary_to_string(_8_bit_binary : str) -> str:
    binary_split: list[str] = [_8_bit_binary[i: i+8] for i in range(0, len(_8_bit_binary), 8)]
    return "".join(_8bit_binary_to_char(j) for j in binary_split)


# Merge the rgb values of parent and hidden image. Parent rgb stays dominant : 4 most significant 
# bits from parent image (rgb_1) and 4 most significant bits form to be encoded image (rgb_2).
def merge_rgb(rgb_1: tuple, rgb_2: tuple) -> tuple:
    _8bit_binary_rgb_1: tuple = rgb_to_8bit_binary(rgb_1)
    _8bit_binary_rgb_2: tuple = rgb_to_8bit_binary(rgb_2)
    merged_8bit_binary: list[str] = []
    for i in range(3):
        new_8bit_binary_rgb: str = _8bit_binary_rgb_1[i][0: 4] + _8bit_binary_rgb_2[i][0: 4]
        merged_8bit_binary.append(new_8bit_binary_rgb)

    return _8bit_binary_to_rgb(merged_8bit_binary)


# Returns the rgb values of the hidden image after unmerging.
def unmerge_rgb(rgb: tuple) -> tuple:
    bin_rgb: tuple = rgb_to_8bit_binary(rgb)
    unmerged: list[str] = []
    for i in bin_rgb:
        unmerged.append(i[4: 8] + "0000") # Add zeros to make it 8 bits. (Originally 4 bits)
        
    return _8bit_binary_to_rgb(unmerged)
    

# Universal conversion function based on types.
def convert(input_type: str, result_type: str, value: str) -> str:
    if input_type == "string" and result_type == "8-bit binary":
        return string_to_8bit_binary(value)

    if input_type == "8-bit binary" and result_type == "string":
        return _8bit_binary_to_string(value)


