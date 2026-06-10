import ast
import math
import tkinter as tk
from tkinter import messagebox, simpledialog


class ScientificCalculator:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title('Scientific Calculator')
        self.root.resizable(False, False)
        self.root.configure(bg='#1f1f1f')

        self.display = tk.Entry(
            root,
            font=('Arial', 24),
            justify='right',
            bd=0,
            relief='flat',
            bg='white',
            fg='black',
            insertbackground='black',
        )
        self.display.grid(row=0, column=0, columnspan=5, padx=16, pady=(16, 12), sticky='nsew')
        self.display.focus_set()

        self.buttons_frame = tk.Frame(root, bg='#1f1f1f')
        self.buttons_frame.grid(row=1, column=0, padx=16, pady=(0, 16))

        self.calculus_mode = None

        self.create_buttons()
        self.root.bind('<Return>', lambda event: self.evaluate())
        self.root.bind('<BackSpace>', lambda event: self.delete_last())
        self.root.bind('<Escape>', lambda event: self.clear())

    def create_buttons(self) -> None:
        buttons = [
            ('sin', self.insert_function), ('cos', self.insert_function), ('tan', self.insert_function), ('log', self.insert_function), ('√', self.insert_sqrt),
            ('7', self.insert_text), ('8', self.insert_text), ('9', self.insert_text), ('/', self.insert_text), ('x²', self.insert_square),
            ('4', self.insert_text), ('5', self.insert_text), ('6', self.insert_text), ('*', self.insert_text), ('x³', self.insert_cube),
            ('1', self.insert_text), ('2', self.insert_text), ('3', self.insert_text), ('-', self.insert_text), ('π', self.insert_pi),
            ('0', self.insert_text), ('.', self.insert_text), ('+', self.insert_text), ('=', self.evaluate), ('e', self.insert_e),
            ('C', self.clear), ('(', self.insert_text), (')', self.insert_text), ('%', self.insert_text), ('^', self.insert_power),
            ('Del', self.delete_last), ('ln', self.insert_function), ('abs', self.insert_function), ('1/x', self.insert_reciprocal), ('x!', self.insert_factorial),
            ('x', self.insert_text), ('diff', self.insert_diff), ('int', self.insert_int), ('A=πx²', self.insert_area_formula), ('V=4/3πx³', self.insert_volume_formula),
        ]

        for index, (label, command) in enumerate(buttons):
            row = index // 5
            column = index % 5
            button = tk.Button(
                self.buttons_frame,
                text=label,
                width=8,
                height=2,
                font=('Arial', 14),
                bd=0,
                relief='flat',
                command=lambda value=label, handler=command: handler(value),
            )

            if label in {'=', '+', '-', '*', '/', '^'}:
                button.configure(bg='orange', fg='white', activebackground='#ffb347')
            elif label in {'C', 'Del', 'diff', 'int', 'sin', 'cos', 'tan', 'log', 'ln', 'abs', '1/x', 'x!', '√', 'x²', 'x³', 'π', 'e', 'x', 'A=πx²', 'V=4/3πx³'}:
                button.configure(bg='#5c5c5c', fg='white', activebackground='#7a7a7a')
            else:
                button.configure(bg='#dddddd', fg='black', activebackground='#cfcfcf')

            button.grid(row=row, column=column, padx=4, pady=4, sticky='nsew')

    def get_display(self) -> str:
        return self.display.get().strip()

    def set_display(self, value: str) -> None:
        self.display.delete(0, tk.END)
        self.display.insert(0, value)

    def append_display(self, value: str) -> None:
        self.display.insert(tk.END, value)

    def insert_text(self, value: str) -> None:
        self.append_display(value)

    def insert_function(self, value: str) -> None:
        self.append_display(f'{value}(')

    def insert_sqrt(self, value: str) -> None:
        self.append_display('sqrt(')

    def insert_square(self, value: str) -> None:
        self.append_display('**2')

    def insert_cube(self, value: str) -> None:
        self.append_display('**3')

    def insert_pi(self, value: str) -> None:
        self.append_display('pi')

    def insert_e(self, value: str) -> None:
        self.append_display('e')

    def insert_power(self, value: str) -> None:
        self.append_display('**')

    def insert_reciprocal(self, value: str) -> None:
        self.append_display('recip(')

    def insert_factorial(self, value: str) -> None:
        self.append_display('!')

    def insert_diff(self, value: str) -> None:
        expression = simpledialog.askstring('Differentiate', 'Enter a function of x:', initialvalue='sin(x)', parent=self.root)
        if expression is None:
            return

        point = simpledialog.askstring('Differentiate', 'Enter the x-value:', initialvalue='0', parent=self.root)
        if point is None:
            return

        self.append_display(f'diff({expression},{point})')

    def insert_int(self, value: str) -> None:
        expression = simpledialog.askstring('Integrate', 'Enter a function of x:', initialvalue='sin(x)', parent=self.root)
        if expression is None:
            return

        lower = simpledialog.askstring('Integrate', 'Enter lower bound:', initialvalue='0', parent=self.root)
        if lower is None:
            return

        upper = simpledialog.askstring('Integrate', 'Enter upper bound:', initialvalue='pi', parent=self.root)
        if upper is None:
            return

        self.append_display(f'int({expression},{lower},{upper})')

    def insert_area_formula(self, value: str) -> None:
        self.append_display('pi*x**2')

    def insert_volume_formula(self, value: str) -> None:
        self.append_display('(4/3)*pi*x**3')

    def clear(self, value: str = '') -> None:
        self.set_display('')

    def delete_last(self, value: str = '') -> None:
        current = self.get_display()
        self.set_display(current[:-1])

    def evaluate(self, value: str = '') -> None:
        expression = self.get_display()
        if not expression:
            return

        try:
            result = self.evaluate_expression(expression)
            self.set_display(self.format_result(result))
        except Exception:
            messagebox.showerror('Error', 'Invalid expression')
            self.set_display('')

    def evaluate_expression(self, expression: str, x_value=None):
        expression = expression.strip()
        if not expression:
            return ''

        expression = self.resolve_advanced_functions(expression)
        expression = self.normalize_expression(expression)
        return self.safe_eval(expression, x_value)

    def resolve_advanced_functions(self, expression: str) -> str:
        resolved = expression

        while True:
            diff_index = resolved.find('diff(')
            int_index = resolved.find('int(')

            if diff_index == -1 and int_index == -1:
                break

            if diff_index != -1 and (int_index == -1 or diff_index < int_index):
                function_name = 'diff'
                function_index = diff_index
            else:
                function_name = 'int'
                function_index = int_index

            start_index = function_index + len(function_name) + 1
            arguments, end_index = self.extract_arguments(resolved, start_index)

            if function_name == 'diff' and len(arguments) == 2:
                value = self.numerical_derivative(arguments[0], arguments[1])
            elif function_name == 'int' and len(arguments) == 3:
                value = self.numerical_integral(arguments[0], arguments[1], arguments[2])
            else:
                raise ValueError('Invalid calculus function call')

            resolved = f'{resolved[:function_index]}{value}{resolved[end_index + 1:]}'

        return resolved

    def extract_arguments(self, expression: str, start_index: int):
        depth = 1
        current = ''
        arguments = []

        for index in range(start_index, len(expression)):
            character = expression[index]

            if character == '(':
                depth += 1
                current += character
            elif character == ')':
                depth -= 1
                if depth == 0:
                    arguments.append(current.strip())
                    return arguments, index
                current += character
            elif character == ',' and depth == 1:
                arguments.append(current.strip())
                current = ''
            else:
                current += character

        raise ValueError('Unmatched function call')

    def numerical_derivative(self, expression: str, point_expression: str) -> float:
        point = self.evaluate_core(point_expression, None)
        if not self.is_finite_number(point):
            return float('nan')

        delta = 1e-5
        forward = self.evaluate_core(expression, point + delta)
        backward = self.evaluate_core(expression, point - delta)
        if not self.is_finite_number(forward) or not self.is_finite_number(backward):
            return float('nan')

        return (forward - backward) / (2 * delta)

    def numerical_integral(self, expression: str, lower_expression: str, upper_expression: str) -> float:
        lower = self.evaluate_core(lower_expression, None)
        upper = self.evaluate_core(upper_expression, None)
        if not self.is_finite_number(lower) or not self.is_finite_number(upper):
            return float('nan')

        if lower == upper:
            return 0.0

        steps = 1000
        step_size = (upper - lower) / steps
        total = self.evaluate_core(expression, lower) + self.evaluate_core(expression, upper)
        if not self.is_finite_number(total):
            return float('nan')

        for index in range(1, steps):
            x = lower + index * step_size
            value = self.evaluate_core(expression, x)
            if not self.is_finite_number(value):
                return float('nan')
            total += 4 * value if index % 2 else 2 * value

        return (step_size / 3) * total

    def evaluate_core(self, expression: str, x_value):
        normalized = self.normalize_expression(expression)
        return self.safe_eval(normalized, x_value)

    def normalize_expression(self, expression: str) -> str:
        text = expression.replace('π', 'pi').replace('%', '/100')
        text = self.balance_parentheses(text)
        text = self.expand_factorials(text)
        text = self.insert_implicit_multiplication(text)
        text = text.replace('\u221a', 'sqrt')
        return text

    def balance_parentheses(self, expression: str) -> str:
        open_count = 0
        for character in expression:
            if character == '(':
                open_count += 1
            elif character == ')' and open_count > 0:
                open_count -= 1
        return expression + ')' * open_count

    def expand_factorials(self, expression: str) -> str:
        while '!' in expression:
            updated = self.replace_factorial_once(expression)
            if updated == expression:
                break
            expression = updated
        return expression

    def replace_factorial_once(self, expression: str) -> str:
        index = expression.find('!')
        if index == -1:
            return expression

        start = index - 1
        if start < 0:
            return expression

        if expression[start] == ')':
            depth = 1
            start -= 1
            while start >= 0:
                if expression[start] == ')':
                    depth += 1
                elif expression[start] == '(':
                    depth -= 1
                    if depth == 0:
                        break
                start -= 1
            if start < 0:
                return expression
            operand = expression[start:index]
        else:
            while start >= 0 and (expression[start].isalnum() or expression[start] in '._'):
                start -= 1
            operand = expression[start + 1:index]

        if not operand:
            return expression

        return f'{expression[:start + 1]}fact({operand}){expression[index + 1:]}'

    def insert_implicit_multiplication(self, expression: str) -> str:
        rules = [
            (r'(\d|\)|pi|e|x)(?=\()', r'\1*'),
            (r'(\d|\)|pi|e|x)(?=(sin|cos|tan|log|ln|sqrt|abs|recip|fact|pi|e|x))', r'\1*'),
            (r'(\))(?=\d|pi|e|x|sin|cos|tan|log|ln|sqrt|abs|recip|fact|\()', r'\1*'),
        ]

        for pattern, replacement in rules:
            expression = self.regex_substitute(pattern, replacement, expression)
        return expression

    def regex_substitute(self, pattern: str, replacement: str, text: str) -> str:
        import re
        return re.sub(pattern, replacement, text)

    def safe_eval(self, expression: str, x_value=None):
        allowed = {
            'x': x_value,
            'pi': math.pi,
            'e': math.e,
            'sin': self.sin,
            'cos': self.cos,
            'tan': self.tan,
            'log': self.log10,
            'ln': self.ln,
            'abs': self.abs_value,
            'sqrt': self.sqrt,
            'recip': self.recip,
            'fact': self.fact,
            'diff': self.diff,
            'int': self.integral,
            'Math': math,
        }

        tree = ast.parse(expression, mode='eval')
        return self.eval_ast(tree.body, allowed)

    def eval_ast(self, node, allowed):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError('Invalid constant')

        if isinstance(node, ast.Name):
            if node.id in allowed:
                return allowed[node.id]
            raise ValueError(f'Unknown name {node.id}')

        if isinstance(node, ast.BinOp):
            left = self.eval_ast(node.left, allowed)
            right = self.eval_ast(node.right, allowed)

            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
            if isinstance(node.op, ast.Mod):
                return left % right
            raise ValueError('Unsupported operator')

        if isinstance(node, ast.UnaryOp):
            value = self.eval_ast(node.operand, allowed)
            if isinstance(node.op, ast.UAdd):
                return +value
            if isinstance(node.op, ast.USub):
                return -value
            raise ValueError('Unsupported unary operator')

        if isinstance(node, ast.Call):
            function = self.eval_ast(node.func, allowed)
            args = [self.eval_ast(argument, allowed) for argument in node.args]
            return function(*args)

        if isinstance(node, ast.Attribute):
            value = self.eval_ast(node.value, allowed)
            return getattr(value, node.attr)

        raise ValueError('Unsupported expression')

    def sin(self, value):
        radians = self.to_radians(value)
        return self.normalize_near_zero(math.sin(radians))

    def cos(self, value):
        radians = self.to_radians(value)
        return self.normalize_near_zero(math.cos(radians))

    def tan(self, value):
        radians = self.to_radians(value)
        cosine = math.cos(radians)
        if abs(cosine) < 1e-12:
            return float('inf')
        return self.normalize_near_zero(math.tan(radians))

    def log10(self, value):
        if value <= 0:
            return float('nan')
        return math.log10(value)

    def ln(self, value):
        if value <= 0:
            return float('nan')
        return math.log(value)

    def abs_value(self, value):
        return abs(value)

    def sqrt(self, value):
        if value < 0:
            return float('nan')
        return math.sqrt(value)

    def recip(self, value):
        if value == 0:
            return float('inf')
        return 1 / value

    def fact(self, value):
        if int(value) != value or value < 0:
            return float('nan')
        return math.factorial(int(value))

    def diff(self, expression, point):
        delta = 1e-5
        forward = self.evaluate_expression(str(expression), float(point) + delta)
        backward = self.evaluate_expression(str(expression), float(point) - delta)
        if not self.is_finite_number(forward) or not self.is_finite_number(backward):
            return float('nan')
        return (forward - backward) / (2 * delta)

    def integral(self, expression, lower, upper):
        lower = float(lower)
        upper = float(upper)
        if lower == upper:
            return 0.0

        steps = 1000
        step_size = (upper - lower) / steps
        total = self.evaluate_expression(str(expression), lower) + self.evaluate_expression(str(expression), upper)
        if not self.is_finite_number(total):
            return float('nan')

        for index in range(1, steps):
            x_value = lower + index * step_size
            value = self.evaluate_expression(str(expression), x_value)
            if not self.is_finite_number(value):
                return float('nan')
            total += 4 * value if index % 2 else 2 * value

        return (step_size / 3) * total

    def to_radians(self, value):
        return (float(value) * math.pi) / 180

    def normalize_near_zero(self, value):
        return 0 if abs(value) < 1e-12 else value

    def format_result(self, value):
        if isinstance(value, bool):
            return str(value)
        if isinstance(value, (int, float)):
            if math.isnan(value):
                return 'Error'
            if math.isinf(value):
                return 'Infinity' if value > 0 else '-Infinity'
            if abs(value) < 1e-12:
                return '0'
            rounded = float(f'{value:.12g}')
            if abs(rounded) < 1e-12:
                return '0'
            if rounded.is_integer():
                return str(int(rounded))
            return str(rounded)
        return str(value)

    def is_finite_number(self, value):
        return isinstance(value, (int, float)) and math.isfinite(value)


if __name__ == '__main__':
    root = tk.Tk()
    ScientificCalculator(root)
    root.mainloop()
