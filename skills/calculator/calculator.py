import sys
import ast

def safe_eval(expression: str) -> str:
    """Tính toán biểu thức toán học an toàn, không dùng eval() trực tiếp."""
    try:
        # Parse thành AST trước để kiểm tra an toàn
        tree = ast.parse(expression, mode="eval")
        
        # Chỉ cho phép các node toán học, chặn code độc hại
        allowed = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
            ast.FloorDiv, ast.USub, ast.UAdd
        )
        for node in ast.walk(tree):
            if not isinstance(node, allowed):
                return f"Error: '{expression}' contains unsafe operations"
        
        result = eval(compile(tree, "<string>", "eval"))
        return str(result)
    
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return f"Error: Could not parse '{expression}'"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Nhận expression từ command line argument
    if len(sys.argv) < 2:
        print("Error: No expression provided")
        sys.exit(1)
    
    expression = sys.argv[1]
    print(safe_eval(expression))