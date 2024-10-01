import google.generativeai as genai
import ast
import json
from PIL import Image
from constants import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_image(img: Image, dict_of_vars: dict):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    dict_of_vars_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
        f"You are an advanced problem solver tasked with analyzing an image containing mathematical expressions, equations, graphical problems, or abstract concepts. Your job is to identify the problem and solve it according to the type of expression found in the image. "
        f"Your priority is to follow the PEMDAS rule when solving mathematical expressions. PEMDAS stands for: Parentheses, Exponents, Multiplication and Division (left to right), Addition and Subtraction (left to right). For equations, correctly substitute variables using the provided dictionary, solve for unknowns, and return the result. "
        f"Here are the types of problems you may encounter in the image, and instructions on how to handle each: \n"
        
        f"1. **Simple Mathematical Expressions**: These are expressions like 2 + 2, 3 * 4, 5 / 6, 7 - 8, etc. Evaluate the expression and return the result in this format: \n"
        f"    [{{'expr': 'given expression', 'result': calculated_answer}}] \n"
        
        f"2. **Single or Multiple Equations**: These could be equations like x^2 + 2x + 1 = 0, or systems like 3y + 4x = 0, 5x^2 + 6y + 7 = 12. Solve for the unknown variables. If there are multiple variables, solve each and return a list of dictionaries like this: \n"
        f"    [{{'expr': 'x', 'result': solution_for_x, 'assign': True}}, {{'expr': 'y', 'result': solution_for_y, 'assign': True}}] \n"
        f"    If only one variable exists, return it in the same format with 'assign' set to True. \n"
        
        f"3. **Variable Assignment**: When the expression involves assigning values to variables, like x = 4, y = 5, z = 6, recognize the assignment and store these values. Return the result in this format: \n"
        f"    [{{'expr': 'variable', 'result': value, 'assign': True}}] \n"
        
        f"4. **Graphical Math Problems**: These are problems involving a scenario represented as a drawing, such as cars colliding, trigonometric problems, or diagrams of geometric shapes. Carefully analyze the drawing and any accompanying information (e.g., labels, colors, measurements), then solve the problem. Return the result in this format: \n"
        f"    [{{'expr': 'problem description', 'result': calculated answer}}] \n"
        
        f"5. **Abstract Concepts in Drawings**: Sometimes a drawing might represent a concept such as love, war, jealousy, or patriotism. Analyze the abstract concept shown and explain it. Return the result in this format: \n"
        f"    [{{'expr': 'concept explanation', 'result': abstract concept}}] \n"
        
        f"**Special Notes for Handling Variables**: \n"
        f"If the image contains variables that match any in the provided dictionary of user-assigned variables ({dict_of_vars_str}), substitute those variables with their actual values before solving the expression. Ensure to check the dictionary for these values before proceeding with the calculation. \n"
        
        f"**Variable Substitution Example**: \n"
        f"    If the image shows the expression 'x + 2' and the dictionary contains {{'x': 3}}, replace 'x' with 3 and solve the expression as '3 + 2'. Return the result as: \n"
        f"    [{{'expr': 'x + 2', 'result': 5, 'assign': False}}] \n"
        
        f"Ensure all keys and values are properly quoted to allow for easy parsing using Python's ast.literal_eval. Provide a clear and concise result for each type of problem identified in the image."

        f"Ensure that the result is clearly formatted with spaces between words."

    )
    response = model.generate_content([prompt, img])
    print(response.text)
    print("Raw response:", response.text)
    answers = []
    try:
        answers = ast.literal_eval(response.text)
    except Exception as e:
        print(f"Error in parsing response from Gemini API: {e}")
    print('returned answer ', answers)
    for answer in answers:
        if 'assign' in answer:
            answer['assign'] = True
        else:
            answer['assign'] = False
    return answers