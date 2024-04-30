import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


# ERRORS

# Constructor for creating error objects with position, name, and details 
class Error:
	def __init__(self, pos_start, pos_end, error_name, details):
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.error_name = error_name
		self.details = details
	
    # Generates a string representation of the error for printing 	
	def as_string(self):
		result  = f'{self.error_name}: {self.details}'
		return result

class IllegalCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
	def __init__(self, pos_start, pos_end, details=''):
		super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

# Constructor for runtime errors, including context information
class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context

	# Generates a string representation of the runtime error 
	def as_string(self):
		result  = self.generate_traceback()  # Generate the traceback
		result += f'{self.error_name}: {self.details}'
		return result

	# Generates a traceback to show the call stack leading to the error
	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx: # Traverse the context chain

			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):' + result # Basic traceback 


# POSITION

# Constructor to store position information (index, line, column, filename, file text)
class Position:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

    # Advances the position based on the current character
	def advance(self, current_char=None):
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0

		return self

    # Creates a copy of the current position object
	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


# TOKENS

TT_INT			= 'INT'
TT_FLOAT    	= 'FLOAT'
TT_INGREDIENT	= 'INGREDIENT'
TT_KEYWORD		= 'KEYWORD'
TT_PLUS     	= 'PLUS'
TT_MINUS    	= 'MINUS'
TT_MUL      	= 'MUL'
TT_DIV      	= 'DIV'
TT_EQ			= 'EQ'
TT_EOF			= 'EOF'

KEYWORDS = [
	'ingredient'
]

# Creates a copy of the current position object
class Token:
	def __init__(self, type_, value=None, pos_start=None, pos_end=None):
		self.type = type_
		self.value = value

		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()

		if pos_end:
			self.pos_end = pos_end.copy()

	# Checks if the token matches the given type and value 
	def matches(self, type_, value):
		return self.type == type_ and self.value == value
	
	# Represent how the token looks in terminal
	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'


# LEXER

# Constructor to initialize the lexer with filename and text input
class ChefLexer:
	def __init__(self, fn, text):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.advance()
	
	# Advances to the next character in the input text 
	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

 	# Generates a list of tokens from the input text
	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t':	# Ignore whitespace
				self.advance()
			elif self.current_char in DIGITS: # Handle numbers
				tokens.append(self.make_number()) 
			elif self.current_char in LETTERS: # Handle ingredients
				tokens.append(self.make_ingredient()) 
			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS, pos_start=self.pos))
				self.advance()
			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS, pos_start=self.pos))
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(TT_MUL, pos_start=self.pos))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(TT_DIV, pos_start=self.pos))
				self.advance() 
			elif self.current_char == '=':  
				tokens.append(Token(TT_EQ, pos_start=self.pos))
				self.advance() 
			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

		tokens.append(Token(TT_EOF, pos_start=self.pos)) # Append end-of-file token
		return tokens, None

	def make_number(self):
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
			num_str += self.current_char
			self.advance()

		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

	def make_ingredient(self): 
		id_str = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.advance()

		tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_INGREDIENT
		return Token(tok_type, id_str, pos_start, self.pos) 


# NODES

class NumberNode:
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return f'{self.tok}'

class IngredientAccessNode:
	def __init__(self, ingredient_name_tok): 
		self.ingredient_name_tok = ingredient_name_tok 

		self.pos_start = self.ingredient_name_tok.pos_start
		self.pos_end = self.ingredient_name_tok.pos_end

class IngredientAssignNode: 
	def __init__(self, ingredient_name_tok, value_node):
		self.ingredient_name_tok = ingredient_name_tok
		self.value_node = value_node

		self.pos_start = self.ingredient_name_tok.pos_start
		self.pos_end = self.value_node.pos_end

class BinOpNode:
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return f'({self.left_node}, {self.op_tok}, {self.right_node})'


# PARSE RESULT

# Check for errors
class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.advance_count = 0

	def register_advancement(self):
		self.advance_count += 1

	def register(self, res):
		self.advance_count += res.advance_count
		if res.error: self.error = res.error
		return res.node

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		if not self.error or self.advance_count == 0:
			self.error = error
		return self


# PARSER

class ChefParser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_idx = -1
		self.advance()

	def advance(self, ):
		self.tok_idx += 1
		if self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]
		return self.current_tok

	def parse(self):
		res = self.expr()
		# Check for errors and unexpected tokens at the end of parsing 
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '+', '-', '*' or '/'" 
			))
		return res

    # Parses basic units of expressions (numbers or ingredient access)
	def atom(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_INT, TT_FLOAT): # Number
			res.register_advancement()
			self.advance()
			return res.success(NumberNode(tok))

		elif tok.type == TT_INGREDIENT: # Ingredient access 
			res.register_advancement()
			self.advance()
			return res.success(IngredientAccessNode(tok))
		
		else: # Invalid atom 
			return res.failure(InvalidSyntaxError(
				tok.pos_start, tok.pos_end,
				"Expected int, float, identifier, '+', or '-'"
			))

	def factor(self):
		# Parses factors, which can be atoms
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS):
			return res.failure(InvalidSyntaxError(
				tok.pos_start, tok.pos_end,
				"Expected ingredient, number, '+', '-' or '*'"
			))

		return self.atom()  # Call atom directly

	def term(self):
		# Parses terms, which are factors combined with multiplication or division 
		return self.bin_op(self.factor, (TT_MUL, TT_DIV))

	def expr(self): 
		# Parses expressions, which are terms combined with addition or subtraction
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, 'ingredient'):  # Ingredient assignment 
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_INGREDIENT:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ingredient name" 
				))

			ingredient_name = self.current_tok 
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_EQ: 
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '='" 
				)) 

			res.register_advancement()
			self.advance()
			expr = res.register(self.expr()) 
			if res.error: return res
			return res.success(IngredientAssignNode(ingredient_name, expr)) 

		node = res.register(self.bin_op(self.term, (TT_PLUS, TT_MINUS))) 

		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'ingredient', number, '+', '-' or '*'"
			))

		return res.success(node)


	def bin_op(self, func_a, ops, func_b=None):
		# Helper function to parse binary operations (e.g., addition, multiplication)
		if func_b == None:
			func_b = func_a
		
		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_tok.type in ops:
			op_tok = self.current_tok
			res.register_advancement()
			self.advance()
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)


# RUNTIME RESULT

class RTResult:
	def __init__(self):
		self.value = None
		self.error = None

	def register(self, res):
		if res.error: self.error = res.error
		return res.value

	def success(self, value):
		self.value = value
		return self

	def failure(self, error):
		self.error = error
		return self


# VALUES

class Number:
	def __init__(self, value):
		self.value = value
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Division by zero',
					self.context
				)

			return Number(self.value / other.value).set_context(self.context), None

	def powed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		return str(self.value)


# CONTEXT

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None


# SYMBOL TABLE

class SymbolTable:
	def __init__(self):
		self.symbols = {}
		self.parent = None

	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]


# INTERPRETER

class Interpreter:
	# Generic visit method to dispatch to specific node type handlers 
	def visit(self, node, context):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		# Handles cases where a visit method for a specific node type is not found 
		raise Exception(f'No visit_{type(node).__name__} method defined')


	def visit_NumberNode(self, node, context):
		# Handles NumberNode by creating a Number value 
		return RTResult().success(
			Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_IngredientAccessNode(self, node, context):
		# Handles IngredientAccessNode by looking up the ingredient value in the symbol table
		res = RTResult()
		ingredient_name = node.ingredient_name_tok.value
		value = context.symbol_table.get(ingredient_name) 

		if not value:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"'{ingredient_name}' is not defined", 
				context
			))

		value = value.copy().set_pos(node.pos_start, node.pos_end) 
		return res.success(value)

	def visit_IngredientAssignNode(self, node, context): 
		# Handles IngredientAssignNode by assigning a value to an ingredient in the symbol table 
		res = RTResult()
		ingredient_name = node.ingredient_name_tok.value 
		value = res.register(self.visit(node.value_node, context))
		if res.error: return res

		context.symbol_table.set(ingredient_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		# Handles BinOpNode by performing the appropriate mathematical operation 
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if res.error: return res
		right = res.register(self.visit(node.right_node, context))
		if res.error: return res

		if node.op_tok.type == TT_PLUS:
			result, error = left.added_to(right)
		elif node.op_tok.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == TT_MUL:
			result, error = left.multed_by(right)
		elif node.op_tok.type == TT_DIV:
			result, error = left.dived_by(right)

		if error:
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.pos_start, node.pos_end))


# RUN

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

def run(fn, text):
	# Generate tokens
	lexer = ChefLexer (fn, text)
	tokens, error = lexer.make_tokens()
	if error: return None, error
	
	# Generate AST
	parser = ChefParser (tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run program
	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error
