# Conversion file responsible for conversions to and from 8-bit binary.


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


# Universal conversion function based on types.
def convert(input_type: str, result_type: str, value: str) -> str:
    if input_type == "string" and result_type == "8-bit binary":
        return string_to_8bit_binary(value)

    if input_type == "8-bit binary" and result_type == "string":
        return _8bit_binary_to_string(value)


