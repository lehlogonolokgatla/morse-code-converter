# morse_logic.py
# This file contains the core Morse Code conversion logic.

# --- Morse Code Dictionary ---
# --- Morse Code Dictionary (Extended) ---
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.','%': '.-.-.-.-'
}


# Create a reverse dictionary for Morse to Text conversion for efficient lookups
REVERSE_MORSE_CODE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

# --- ASCII Art for the program ---
# We'll keep this here, but it won't be used in the GUI.
# It can still be part of your original CLI version if you keep it.
MORSE_ART = """
 ______             _              ___           _
|  ____|           | |            / _ \         | |
| |__   ___  _ __  | |_  ___  ___| (_) | ___  ___| | __
|  __| / _ \| '_ \ | __|/ _ \/ __|> _ < / _ \/ __| |/ /
| |___| (_) | | | || |_| (_) \__ \  _ <|  __/\__ \   <
|______\___/|_| |_| \__|\___/|___/_/ \_\\\___||___/_|\_\

          ...---...  ...---...  ...---...
"""
# ---------------------------------

def text_to_morse(text):
    """
    Converts a given text string into Morse Code.

    Args:
        text (str): The input string to be converted.

    Returns:
        tuple: A tuple containing (converted Morse Code string, boolean indicating success, optional warning)
               or (error message, False, None) if input is empty or contains unsupported characters.
    """
    if not text:
        return "Input cannot be empty. Please enter some text to convert.", False, None

    morse_code_output = []
    text_processed = text.upper()
    unconvertible_chars_found = False
    unsupported_chars_warning = ""

    for char in text_processed:
        if char == ' ':
            morse_code_output.append('   ')
        elif char in MORSE_CODE_DICT:
            morse_code_output.append(MORSE_CODE_DICT[char] + ' ')
        else:
            morse_code_output.append(f"[UNSUPPORTED_CHAR:{char}] ")
            unconvertible_chars_found = True

    final_morse = "".join(morse_code_output).strip()

    if unconvertible_chars_found:
        unsupported_chars_warning = "Warning: Some characters could not be converted to Morse Code. Unsupported characters are marked as '[UNSUPPORTED_CHAR:X]' in the output."

    return final_morse, True, unsupported_chars_warning


def morse_to_text(morse_code):
    """
    Converts a Morse Code string back into human-readable text.

    Args:
        morse_code (str): The Morse Code string to be converted.
                          Individual character codes should be separated by a single space.
                          Word breaks should be indicated by three spaces.

    Returns:
        tuple: A tuple containing (converted text string, boolean indicating success, optional warning)
               or (error message, False, None) if input is empty or contains invalid Morse code.
    """
    if not morse_code:
        return "Input cannot be empty. Please enter some Morse code to convert.", False, None

    words_morse = morse_code.strip().split('   ')
    decoded_text = []
    invalid_morse_found = False
    unknown_morse_warning = ""

    for word_morse in words_morse:
        characters_morse = word_morse.split(' ')
        decoded_word_chars = []
        for char_morse in characters_morse:
            if not char_morse:
                continue
            if char_morse in REVERSE_MORSE_CODE_DICT:
                decoded_word_chars.append(REVERSE_MORSE_CODE_DICT[char_morse])
            else:
                decoded_word_chars.append(f"[UNKNOWN_MORSE:{char_morse}]")
                invalid_morse_found = True
        decoded_text.append("".join(decoded_word_chars))
        decoded_text.append(" ")

    final_text = "".join(decoded_text).strip()

    if invalid_morse_found:
        unknown_morse_warning = "Warning: Some Morse code sequences could not be converted to text. Unknown sequences are marked as '[UNKNOWN_MORSE:CODE]' in the output."

    return final_text, True, unknown_morse_warning

def save_conversion(original_text, converted_result, conversion_type):
    """
    Saves the original text and its conversion to a text file.

    Args:
        original_text (str): The input text or Morse code provided by the user.
        converted_result (str): The output Morse code or text.
        conversion_type (str): 'text_to_morse' or 'morse_to_text' to describe the conversion.
    """
    filename = "morse_conversions.txt"
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write("----------------------------------------\n")
            file.write(f"Conversion Type: {conversion_type.replace('_', ' ').title()}\n")
            file.write(f"Original: {original_text}\n")
            file.write(f"Converted: {converted_result}\n")
            file.write("----------------------------------------\n\n")
        return True, f"Conversion successfully saved to '{filename}'."
    except IOError as e:
        return False, f"Error saving conversion to file: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred while saving: {e}"

# The main() function from your original script is no longer needed here,
# as the GUI will handle the user interaction.
if __name__ == "__main__":
    # This block can be used for simple testing of the logic functions if needed.
    print("This is the morse_logic.py file. It contains the core conversion functions.")
    print("Run app_gui.py to use the GUI application.")
    morse, success, warning = text_to_morse("Hello World!")
    if success:
        print(f"Test Text to Morse: {morse}")
        if warning: print(warning)
    else:
        print(f"Error: {morse}")

    text, success, warning = morse_to_text(".... . .-.. .-.. ---   .-- --- .-. .-.. -..")
    if success:
        print(f"Test Morse to Text: {text}")
        if warning: print(warning)
    else:
        print(f"Error: {text}")