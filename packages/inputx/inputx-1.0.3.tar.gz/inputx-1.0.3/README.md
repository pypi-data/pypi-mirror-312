# INPUTX

`inputx` is a Python module that provides an advanced input function with various validation options. It allows you to get user input in a flexible and secure way, supporting data types like `int`, `float`, and `str`, as well as restrictions on the types of characters allowed (e.g., only English letters, digits, symbols, etc.).

## Features

- **Data type validation**: Ensures input is of type `int`, `float`, or `str`.
- **Invisible input**: Can hide user input (useful for passwords).
- **Character restrictions**: Restrict input to specific sets of characters, such as:
  - Only English letters (`a-z`, `A-Z`)
  - Only Russian letters (`а-я`, `А-Я`)
  - Only digits (`0-9`)
  - Only symbols (e.g., `!@#$%^&*`)

## Supported Platforms

Currently, this module supports only **Windows** operating system, because it using `msvcrt` for capturing user input. Other platforms (e.g., Linux, macOS) are not yet supported.


## Installation

To install the package, use [GIT](https://git-scm.com/):

```
git clone https://github.com/KonstantinDigital/Inputx.git
```
Or install directly from [PyPI](https://pypi.org/project/inputx/):

```
pip install inputx

```

## USAGE
### Basic Example
```python
from inputx import inputx

# Get an integer input
age = inputx("Enter your age: ", data_type="int")
print(f"Your age is: {age}")

# Get a float input
price = inputx("Enter the price: ", data_type="float")
print(f"Price: {price}")

# Get a password (invisible input)
password = inputx("Enter your password: ", invisible_input=True)
print("Password entered successfully.")

```

### Restrictions
You can use restrictions to limit the types of characters users can enter.
```python
from inputx import inputx

# Only accept English letters
name = inputx("Enter your name: ", only_en_letters=True)

# Only accept digits and symbols
phone = inputx("Enter your phone number: ", only_digitals=True, only_symbols=True)

# Only accept symbols
symbols = inputx("Enter some symbols: ", only_symbols=True)

```
## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.
