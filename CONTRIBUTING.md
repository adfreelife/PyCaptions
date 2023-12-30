# How to Contribute
Thank you for considering contributing! To maintain a clean and consistent code, please follow the guidelines below.

## Code style
The code should be [PEP8](https://peps.python.org/pep-0008/) complient code.

Thunder methods should be at the start of the class and at the end of docstrings.

E501 exception line length can be up to 110 characters long for a single line, if it's more follow the standard of 79 characters. Completly ignore this exception for docstrings.

For redability purposes multiline if statements should be written as follows:
- line breaks should only be before logical operators (and, or, not)
- follow standard indentation rules
- closing parenthesis should be in a new line aligned with if-statement
- ignore E124 in this case

Example:
```python
if (variable1 > variable2 or variable3
    and variable4 < variable5
):
    pass
```

You can test this using flake8 or any other tool.

## Pull Requests
- Clearly state what you've tried to accomplish, try to be short as possible
- If it's a new feature, include examples
- Check that you didn't break anything in the process

## Issues
- State what you've tried to accomplish, try to be short as possible
- If it's a bug, provide parts of code, files and results
- If possible provide a possible solution or what you think the problem is