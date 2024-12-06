# dual_autodiff

The `dual_autodiff` package is a Python library designed for forward-mode automatic differentiation using dual numbers!

---

## Features

- **Core Dual Class**:
  - Represents dual numbers with real and dual parts.
  - Supports basic arithmetic operations (addition, subtraction, multiplication, division).
- **Advanced Functions**:
  - Trigonometric functions: `sin`, `cos`, `tan`.
  - Exponential and logarithmic functions: `exp`, `log`, `sqrt`.
  - Hyperbolic and inverse trigonometric functions: `sinh`, `asin`, etc.
- **Easy-to-Use API**:
  - Simple function calls for differentiation tasks.

---

## Installation

Ensure you have Python 3.9 or higher. You can install the package using `pip install -e .` from the project folder:

```bash
cd /path/to/dual_autodiff
pip install -e .
```

## Usage

Here’s a quick example of how to use the package:

```python
from dual_autodiff.dual import Dual
from dual_autodiff.functions import sin, log

# Define a dual number
x = Dual(1, 1)  # Dual number: 1 + 1ε

# Perform arithmetic operations
y = x ** 2 + 3 * x - 5

# Compute derivatives using built-in functions
result_sin = sin(x)  # sin(1) + cos(1)ε
result_log = log(x)  # ln(1) + (1 / 1)ε

# Display the results
print(y)           # Output: 1 + 5ε
print(result_sin)  # Output: sin(1) + cos(1)ε
print(result_log)  # Output: ln(1) + 1ε
```

---

## Testing

Run the test suite using `pytest` to ensure everything is working correctly:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License.  

You are free to use, modify, and distribute this software under the terms of the MIT License.  
See the `LICENCE` file for detailed information.

