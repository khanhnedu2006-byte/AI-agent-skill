---
name: calculator
description: Use this skill when the user asks to compute math expressions, do arithmetic, or evaluate numerical formulas.
---

# Calculator

When the user asks a math question:
1. Extract the math expression from their query
2. Evaluate it using Python's eval()
3. Return the result in a friendly sentence

## Supported operations
- Basic: +, -, *, /
- Power: ** (ví dụ: 2**10)
- Parentheses: (2 + 3) * 4

## Edge cases to handle
- Nếu không tách được biểu thức → hỏi lại user
- Không tính các biểu thức có chữ cái lạ (tránh eval() bị inject)

## Examples
- User: "What's 25 * 4 + 10?" → "25 * 4 + 10 equals 110."
- User: "Calculate 2 to the power of 8" → extract "2**8" → "2**8 equals 256."
- User: "Area of circle radius 5" → extract "3.14159 * 5**2" → "The area is approximately 78.54."