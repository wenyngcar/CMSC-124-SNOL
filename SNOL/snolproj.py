import re

# Check if the value can be converted to an integer
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Check if the value can be converted to a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# main class to handle SNOL commands
class SNOLInterpreter:
    def __init__(self):
        self.variables = {}  # Stores variables and their values
    
    def execute_command(self, command):
        # Strip the command of leading/trailing whitespace and handle exit commands
        command = command.strip()
        if command == "EXIT!" or command.lower() == "exit":
            print("Interpreter is now terminated...")
            return False

        # Handles BEG command for creating variables
        if command.startswith("BEG "):
            var = command[4:].strip()
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', var):
                print(f"Unknown variable [{var}]")
            else:
                input_value = input(f"SNOL> Please enter value for [{var}]: ")
                if is_integer(input_value):
                    self.variables[var] = int(input_value)
                elif is_float(input_value):
                    self.variables[var] = float(input_value)
                else:
                    print("Invalid number format")
        
        # handles PRINT command to print variable values or expressions
        elif command.startswith("PRINT "):
            expr = command[6:].strip()
            value = self.evaluate_expression(expr)
            if isinstance(value, str):
                print(value)
            else:
                print(f"SNOL> [{expr}] = {value}")
        else:
            # Evaluate and execute other expressions or commands
            result = self.evaluate_expression(command)
            if isinstance(result, str):
                print(result)
            elif result is not None:
                print(f"SNOL> {result}")

        return True

    def evaluate_expression(self, expr):
        # Check if the expression is a variable name
        if expr in self.variables:
            return self.variables[expr]
        
        # Check for assignment operation
        if "=" in expr:
            var, val_expr = expr.split("=", 1)
            var = var.strip()
            val_expr = val_expr.strip()
            value = self.evaluate_expression(val_expr)
            if isinstance(value, str):
                return value
            self.variables[var] = value
            return
        
        # Check for arithmetic operations
        tokens = re.split(r'(\+|\-|\*|\/|\%)', expr)
        if len(tokens) > 1:
            tokens = [token.strip() for token in tokens if token.strip()]
            if len(tokens) % 2 == 0:
                return "Unknown command! Does not match any valid command of the language."

            result = self.evaluate_expression(tokens[0])
            if isinstance(result, str):
                return result
            
            i = 1
            while i < len(tokens):
                operator = tokens[i]
                next_val = self.evaluate_expression(tokens[i+1])
                if isinstance(next_val, str):
                    return next_val
                
                if (isinstance(result, float) and isinstance(next_val, int)) or (isinstance(result, int) and isinstance(next_val, float)):
                    return "Error! Operands must be of the same type in an arithmetic operation!"

                if operator == '+':
                    result += next_val
                elif operator == '-':
                    result -= next_val
                elif operator == '*':
                    result *= next_val
                elif operator == '/':
                    result /= next_val
                elif operator == '%':
                    if isinstance(result, float) or isinstance(next_val, float):
                        return "Modulo operation not allowed with floating-point numbers."
                    result %= next_val
                i += 2
            return result

        # Check if the expression is an integer
        if re.match(r'^[-]?[0-9]+$', expr):
            return int(expr)
        # Check if the expression is a float
        if re.match(r'^[-]?[0-9]+\.[0-9]+$', expr):
            return float(expr)

        # Return an error if the expression is not recognized
        return "Undefined variable or invalid number [" + expr + "]"

# Function to start the SNOL interpreter
def run_snol_interpreter():
    print("The SNOL environment is now active, you may proceed with giving your commands.")
    interpreter = SNOLInterpreter()
    while True:
        command = input("Command: ")
        if not interpreter.execute_command(command):
            break

# Start the SNOL interpreter
run_snol_interpreter()
