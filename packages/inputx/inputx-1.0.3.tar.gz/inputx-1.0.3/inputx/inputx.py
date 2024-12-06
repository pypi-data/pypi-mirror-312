import msvcrt
import sys


# Allowed character sets
SYMBOL_BYTES = {b'\x21', b'\x22', b'\x23', b'\x24', b'\x25', b'\x26', b'\x27', b'\x28',  # !"#$%&'(
                b'\x29', b'\x2a', b'\x2b', b'\x2c', b'\x2d', b'\x2e', b'\x2f',           # )*+,-./
                b'\x3a', b'\x3b', b'\x3c', b'\x3d', b'\x3e', b'\x3f', b'\x40',           # :;<=>?@
                b'\x5b', b'\x5c', b'\x5d', b'\x5e', b'\x5f', b'\x60',                    # [\]^_`
                b'\x7b', b'\x7c', b'\x7d', b'\x7e'}                                      # {|}~

DIGITAL_BYTES = {b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x35', b'\x36', b'\x37', b'\x38', b'\x39'}

EN_LETTER_BYTES = {b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47', b'\x48',  # ABCDEFGH
                   b'\x49', b'\x4a', b'\x4b', b'\x4c', b'\x4d', b'\x4e', b'\x4f',           # IJKLMNO
                   b'\x50', b'\x51', b'\x52', b'\x53', b'\x54', b'\x55', b'\x56', b'\x57',  # PQRSTUVW
                   b'\x58', b'\x59', b'\x5a',                                               # XYZ
                   b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x68',  # abcdefgh
                   b'\x69', b'\x6a', b'\x6b', b'\x6c', b'\x6d', b'\x6e', b'\x6f',           # ijklmno
                   b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77',  # pqrstuvw
                   b'\x78', b'\x79', b'\x7a'}                                               # xyz

RU_LETTER_BYTES = {b'\x80', b'\x81', b'\x82', b'\x83', b'\x84', b'\x85', b'\x86', b'\x87',  # АБВГДЕЖЗ
                   b'\x88', b'\x89', b'\x8a', b'\x8b', b'\x8c', b'\x8d', b'\x8e', b'\x8f',  # ИЙКЛМНОП
                   b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97',  # РСТУФХЦЧ
                   b'\x98', b'\x99', b'\x9a', b'\x9b', b'\x9c', b'\x9d', b'\x9e', b'\x9f',  # ШЩЪЫЬЭЮЯ
                   b'\xa0', b'\xa1', b'\xa2', b'\xa3', b'\xa4', b'\xa5', b'\xa6', b'\xa7',  # абвгдежз
                   b'\xa8', b'\xa9', b'\xaa', b'\xab', b'\xac', b'\xad', b'\xae', b'\xaf',  # ийклмноп
                   b'\xe0', b'\xe1', b'\xe2', b'\xe3', b'\xe4', b'\xe5', b'\xe6', b'\xe7',  # рстуфхцч
                   b'\xe8', b'\xe9', b'\xea', b'\xeb', b'\xec', b'\xed', b'\xee', b'\xef',  # шщъыьэюя
                   b'\xf0', b'\xf1'}                                                        # Ёё

allowed_chars_set = {b'\x20'}  # Space character


def inputx(prompt='',
           data_type='str',
           invisible_input=False,
           only_ru_letters=False,
           only_en_letters=False,
           only_digitals=False,
           only_symbols=False,
           end: str = '\n'):
    """
    Advanced input function for Windows terminal-based Python applications.
    Features:
    - Character type filtering (digits, Russian/English letters, symbols).
    - Real-time visible input editing with cursor navigation.
    - Support for invisible input (e.g., for passwords).
    - Input validation for integers and floats.

    Arguments:
        prompt (str): The prompt to display before input.
        data_type (str): The expected data type ('str', 'int', or 'float').
        invisible_input (bool): If True, input will not be displayed on the terminal.
        only_ru_letters (bool): If True, restrict input to Russian letters.
        only_en_letters (bool): If True, restrict input to English letters.
        only_digitals (bool): If True, restrict input to digits.
        only_symbols (bool): If True, restrict input to symbols.
        end (str): The string to append at the end of input.

    Returns:
        str|int|float: The user input, cast to the appropriate data type.
    """

    def redraw_line(user_input, cursor_pos):
        """Redraws the input line with the cursor at the correct position."""
        sys.stdout.write('\r' + ' ' * (len(user_input) + len(prompt) + 1) + '\r')
        sys.stdout.write(f'{prompt}{user_input}')
        sys.stdout.write(f'\r{prompt}{user_input[:cursor_pos]}')
        sys.stdout.flush()

    def write_char(user_input, cursor_pos, char):
        """Writes a character at the cursor position."""
        try:
            decoded_char = char.decode('cp866')
            user_input = user_input[:cursor_pos] + decoded_char + user_input[cursor_pos:]
            cursor_pos += 1
            if not invisible_input:
                redraw_line(user_input, cursor_pos)
            return user_input, cursor_pos
        except UnicodeDecodeError as e:
            return user_input, cursor_pos  # Ignore invalid characters

    # Update allowed characters based on the input type or filters
    if data_type in {'int', 'float'}:
        allowed_chars_set.update(DIGITAL_BYTES)
        allowed_chars_set.discard(b'\x20')  # Remove space
        if data_type == 'float':
            allowed_chars_set.add(b'\x2e')  # Allow '.'
        check_need = True
    else:
        check_need = any((only_ru_letters, only_en_letters, only_digitals, only_symbols))
        if check_need:
            if only_ru_letters:
                allowed_chars_set.update(RU_LETTER_BYTES)
            if only_en_letters:
                allowed_chars_set.update(EN_LETTER_BYTES)
            if only_digitals:
                allowed_chars_set.update(DIGITAL_BYTES)
            if only_symbols:
                allowed_chars_set.update(SYMBOL_BYTES)

    user_input = ''
    cursor_pos = 0
    dot_present = False

    sys.stdout.write(prompt)
    sys.stdout.flush()

    while True:
        char = msvcrt.getch()
        if char == b'\r':  # Enter
            break
        elif char == b'\x08':  # Backspace
            if cursor_pos > 0:
                if data_type == 'float' and user_input[cursor_pos - 1] == '.':
                    dot_present = False
                user_input = user_input[:cursor_pos - 1] + user_input[cursor_pos:]
                cursor_pos -= 1
                if not invisible_input:
                    redraw_line(user_input, cursor_pos)
        elif char in {b'\xe0', b'\x00'}:  # Special keys
            if msvcrt.kbhit():  # Check for the second byte
                special_key = msvcrt.getch()
                if special_key == b'K':  # Left arrow
                    if cursor_pos > 0:  # If not in the start of string
                        cursor_pos -= 1
                        if not invisible_input:
                            redraw_line(user_input, cursor_pos)
                elif special_key == b'M':  # Right arrow
                    if cursor_pos < len(user_input):  # If not in the end of string
                        cursor_pos += 1
                        if not invisible_input:
                            redraw_line(user_input, cursor_pos)
                elif special_key == b'H':  # Up arrow
                    pass  # Placeholder for future implementation
                elif special_key == b'P':  # Down arrow
                    pass  # Placeholder for future implementation
                elif special_key == b'S':  # Delete
                    if cursor_pos < len(user_input):  # If not in the end of string
                        if data_type == 'float' and user_input[cursor_pos] == '.':
                            dot_present = False
                        user_input = user_input[:cursor_pos] + user_input[cursor_pos + 1:]
                        if not invisible_input:
                            redraw_line(user_input, cursor_pos)
            else:  # If there is no second byte
                if check_need and char in allowed_chars_set:
                    user_input, cursor_pos = write_char(user_input, cursor_pos, char)
                elif not check_need:
                    user_input, cursor_pos = write_char(user_input, cursor_pos, char)
        else:
            if data_type == 'float' and char == b'\x2e':  # Check for dots
                if dot_present:
                    continue  # Ignore additional dots
                dot_present = True
            if check_need and char in allowed_chars_set:
                user_input, cursor_pos = write_char(user_input, cursor_pos, char)
            elif not check_need:
                user_input, cursor_pos = write_char(user_input, cursor_pos, char)

    sys.stdout.write(end)
    sys.stdout.flush()

    # Convert input to the specified data type
    if data_type == 'int':
        try:
            return int(user_input)
        except ValueError:
            return 0
    elif data_type == 'float':
        try:
            return float(user_input)
        except ValueError:
            return .0
    else:
        return user_input


# Example usage
if __name__ == "__main__":
    test_input = inputx('Enter floating number: ', data_type='float', invisible_input=False)
    print(type(test_input), test_input)
