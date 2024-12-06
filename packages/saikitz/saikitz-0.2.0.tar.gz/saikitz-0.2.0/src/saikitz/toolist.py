import math

def calutions(a, b = None, operator = "+") :
    match operator :
        case "+" :
            if b is None :
                return a
            else :
                return a + b
        case "-" :
            if b is None :
                return -a
            else :
                return a - b
        case "*" :
            if b is None :
                return a * a
            else :
                return a * b
        case "/" :
            if b is None :
                raise ValueError("Can't divide by zero")
            else :
                return a / b
        case "^"|"**"|"power"|"pow" :
            if b is None :
                return math.e ** a
            else :
                return a ** b
        case "sqrt"|"square_root" :
            if b is None :
                return math.sqrt(a)
            else :
                return a ** (1/b)
        case "log" :
            if b is None :
                return math.log(a)
            else :
                return math.log(a, b)
        case "sin" :
            if b is None :
                return math.sin(a)
            else :
                raise ValueError("Too many arguments")
        case "cos" :
            if b is None :
                return math.cos(a)
            else :
                raise ValueError("Too many arguments")
        case "tan" :
            if b is None :
                return math.tan(a)
            else :
                raise ValueError("Too many arguments")
        case ">" :
            if b is None :
                raise ValueError("Too few arguments")
            else :
                return a > b
        case "<" :
            if b is None :
                raise ValueError("Too few arguments")
            else :
                return a < b
        case "="|"==" :
            if b is None :
                raise ValueError("Too few arguments")
            else :
                return a == b
        case "!=" :
            if b is None :
                raise ValueError("Too few arguments")
            else :
                return a != b
        case ">=" :
            if b is None :
                raise ValueError("Too few arguments")
            else :
                return a >= b
        case "<=" :
            if b is None :
                raise ValueError("Too few arguments")
            else :
                return a <= b
        case _ :
            raise ValueError("Invalid operator")

cal_info = {
    "type": "function",
    "function": {
        "name": "calutions",
        "description": "一个综合计算器",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                     "type": "float",
                     "description": "The city and state, e.g., San Francisco, CA"
                     },
                "b": {
                     "type": "float",
                     "description": "The city and state, e.g., San Francisco, CA"
                     },
                "operator": {
                    "type": "string",
                    "enum": ["+", "-", "*", "/", "^", "sqrt", "log", "sin", "cos", "tan", ">", "<", "="],
                    "description": "The temperature unit to use. Infer this from the user's location."
                    }
            },
            "required": ["location", "unit"]
        }
    }
}