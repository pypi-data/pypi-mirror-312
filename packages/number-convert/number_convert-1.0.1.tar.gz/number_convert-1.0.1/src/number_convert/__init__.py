import typing


def convert(
    number: typing.Union[str, int, float],
    from_base: int = 2,
    to_base: int = 10,
    max_fractional_length: int = 10,
    alphabet: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/",
    negative_char: str = "-",
    delimiter: str = ".",
):
    number = str(number)

    # Numer bases checks
    if from_base < 2:
        raise ValueError("from_base must be greater than 1")
    if to_base < 2:
        raise ValueError("to_base must be greater than 1")
    if from_base > len(alphabet):
        raise ValueError("alphabet is to short for this from_base")
    if to_base > len(alphabet):
        raise ValueError("alphabet is to short for this to_base")

    # Alphabet checks
    alphabet_from = alphabet[:from_base]
    alphabet_to = alphabet[:to_base]
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet contains repeated characters")
    if negative_char in alphabet:
        raise ValueError("negative_char in alphabet")
    if delimiter in alphabet:
        raise ValueError("delimiter in alphabet")

    # Storing the negativity
    negative = False
    if number[0] == negative_char:
        negative = True
        number = number[1:]

    # Negative and delimiter chars checks
    if number.count(negative_char) > 0:
        raise ValueError("there is more than one negative_char in number")
    if number.count(delimiter) > 1:
        raise ValueError("there is more than delimiter in number")

    # Number splitting
    parts = number.split(delimiter)
    integer_part = parts[0]
    fractional_part = ""
    if len(parts) == 2:
        fractional_part = parts[1]

    # Number specific alphabet check
    for digit in integer_part + fractional_part:
        if digit not in alphabet_from:
            raise ValueError(f"invalid digit {digit} for alphabet")

    # To base10 convertion
    base_10_integer = 0
    base_10_fractional = 0.0

    for i, digit in enumerate(integer_part):
        base_10_integer += alphabet_from.index(digit) * (
            from_base ** (len(integer_part) - 1 - i)
        )
    for i, digit in enumerate(fractional_part):
        base_10_fractional += alphabet_from.index(
            digit) * (from_base ** (-i - 1))

    # From base10 convertion
    integer_part = ""
    fractional_part = ""
    while base_10_integer != 0:
        integer_part += alphabet_to[base_10_integer % to_base]
        base_10_integer = base_10_integer // to_base
    integer_part = integer_part[::-1]
    fractional_length = 0
    while base_10_fractional != 0 and fractional_length != max_fractional_length:
        fractional_length += 1
        base_10_fractional *= to_base
        fractional_part += alphabet_to[int(base_10_fractional // 1)]
        base_10_fractional -= base_10_fractional // 1

    # Number concatination
    if str(integer_part) == "":
        integer_part = alphabet[0]
    number = integer_part + "." + fractional_part
    if str(fractional_part) == "":
        number = integer_part

    # Restoring the negativity
    if number != alphabet[0]:
        if negative:
            number = negative_char + number

    return number
