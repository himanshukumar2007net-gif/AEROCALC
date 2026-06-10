# AEROCALC

AEROCALC is a scientific calculator project built as a Python desktop app with `tkinter`.

## Features

- Basic arithmetic: add, subtract, multiply, divide
- Scientific functions: `sin`, `cos`, `tan`, `log`, `ln`, `sqrt`, `abs`
- Constants: `pi`, `e`
- Powers and shortcuts: `x²`, `x³`, `^`, `1/x`, factorial
- Backspace and clear controls
- Degree-based trig functions
- Numerical differentiation and integration
- Formula shortcuts like area and volume expressions

## Files

- `app.py` - main Python calculator app
- `index.html` - earlier web version of the calculator
- `open-calculator.bat` - Windows launcher for the HTML version
- `LICENSE` - project license

## Requirements

- Python 3.x
- `tkinter` (usually included with Python on Windows)

## How to run

From the project folder, run:

```powershell
python app.py
```

If `python` is not recognized, install Python and make sure it is added to PATH.

## Notes

- Trig functions use degrees by default.
- `tan(90)` returns `Infinity`.
- Invalid inputs like `log(-1)` or `sqrt(-1)` display an error.

## Example expressions

- `sin(30)`
- `cos(90)`
- `diff(sin(x),0)`
- `int(sin(x),0,pi)`
- `pi*x**2`

## Author

Created and maintained by Himanshu.
