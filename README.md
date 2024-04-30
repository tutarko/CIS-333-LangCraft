# Chef: A Cooking-Themed Programming Language

<img src="code chef.png" width="200">

## Names of Members
Arthur Kondratyuk

## Language Overview

Chef is a programming language designed to introduce programming concepts using familiar cooking terminology and actions.\
By drawing analogies between cooking and coding, Chef aims to make programming more accessible and engaging for beginners. 

## Example Code Snippet

```python
# SOUP RECIPE

# Prepare the ingredients
ingredient broth = 8 cups 
ingredient vegetables = ["carrots", "celery", "onions"]
ingredient protein = "chicken"

# Prepare vegetables 
recipe chop_vegetables(vegetables): 
    chopped_vegetables = []
    for vegetable in vegetables:
        chopped_vegetables.append(chop(vegetable))
    return chopped_vegetables 

prepped_vegetables = chop_vegetables(vegetables) 

# Combine and simmer
pot = combine(broth, prepped_vegetables, protein)
simmer(pot, ftime=30 minutes) 

# Serve
serve(pot)
```

## Instructions

### Prerequisites:

*   **Python 3.x:** Ensure you have Python 3.x installed on your system.  

### Running Chef Code:

1.  **Download:** Download the `chef.py` and `cook_book.py` files from this repository. 
2.  **Open Terminal:** Navigate to the directory where you saved the files using the terminal or command prompt.
3.  **Run Interpreter:** Type `python cook_book.py` and press Enter.  
4.  **Enter Code:** You can now type your Chef code line by line and press Enter to execute it.  

## Syntax Table

| Type        | Example               | Description                                   |
|---|---|---| 
| INGREDIENT  | flour, eggs, sugar   | Names of ingredients (variables)              |
| INT         | 2, 10, 50             | Integer numbers                               | 
| FLOAT       | 1.5, 3.14            | Floating-point numbers                        |
| KEYWORD     | ingredient           | Reserved keyword for variable declaration    |
| EQUALS      | =                     | Assignment operator                           | 
| PLUS        | +                     | Addition operator                             |
| MINUS       | -                     | Subtraction operator                          |
| MUL         | *                     | Multiplication operator                       |
| DIV         | /                     | Division operator                             | 
| EOF         | (end of input)        | Indicates the end of the input code          |

## Valid Grammar Statements

*   Mathematical expressions: `2 + 3`, `6 - 1`, `4 * 5`, `10 / 2`
*   Ingredient (variable) assignment: `ingredient flour = 2`
*   Ingredient assignment with expression: `ingredient sugar = 1 + 2`
*   Ingredient combination: ingredient mixture = `ingredient cookie_dough = dry_ingredients + wet_ingredients`
*   Recipe (function) definition: `recipe make_cake(flour, sugar, eggs)`: ... (not yet implemented)
*   Recipe call: cake = `make_cake(2 cups, 1 cup, 3)` (not yet implemented)
*   Control flow (if): `if is_mixed(batter): pour(batter, into=pan)` (not yet implemented)
*   Control flow (while): `while not is_baked(cake): wait(5 minutes)` (not yet implemented)
*   For loop: `for each cookie in batch: decorate(cookie)` (not yet implemented)

## State of the Language

### Working:

*   **Lexer:**  The lexer correctly identifies and tokenizes integers, floats, ingredient names, the assignment operator, and basic mathematical operators.
*   **Parser:** The parser can parse ingredient assignment statements and mathematical expressions, generating an AST. 
*   **Interpreter:** The interpreter can execute ingredient assignments, storing values in a symbol table, and evaluate basic mathematical expressions.

### Not Working (Future Development):

*   **Units of Measurement:**  The language does not currently handle units (e.g., "cups", "grams") for ingredient quantities.
*   **More Complex Expressions:**  The parser and interpreter are limited to handling basic mathematical expressions and do not support parentheses or operator precedence.
*   **Multiple-Line Statements:** Currently, the language only supports single-line statements. Implementing a mechanism to handle multi-line statements or code blocks would enhance usability and allow for more complex recipes. 
*   **Control Flow and Functions:**  The language does not yet include control flow statements (e.g., if-else, loops) or functions (recipes) for more complex logic.
