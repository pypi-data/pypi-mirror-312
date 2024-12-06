import random
import string

def generate_pass(length: int, uppercase: bool = True, lowercase: bool = True, numbers: bool = True, special: bool = False) -> str:
    """
    Generate a random password with the specified length and character types.
    
    :param length: The length of the password to generate
    :param uppercase: Include uppercase letters in the password
    :param lowercase: Include lowercase letters in the password
    :param numbers: Include numbers in the password
    :param special: Include special characters in the password
    :return: A random password with the specified length and character types
    """
    # Define the character sets to use
    characters = ""
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if numbers:
        characters += string.digits
    if special:
        characters += string.punctuation

    # Generate the ID
    return "".join(random.choice(characters) for _ in range(length))
    

   