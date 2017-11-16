import re
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from collections import *
import copy
"""
	LOLCode Interpreter Class
"""
class Interpreter(QtCore.QObject):
		class Lexeme: # constructor for lexeme
				def __init__(self, regex, type):
						self.regex = regex
						self.type = type
		"""
			Lexemes Definitions
				Lexemes are defined in the Interpreter class.
				Each lexeme contains a regex expression
				and a list of labels that correspond to
				the groups in the regex exression.
		"""
		LEXEMES = [
				#Start and end delimiters of source code
				Lexeme(r"(HAI)[ \t]*",
						["Code Starting Delimiter"]),
				Lexeme(r"(KTHXBYE)",
						["Code Ending Delimiter"]),
				#Input and Output
				Lexeme(r"(GIMMEH)[ \t]+",
						["Input"]),
				Lexeme(r"(VISIBLE)[ \t]+",
						["Output"]),
				#Variable Declaration and Assignment
				Lexeme(r"(I[ \t]+HAS[ \t]+A)[ \t]+",
						["Variable Declaration"]),
				Lexeme(r"(ITZ)[ \t]+",
						["Declaration Assignment"]),
				Lexeme(r"(R)[ \t]+",
						["Value Assignment"]),
				#Arithmetic Operations
				Lexeme(r"(SUM[ \t]+OF)[ \t]+",
						["Addition"]),
				Lexeme(r"(DIFF[ \t]+OF)[ \t]+",
						["Subtraction"]),
				Lexeme(r"(PRODUKT[ \t]+OF)[ \t]+",
						["Multiplication"]),
				Lexeme(r"(QUOSHUNT[ \t]+OF)[ \t]+",
						["Division"]),
				Lexeme(r"(MOD[ \t]+OF)[ \t]+",
						["Modulo"]),
				Lexeme(r"(BIGGR[ \t]+OF)[ \t]+",
						["Maximum"]),
				Lexeme(r"(SMALLR[ \t]+OF)[ \t]+",
						["Minimum"]),
				#Boolean Operations
				Lexeme(r"(BOTH[ \t]+OF)[ \t]+",
						["AND Operator"]),
				Lexeme(r"(EITHER[ \t]+OF)[ \t]+",
						["OR Operator"]),
				Lexeme(r"(WON[ \t]+OF)[ \t]+",
						["XOR Operator"]),
				Lexeme(r"(NOT)[ \t]+",
						["NOT Operator"]),
				Lexeme(r"(BOTH[ \t]+SAEM)[ \t]+",
						["Equal Operator"]),
				Lexeme(r"(DIFFRINT)[ \t]+",
						["Not Equal Operator"]),
				#Boolean Arity Operations
				Lexeme(r"(ALL[ \t]+OF)[ \t]+",
						["Infinite Arity AND Operator"]),
				Lexeme(r"(ANY[ \t]+OF)[ \t]+",
						["Infinite Arity OR Operator"]),
				Lexeme(r"(SMOOSH)[ \t]+",
						["Infinite Arity Concatenation"]),
				Lexeme(r"(MKAY)[ \t]*",
						["Infinite Arity Terminator"]),
				#changed + to * in number of white spaces
				Lexeme(r"(IS NOW A)[ \t]+",
						["Type Cast Keyword"]),
				Lexeme(r"(MAEK)[ \t]+",
						["Type Cast Keyword 2"]),
				Lexeme(r"(A)[ \t]+",
						["A Delimiter"]),
				#Connector
				Lexeme(r"(AN)[ \t]+",
						["Connector"]),
				#Conditional Statements
				Lexeme(r"(O[ \t]+RLY\?)[ \t]*",
						["If Else Statement Init"]),
				Lexeme(r"(YA[ \t]+RLY)[ \t]*",
						["If Statement"]),
				Lexeme(r"(NO[ \t]+WAI)[ \t]*",
						["Else Statement"]),
				Lexeme(r"(MEBBE)[ \t]+",
						["Else If Statement"]),
				Lexeme(r"(WTF\?)[ \t]*",
						["Switch Statement Init"]),
				Lexeme(r"(OMG)[ \t]+",
						["Switch Statement Conditions"]),
				Lexeme(r"(OMGWTF)[ \t]*",
						["Switch Statement Default Condition"]),
				Lexeme(r"(GTFO)[ \t]*",
						["Case Terminator"]),
				Lexeme(r"(OIC)[ \t]*",
						["Conditional Statement Terminator"]),
				Lexeme(r"(BTW)[ \t]+([^\n]*)",
						["Single Line Comment Init", "Comment"]),
				Lexeme(r"(OBTW)\s*([\s\S]*)\s+(TLDR)[ \t]*",
						["Multiline Comment Init", "Comment", "Multiline Comment Terminator"]),
				#Loop Statement
				Lexeme(r"(IM IN YR)[ \t]+([a-zA-Z][a-zA-Z0-9_]*)[ \t]+",
						["Loop Init", "Loop Name"]),
				Lexeme(r"(UPPIN|NERFIN)[ \t]+(YR)[ \t]+",
						["Loop Operation", "Loop YR Delimiter"]),
				Lexeme(r"(TIL|WILE)",
								["Loop Condition Delimiter"]),
				Lexeme(r"(IM OUTTA YR)[ \t]+([a-zA-Z][a-zA-Z0-9_]*)[ \t]*",
						["Loop Terminate", "Loop Name"]),
				#Data Types
				Lexeme("(\")([^\"]*)(\")",
						["String Starting Delimiter", "YARN", "String Ending Delimiter"]),
				Lexeme(r"(NOOB|TROOF|NUMBAR|NUMBR|YARN)[ \t]*",
						["Data Type"]),
				Lexeme(r"(WIN|FAIL)(?=[\s]+)",
						["TROOF"]),
				Lexeme(r"([a-zA-Z][a-zA-Z0-9_]*)[ \t]*",
						["Variable Name"]),
				Lexeme(r"(-?\d+\.\d*)[ \t]*",
						["NUMBAR"]),
				Lexeme(r"(-?\d+)[ \t]*",
						["NUMBR"]),
				#Other Characters
				Lexeme(r"(!)[ \t]*",
						["New Line Suppressor"]),
				Lexeme(r"(\n)",
						["New Line"]),
				Lexeme(r"(,)\s*",
						["Soft Line Break"])
		]

		sourceCode = deque([])

		"""
			Combined Regex expression
				Each regex expression is joined using OR symbol in tokenizer.
		"""
		tokenizer = re.compile("|".join([lexeme.regex for lexeme in LEXEMES]))
		"""
			Types/labels
				A list of labels for group in the combined regex expression
		"""
		types = sum([lexeme.type for lexeme in LEXEMES], [])
		def __init__(self, inp, gui):
				super(self.__class__, self).__init__(None)
				self.gui = gui
				self.inp = inp # source code entered by user/ read from file
				self.lex_table = []
				self.sym_table = {}

		"""
			Lexer
				Generates a lexical table from the input source code
		"""
		def make_lex_table(self):
				self.lex_table = []
				for match in self.tokenizer.finditer(self.inp):
						cnt = len(match.groups()) - match.groups().count(None)
						for i in range(match.lastindex-cnt,match.lastindex):
								key = match.group(i+1)
								type1 = self.types[i]
								if key in [None]: continue
								if type1 not in ["YARN", "Comment", "New Line"]: key = " ".join(key.split())
								self.lex_table.append((key, type1))

		"""
			Prefix Expression Evaluator
		"""
		def eval(self):
				# lol types	
				lol_types = ["TROOF", "YARN", "NUMBR", "NUMBAR"]
				# python types allowed in operations
				arithmetic_types = [float, int]
				bool_types = [bool]
				equality_types = [str, float, bool, int]
				is_bool         = lambda x : x[1] == "TROOF"
				is_float        = lambda x : x[1] == "NUMBAR"
				is_integer      = lambda x : x[1] == "NUMBR"
				is_connector    = lambda x : x[1] == "Connector"
				is_string       = lambda x : x[1] == "YARN"
				is_mkay         = lambda x : x[0] == "MKAY"
				is_operand      = lambda x : is_float(x) or is_integer(x) or is_string(x) or is_bool(x)
				is_binary_op    = lambda x : x[0] in op["binary"]["arithmetic"] or x[0] in op["binary"]["logical"] or x[0] in op["binary"]["equality"]
				is_infinite_op  = lambda x : x[0] in op["infinite"]
				is_unary_op     = lambda x : x[0] in op["unary"]
				is_operator     = lambda x : is_binary_op(x) or is_infinite_op(x) or is_unary_op(x) or x[0] == "MAEK"
				is_lol_type			= lambda x : x[0] in lol_types

				def to_string(s):
						if type(s) == bool:
								if s == True:
										return "WIN"
								else:
										return "FAIL"
						else:
								return str(s)

				def to_bool(s):
						if type(s) == bool:
								return s
						else:
								return True

				def isfloat(s):
						try:
								t = float(s)
								return True
						except:
								return False

				def to_arithmetic(s, t = None):
						if type(s) == str:
								if s.isnumeric():
										return int(s)
								elif isfloat(s):
										return float(s)
								else:
										None
						elif type(s) == int or type(s) == float:
								return s
						elif type(s) == bool:
								return int(s)
				uncast_type = {
					int   : lambda x: (str(x), "NUMBR"),
					float : lambda x: (str(x), "NUMBAR"),
					bool  : lambda x: ({ True : "WIN", False : "FAIL" } [x], "TROOF"),
					str   : lambda x: (str(x), "YARN"),
				}

				cast_type = {
					"NUMBR"  :        int,
					"NUMBAR" :        float,
					"TROOF"  :        lambda x: { "WIN" : True, "FAIL" : False } [x],
					"YARN": str
				}

				uncast  = lambda x: uncast_type[type(x)](x)
				cast    = lambda x: cast_type[x[1]](x[0])

				op = {
						# Binary operations
						"binary" : {
								"arithmetic" : {
										'SUM OF'     : lambda x,y : x + y,
										'PRODUKT OF' : lambda x,y : x * y,
										'QUOSHUNT OF': lambda x,y : x / y,
										'DIFF OF'    : lambda x,y : x - y,
										'MOD OF'     : lambda x,y : x % y,
										'BIGGR OF'   : lambda x,y : max(x,y),
										'SMALLR OF'  : lambda x,y : min(x,y)
								},
								"equality" : {
										'BOTH SAEM'  : lambda x,y : x == y,
										'DIFFRINT'   : lambda x,y : x != y
								},
								"logical" : {
										'BOTH OF'    : lambda x,y : x and y,
										'EITHER OF'  : lambda x,y : x or y,
										'WON OF'     : lambda x,y : (x or y) and (x != y)
								}
						},
						# Infinite Arity Operatons
						"infinite"  : {
							'SMOOSH' :     lambda *a: "".join(map(str,a)),
							'ALL OF'     : lambda *a: all(map(bool,a)),
							'ANY OF'     : lambda *a: any(map(bool,a))
						},
						"unary" : {
							'NOT'        : lambda x: not x
						}
				}

				if not is_operator(self.sourceCode[0]):
						if self.sourceCode[0][1] == 'Variable Name': #literals
								key = self.sourceCode.popleft()[0]
								return (self.getVarValue(key), self.getVarType(key)) # variable name
						else:
								return self.sourceCode.popleft()
				else:
						stack = []
						while not (len(stack) == 1 and is_operand(stack[0])):
								token = self.sourceCode.popleft()
								if token[1] == "Variable Name": stack.append((self.getVarValue(token[0]), self.getVarType(token[0])))
								else: stack.append(token)

								def is_binary_operation():
									if len(stack) >= 4 and is_operand(stack[-3]) and is_operand(stack[-1]) and is_connector(stack[-2]) and is_binary_op(stack[-4]):
										opc = stack[-4][0]
										op1 = cast(stack[-3])
										op2 = cast(stack[-1])
										if opc in op["binary"]["arithmetic"]:
											if type(op1) not in arithmetic_types: op1 = to_arithmetic(op1)
											if type(op2) not in arithmetic_types: op2 = to_arithmetic(op2)
											res = op["binary"]["arithmetic"][opc](op1, op2)
										elif opc in op["binary"]["equality"]:
											res = op["binary"]["equality"][opc](op1, op2)
										elif opc in op["binary"]["logical"]:
											if type(op1) not in bool_types: op1 = to_bool(op1)
											if type(op2) not in bool_types: op2 = to_bool(op2)
											res = op["binary"]["logical"][opc](op1, op2)
										for i in range(4): stack.pop()
										return uncast(res)
									elif len(stack) >= 3 and is_operand(stack[-2]) and is_operand(stack[-1]) and is_binary_op(stack[-3]):
										opc = stack[-3][0]
										op1 = cast(stack[-2])
										op2 = cast(stack[-1])
										if opc in op["binary"]["arithmetic"]:
											if type(op1) not in arithmetic_types: op1 = to_arithmetic(op1)
											if type(op2) not in arithmetic_types: op2 = to_arithmetic(op2)
											res = op["binary"]["arithmetic"][opc](op1, op2)
										elif opc in op["binary"]["equality"]:
											res = op["binary"]["equality"][opc](op1, op2)
										elif opc in op["binary"]["logical"]:
											if type(op1) not in bool_types: op1 = to_bool(op1)
											if type(op2) not in bool_types: op2 = to_bool(op2)
											res = op["binary"]["logical"][opc](op1, op2)
										for i in range(3): stack.pop()
										return uncast(res)
									else:
										return False
								def is_infinite_operation():
									operands = []
									to_pop = 0
									if len(stack) >= 3 and is_mkay(stack[-1]):
										to_pop += 1   # will pop mkay
										i = len(stack) - 2
										while i > 0 and is_operand(stack[i]):
											operands.append(cast(stack[i]))
											to_pop += 1 # will pop operand
											if is_connector(stack[i-1]):
												to_pop += 1 # will pop connector
												i -= 2
											elif is_infinite_op(stack[i-1]):
												to_pop += 1 # pop operator
												operands.reverse()
												res = op["infinite"][stack[i-1][0]](*operands)
												for i in range(to_pop): stack.pop()
												return uncast(res)
											else:
												i -= 1
									elif len(stack) >= 2 and self.sourceCode[0][0] in ['\n', ','] and not is_operand(self.sourceCode[0]) and not is_connector(self.sourceCode[0]):
											i = len(stack) - 1
											while i > 0 and is_operand(stack[i]):
												operands.append(cast(stack[i]))
												to_pop += 1 # will pop operand
												if is_connector(stack[i-1]):
													to_pop += 1 # will pop connector
													i -= 2
												elif is_infinite_op(stack[i-1]):
													to_pop += 1 # pop operator
													operands.reverse()
													res = op["infinite"][stack[i-1][0]](*operands)
													for i in range(to_pop): stack.pop()
													return uncast(res)
												else:
													i -= 1
									return False

								def is_maek_operation():
									if len(stack) >= 4 and stack[-4][0] == "MAEK" and stack[-2][0] == "A" and is_lol_type(stack[-1]):
										exp = cast(stack[-3])
										if stack[-1][0] == "TROOF":
											exp = to_bool(exp)
										elif stack[-1][0] == "YARN":
											exp = to_string(exp)
										elif stack[-1][0] == "NUMBR" or stack[-1][0] == "NUMBAR":
											exp = cast_type[stack[-1][0]](exp)
										else:
											return False
										for i in range(4): stack.pop()
										return uncast(exp)

								def is_unary_operation():
									if len(stack) >= 2 and is_unary_op(stack[-2]) and is_operand(stack[-1]):
										res = op["unary"][stack[-2][0]](cast(stack[-1]));
										for i in range(2): stack.pop()
										return uncast(res)
									else:
										return False

								while True:
										valid = is_unary_operation()
										if not valid: valid = is_binary_operation()
										if not valid: valid = is_infinite_operation()
										if not valid: valid = is_maek_operation()
										if valid:
											stack.append(valid)
										else:
											break

						return stack[0]

		"""
			String Parser
				interprets special characters in the string
		"""
		def parse_string(self, s):
			return s.replace(":)","\n").replace(":>",	"\t").replace(":o",	"\g").replace(":\"", "\"").replace("::",	":")

		"""
			VISIBLE statement
		"""
		def output_decl(self): #print(anything)
				printText = ''
				while self.sourceCode[0][0] not in ['\n', ',', '!']: printText = printText + self.parse_string(str(self.eval()[0]))
				if self.sourceCode[0][0] == '!': self.sourceCode.popleft() #pop bang sign
				else: printText = printText + '\n'
				self.gui.printConsole(printText)

		"""
			GIMMEH statement
		"""
		def input_decl(self):
				key = self.sourceCode.popleft()[0]
				self.addSymbol(key, "NOOB", None)
				if self.sourceCode[0][0] == "ITZ":
						self.sourceCode.popleft() #pops the ITZ keyword
						value, type = self.eval()
						self.addSymbol(key, value, type)

		"""
			<var> R <expression>
		"""
		def assignment(self):
				# get varname
				varname = self.sourceCode.popleft()[0]
				# pop R
				self.sourceCode.popleft()[0]
				# eval expression and assign result
				value, type = self.eval()
				self.addSymbol(varname, value, type)

		"""
			Input from GUI
				Calls the GUI to get user input
		"""
		def user_input(self):
				varname = self.sourceCode.popleft()[0]
				value, type = self.gui.showDialog(), "YARN"
				self.gui.printConsole('LOL>> Enter Input: ' + value + '\n')
				self.addSymbol(varname, value, type)

		"""
			OMGWTF statement
		"""
		def switch_case(self):
				while self.sourceCode[0][0] in ['\n', ',']: self.sourceCode.popleft() #pops newline or comma
				while self.sourceCode[0][0] != 'OIC':
						if self.sourceCode.popleft()[0] == 'OMGWTF': #pops OMG or OMGWTF
								self.sourceCode.popleft() #pop newline or comma
								while self.sourceCode[0][0] != 'OIC':self.execute_keywords()
						else:
								key, type = self.eval()
								self.sourceCode.popleft()
								if key == self.getVarValue('IT'):
										while self.sourceCode[0][0] not in ['OMG', 'OMGWTF', 'GTFO', 'OIC']:
												self.execute_keywords()
										while self.sourceCode[0][0] not in ['GTFO', 'OIC']:

												if self.sourceCode[0][0] in ['OMG', 'OMGWTF']:
														while self.sourceCode[0][0] not in ['\n', ',']: self.sourceCode.popleft()
														self.sourceCode.popleft()
												if self.sourceCode[0][0] not in ['OMG', 'OMGWTF', 'OIC']: self.execute_keywords()
										break
								else:
										while self.sourceCode[0][0] not in ['OMG', 'OMGWTF', 'OIC']: self.sourceCode.popleft()
				while self.sourceCode[0][0] != 'OIC': self.sourceCode.popleft()
				self.sourceCode.popleft() #pops OIC

		"""
			O RLY? statment
		"""
		def if_else(self):
				while self.sourceCode[0][0] in ['\n', ',']: self.sourceCode.popleft() #pop newline or comma
				while self.sourceCode[0][0] != 'OIC':
						key = self.sourceCode.popleft()[0]
						if key == 'MEBBE': self.execute_keywords()  #pop YA RLY/NO WAI/MEBBE , if MEBBE assign to IT
						else: self.sourceCode.popleft() #pop newline or comma
						if key == 'NO WAI':             # It reached the else statement
								while self.sourceCode[0][0] != 'OIC': self.execute_keywords()
						elif self.getVarValue('IT') == 'WIN': # checks if the value of IT is true
								while self.sourceCode[0][0] not in ['NO WAI', 'MEBBE', 'OIC']: self.execute_keywords()
								while self.sourceCode[0][0] != 'OIC': self.sourceCode.popleft()
						else:
								while self.sourceCode[0][0] not in ['NO WAI', 'MEBBE', 'OIC']: self.sourceCode.popleft()

				self.sourceCode.popleft() # pop oic

		"""
			Loop Code Block
		"""
		def loop(self):
				loop_name = self.sourceCode.popleft()[0]
				if self.sourceCode[0][0] in ['UPPIN', 'NERFIN']:
					loop_operation = self.sourceCode.popleft()[0]
					self.sourceCode.popleft() # pop YR
					loop_variable = self.sourceCode.popleft()[0]  # pop variable
					loop_condition = self.sourceCode.popleft()[0] # wile or til
				else:
					loop_operation = None

				loop_body = deque([])
				while not (self.sourceCode[0][0] == 'IM OUTTA YR' and self.sourceCode[1][0] ==  loop_name):
						loop_body.appendleft(self.sourceCode.popleft()) # loop body creation

				while True:
					self.sourceCode.extendleft(copy.deepcopy(loop_body))
					if loop_operation != None:
						x = self.eval()
						if loop_condition == "WILE" and x[0] == 'FAIL':
							break
						elif loop_condition == "TIL" and x[0] == 'WIN':
							break
					while not (self.sourceCode[0][0] == 'IM OUTTA YR' and self.sourceCode[1][0] == loop_name):
						self.execute_keywords()
					if loop_operation == "UPPIN":
						self.addSymbol(loop_variable, int(self.getVarValue(loop_variable)) + 1, "NUMBR")
					elif loop_operation == "NERFIN":
						self.addSymbol(loop_variable, int(self.getVarValue(loop_variable)) - 1, "NUMBR")
				while not (self.sourceCode[0][0] == 'IM OUTTA YR' and self.sourceCode[1][0] == loop_name):
					self.sourceCode.popleft()

		def type_cast(self):
			def to_string(s):
					if type(s) == bool:
							if s == True:
									return "WIN"
							else:
									return "FAIL"
					else:
							return str(s)

			def to_bool(s):
					if type(s) == bool:
							return s
					else:
							return True

			def isfloat(s):
					try:
							t = float(s)
							return True
					except:
							return False

			def to_arithmetic(s, t = None):
					if type(s) == str:
							if s.isnumeric():
									return int(s)
							elif isfloat(s):
									return float(s)
							else:
									None
					elif type(s) == int or type(s) == float:
							return s
					elif type(s) == bool:
							return int(s)
			uncast_type = {
				int   : lambda x: (str(x), "NUMBR"),
				float : lambda x: (str(x), "NUMBAR"),
				bool  : lambda x: ({ True : "WIN", False : "FAIL" } [x], "TROOF"),
				str   : lambda x: (str(x), "YARN"),
			}

			cast_type = {
				"NUMBR"  :        int,
				"NUMBAR" :        float,
				"TROOF"  :        lambda x: { "WIN" : True, "FAIL" : False } [x],
				"YARN": str
			}

			uncast  = lambda x: uncast_type[type(x)](x)
			cast    = lambda x: cast_type[x[1]](x[0])
			
			varname = self.sourceCode.popleft()[0]
			self.sourceCode.popleft() # pop IS NOW A
			vartype = self.sourceCode.popleft()[0] # pop data type
			exp = cast((self.getVarValue(varname), self.getVarType(varname)))
			if vartype == "TROOF":
				exp = to_bool(exp)
			elif vartype == "YARN":
				exp = to_string(exp)
			elif vartype == "NUMBR" or vartype == "NUMBAR":
				exp = cast_type[vartype](exp)
			self.addSymbol(varname, *uncast(exp))



		"""
			Mapping of statement_name to coressponding function
		"""
		keywords = {
				'VISIBLE'   : output_decl,
				'I HAS A'   : input_decl,
				'GIMMEH'    : user_input,
				'WTF?'      : switch_case,
				'O RLY?'    : if_else,
				'IM IN YR'  : loop
		}

		"""
			Code Block
				handles execution of code block
		"""
		def execute_keywords(self):
				if self.sourceCode[0][0] in  ['\n', ',']:
						None
				elif self.sourceCode[0][0] in self.keywords.keys():
						self.keywords[self.sourceCode.popleft()[0]](self)
				elif self.sourceCode[0][0] in self.sym_table.keys() and self.sourceCode[1][0] == 'R':
						self.assignment()
				elif self.sourceCode[0][0] in self.sym_table.keys() and self.sourceCode[1][0] == 'IS NOW A':
						self.type_cast()
				else: #assignment of value to IT
						value, type = self.eval()
						self.addSymbol('IT', value, type)
				self.sourceCode.popleft() #pop newline or comma

		"""
			Execution begins here
		"""
		def run_program(self):
				comments = ["Single Line Comment Init", "Comment","Multiline Comment Init", "Comment", "Multiline Comment Terminator", "String Starting Delimiter", "String Ending Delimiter"]
				self.sourceCode = deque(filter(lambda tup: tup[1] not in comments, self.lex_table)) # to allow popleft()
				while self.sourceCode[0][0] != 'HAI': self.sourceCode.popleft()
				self.sourceCode.popleft()               #pops the keyword HAI
				self.sourceCode.popleft()               #pops new line
				while self.sourceCode[0][0] != 'KTHXBYE':
						if self.sourceCode[0][0] not in ['\n', ',']: self.execute_keywords()
						else: self.sourceCode.popleft()
				
		"""
			Symbol Table Getter/Setters
		"""
		def addSymbol(self, varname, value, type):
				self.sym_table[varname] = (value, type)
				self.gui.updateSymbolTable()

		def getVarValue(self, varname):
				return self.sym_table[varname][0]

		def getVarType(self, varname):
				return self.sym_table[varname][1]
