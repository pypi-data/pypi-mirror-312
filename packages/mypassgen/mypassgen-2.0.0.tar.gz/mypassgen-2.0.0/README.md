# Password Generator

This Python script provides a function `generate_pass` that generates a random password with customizable length and character types.

## Features

- **Customizable Length:** Specify the desired length of the password.
- **Character Types:**
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special characters (!, @, #, etc.)

## Installation

import mypassgen

## Usage

1. Import the `generate_pass` function into your Python project.
2. Call the function with your desired parameters.

### Parameters

| Parameter  | Type    | Description                                | Default |
|------------|---------|--------------------------------------------|---------|
| `length`   | `int`   | Length of the password                    | Required |
| `uppercase`| `bool`  | Include uppercase letters (A-Z)           | `True`  |
| `lowercase`| `bool`  | Include lowercase letters (a-z)           | `True`  |
| `numbers`  | `bool`  | Include numbers (0-9)                     | `True`  |
| `special`  | `bool`  | Include special characters (!, @, #, etc.)| `False` |

### Return

- **`str`**: A randomly generated password.

## Example

```python
from mypassgen import generate_pass

# Generate a random password with all default options (length is required)
password = generate_pass(length=8,special=True,uppercase=True,lowercase=True,numbers=False)
print("Random password:", password)
