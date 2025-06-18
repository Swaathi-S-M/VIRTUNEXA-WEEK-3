def calculate(num1, operator, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Error: Division by zero"
            return num1 / num2
        else:
            return "Invalid operator"
    except:
        return "Invalid input"
