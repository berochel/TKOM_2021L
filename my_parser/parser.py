import my_parser.nodes as nodes

from error.error_handlers import ParserError
from lexer.lexer import LexerMain
from lexer.types import TokenType, parameter_types, function_types


class Parser:
    def __init__(self, maxIdentLength, maxStringLength, textSource=None):
        self.lexer = LexerMain(maxIdentLength, maxStringLength, textSource)
        self.current_token = self.lexer.get_token()
        self.functions_dict = {}
        self.classes_dict = {}

    def parse(self):
        if not self._next_token(TokenType.LEFT_BRACKET):
            return None

        while self._parse_function_definition() or self._parse_class_definition():
            pass

        if not self._next_token(TokenType.RIGHT_BRACKET):
            raise ParserError(self.current_token.value, self.current_token.end, "Program not ended with \'}\'.")

        if self.current_token.type != TokenType.EOT:
            raise ParserError(self.current_token.value, self.current_token.end,
                              "Unexpected data after program definition.")

        return nodes.Program(self.functions_dict, self.classes_dict)

    def _parse_function_definition(self):

        func_type = self._parse_function_type()
        if not func_type:
            return None

        name = self.current_token.value

        self._next_token(TokenType.VALUE_ID)

        if self.functions_dict and name in self.functions_dict.keys():
            raise ParserError(self.current_token.value, self.current_token.start, " - Function redefinition.")

        function = self._parse_rest_of_function_definition(func_type, name)

        self.functions_dict[name] = function

        return function

    def _parse_parameters_definitions(self):
        params = []

        param = self._parse_parameter_definition()
        if param:
            params.append(param)

        while self.current_token.type == TokenType.COMMA:
            self._next_token(TokenType.COMMA)
            param = self._parse_parameter_definition()
            if param:
                params.append(param)
            else:
                raise ParserError(self.current_token.value, self.current_token.start, "Couldn't find next parameter "
                                                                                      "definition.")

        return params

    def _parse_parameter_definition(self):

        par_type = self._parse_parameter_type()
        if not par_type:
            return None

        is_refer = False

        if self.current_token.type == TokenType.MUL_OR_REFER:
            self._next_token(TokenType.MUL_OR_REFER)
            is_refer = True

        name = self.current_token.value

        self._next_token(TokenType.VALUE_ID)

        return nodes.Parameter(par_type, name, is_refer)

    def _parse_class_definition(self):
        if self.current_token.type != TokenType.K_CLASS:
            return None

        self._next_token(TokenType.K_CLASS)
        name = self.current_token.value
        self._next_token(TokenType.VALUE_ID)

        if self.classes_dict and (name in self.classes_dict.keys()):
            raise ParserError(self.current_token.value, self.current_token.start, " - Class redefinition.")

        self._next_token(TokenType.LEFT_BRACKET)

        return self._parse_rest_of_class_definition(name)

    def _parse_rest_of_class_definition(self, name):

        member_methods = []
        member_variables = []

        while self._parse_init_statement_or_function_definition(member_methods, member_variables):
            pass

        self._next_token(TokenType.RIGHT_BRACKET)
        classdef = {name: nodes.Class(name, member_variables, member_methods)}
        self.classes_dict.update(classdef)

        return classdef

    def _parse_init_statement_or_function_definition(self, member_methods, member_variables):
        member_type = self._parse_function_type()
        if not member_type:
            return False

        name = self.current_token.value

        self._next_token(TokenType.VALUE_ID)

        if self.current_token.type == TokenType.LEFT_PARENT:
            member = self._parse_rest_of_function_definition(member_type, name)
            member_methods.append(member)
            return True

        member = self._parse_rest_of_init_statement(member_type, name)
        self._next_token(TokenType.SEMICOLON)
        member_variables.append(member)

        return True

    def _parse_rest_of_function_definition(self, member_type, name):

        self._next_token(TokenType.LEFT_PARENT)

        params = self._parse_parameters_definitions()

        self._next_token(TokenType.RIGHT_PARENT)

        instructions = self._parse_block()

        if not instructions:
            raise ParserError(self.current_token.value, self.current_token.start, " Function is empty.")

        function = nodes.FunctionDef(member_type, name, params, instructions)

        return function

    def _parse_rest_of_init_statement(self, member_type, name):

        assignable = None
        if self.current_token.type == TokenType.ASSIGN_OP:
            self._next_token(TokenType.ASSIGN_OP)
            assignable = self._parse_assignable()

        return nodes.InitStat(member_type, name, assignable)

    def _parse_block(self):
        if self.current_token.type != TokenType.LEFT_BRACKET:
            return None

        self._next_token(TokenType.LEFT_BRACKET)

        instructions = []
        instruction = self._parse_block_instruction()

        while instruction:
            instructions.append(instruction)
            instruction = self._parse_block_instruction()

        self._next_token(TokenType.RIGHT_BRACKET)

        return instructions

    def _parse_block_instruction(self):

        instruction = self._parse_statement()
        if instruction:
            return instruction

        instruction = self._parse_assign_or_function_call()
        if instruction:
            self._next_token(TokenType.SEMICOLON)
            return instruction

        instruction = self._parse_block()
        if instruction:
            return instruction

        return None

    def _parse_statement(self):

        instruction = self._parse_if()
        if instruction:
            return instruction
        instruction = self._parse_while()
        if instruction:
            return instruction
        instruction = self._parse_return()
        if instruction:
            return instruction
        instruction = self._parse_init()
        if instruction:
            return instruction

        return None

    def _parse_assign_or_function_call(self):
        if self.current_token.type != TokenType.VALUE_ID:
            return None

        name = self.current_token.value
        self._next_token(TokenType.VALUE_ID)

        object_name = []

        while self.current_token.type == TokenType.DOT:
            self._next_token(TokenType.DOT)
            object_name.append(self.current_token.value)
            self._next_token(TokenType.VALUE_ID)

        instruction = self._parse_rest_of_function_call(name, object_name)
        if instruction:
            return instruction
        instruction = self._parse_rest_of_assign(name, object_name)
        if instruction:
            return instruction

        self._next_token(TokenType.SEMICOLON)

        raise ParserError(self.current_token.value, self.current_token.end,
                          "Unexpected data instead of function call or assignment statement.")

    def _parse_if(self):
        if self.current_token.type != TokenType.K_IF:
            return None

        self._next_token(TokenType.K_IF)
        self._next_token(TokenType.LEFT_PARENT)

        condition = self._parse_condition()
        if condition is None:
            raise ...
        self._next_token(TokenType.RIGHT_PARENT)

        instructions = self._parse_block()

        else_instr = []
        if self.current_token.type == TokenType.K_ELSE:
            self._next_token(TokenType.K_ELSE)
            else_instr = self._parse_block()

        return nodes.IfElseStat(condition, instructions, else_instr)

    def _parse_while(self):
        if self.current_token.type != TokenType.K_WHILE:
            return None

        self._next_token(TokenType.K_WHILE)
        self._next_token(TokenType.LEFT_PARENT)

        condition = self._parse_condition()
        if condition is None:
            raise ParserError(self.current_token.value, self.current_token.end,
                              "Couldn't find a valid while condition.")

        self._next_token(TokenType.RIGHT_PARENT)

        instructions = self._parse_block()
        if instructions is None:
            raise ParserError(self.current_token.value, self.current_token.end, "Couldn't parse while statement block.")

        return nodes.WhileStat(condition, instructions)

    def _parse_return(self):
        if self.current_token.type != TokenType.K_RETURN:
            return None

        self._next_token(TokenType.K_RETURN)

        return_value = self._parse_assignable()

        self._next_token(TokenType.SEMICOLON)

        return nodes.ReturnStat(return_value)

    def _parse_assignable(self):

        expr = self._parse_condition()
        if expr:
            return expr

        return None

    def _parse_function_call(self):
        if self.current_token.type != TokenType.VALUE_ID:
            return None

        name = self.current_token.value

        return self._parse_rest_of_function_call(name, None)

    def _parse_rest_of_assign(self, name, object_name):
        self._next_token(TokenType.ASSIGN_OP)

        assignable = self._parse_assignable()

        if object_name:
            name = nodes.ObjectVariable(name, object_name)
        else:
            name = nodes.Variable(name)

        return nodes.AssignStat(name, assignable)

    def _parse_rest_of_function_call(self, name, object_name):
        if self.current_token.type != TokenType.LEFT_PARENT:
            return None

        self._next_token(TokenType.LEFT_PARENT)

        arguments = []
        argument = self._parse_assignable()

        if argument:
            arguments.append(argument)
            while self.current_token.type == TokenType.COMMA:
                self._next_token(TokenType.COMMA)
                arguments.append(self._parse_assignable())
                if not argument:
                    raise ParserError

        self._next_token(TokenType.RIGHT_PARENT)

        if object_name:
            name = nodes.ObjectVariable(name, object_name)
        else:
            name = nodes.Variable(name)

        return nodes.FunctionCall(name, arguments)

    def _parse_init(self):
        var_type = self._parse_parameter_type()
        if not var_type:
            return None

        name = self.current_token.value
        self._next_token(TokenType.VALUE_ID)

        assignable = self._parse_rest_of_init_statement(var_type, name)

        self._next_token(TokenType.SEMICOLON)

        return assignable

    def _parse_condition(self):
        left = self._parse_and_condition()
        if not left:
            return None

        while self.current_token.type == TokenType.VERTICAL_LINE:
            operator = self.current_token.type
            self._next_token(operator)

            right = self._parse_and_condition()
            if not right:
                raise ParserError(self.current_token.value, self.current_token.end,
                                  "Couldn't find right operand of or operation.")

            left = nodes.OrOperation(left, right)

        return left

    def _parse_and_condition(self):

        left = self._parse_equality_condition()
        if not left:
            return None

        while self.current_token.type == TokenType.AMPERSAND:
            operator = self.current_token.type
            self._next_token(operator)

            right = self._parse_equality_condition()
            if not right:
                raise ParserError(self.current_token.value, self.current_token.end,
                                  "Couldn't find right operand of and operation.")

            left = nodes.AndOperation(left, right)

        return left

    def _parse_equality_condition(self):

        left = self._parse_relation_condition()
        if not left:
            return None

        if self.current_token.type in [TokenType.EQUAL, TokenType.NOT_EQUAL]:
            operator = self.current_token.type
            self._next_token(operator)

            right = self._parse_relation_condition()
            if not right:
                raise ParserError(self.current_token.value, self.current_token.end,
                                  "Couldn't find right operand of equality operation.")

            if operator == TokenType.EQUAL:
                left = nodes.EqualOperation(left, right)
            else:
                left = nodes.NotEqualOperation(left, right)

        return left

    def _parse_relation_condition(self):
        expression = self._parse_boolean_value()
        if expression:
            return expression

        is_negated = False
        if self.current_token.type == TokenType.EXCLAMATION:
            is_negated = True
            self._next_token(TokenType.EXCLAMATION)

        left = self._parse_expression()
        if not left:
            if is_negated:
                raise ParserError(self.current_token.value, self.current_token.end, "Exclamation mark left without any "
                                                                                    "negable expression.")
            return None

        if self.is_a_relation_operation(TokenType.LESS_EQUAL):
            right = self._parse_rest_of_relation_condition()
            left = nodes.LessEqualOperation(left, right)
        elif self.is_a_relation_operation(TokenType.GREATER_EQUAL):
            self._next_token()
            right = self._parse_expression()
            left = nodes.GreaterEqualOperation(left, right)
        elif self.is_a_relation_operation(TokenType.LESS):
            self._next_token()
            right = self._parse_expression()
            left = nodes.LessOperation(left, right)
        elif self.is_a_relation_operation(TokenType.GREATER):
            self._next_token()
            right = self._parse_expression()
            left = nodes.GreaterOperation(left, right)

        if is_negated:
            left = nodes.NotOperation(left)

        return left

    def _parse_rest_of_relation_condition(self):
        self._next_token()
        right = self._parse_expression()
        if right:
            raise ParserError(self.current_token.value, self.current_token.end,
                              "Unable to parse second operand of relation condition.")

    def _parse_expression(self):

        left = self._parse_multiply_expression()
        if not left:
            return None

        while self.current_token.type in [TokenType.PLUS_OR_CONC, TokenType.MINUS]:
            operator = self.current_token.type
            self._next_token(operator)

            right = self._parse_multiply_expression()
            if not right:
                raise ParserError(self.current_token.value, self.current_token.end,
                                  "Couldn't find right operand of add operation.")

            if operator == TokenType.PLUS_OR_CONC:
                left = nodes.AddOperation(left, right)
            else:
                left = nodes.SubOperation(left, right)

        return left

    def _parse_multiply_expression(self):

        left = self._parse_primary_expression()
        if not left:
            return None

        while self.current_token.type in [TokenType.MUL_OR_REFER, TokenType.DIV]:
            operator = self.current_token.type
            self._next_token(operator)

            right = self._parse_primary_expression()
            if not right:
                raise ParserError(self.current_token.value, self.current_token.end,
                                  "Couldn't find right operand of mul operation.")

            if operator == TokenType.MUL_OR_REFER:
                left = nodes.MulOperation(left, right)
            else:
                left = nodes.DivOperation(left, right)

        return left

    def _parse_primary_expression(self):

        expression = self._parse_integer_value()
        if expression:
            return expression
        expression = self._parse_double_value()
        if expression:
            return expression
        expression = self._parse_string_value()
        if expression:
            return expression
        expression = self._parse_parenth_expression()
        if expression:
            return expression
        expression = self._parse_variable_or_method()
        if expression:
            return expression

        return None

    def _parse_boolean_value(self):

        value = None

        if self.current_token.type == TokenType.K_TRUE:
            value = "true"
        if self.current_token.type == TokenType.K_FALSE:
            value = "false"

        if value:
            self._next_token()
            return nodes.Boolean(value)

        return None

    def _parse_integer_value(self):

        if self.current_token.type == TokenType.VALUE_INT:
            value = self.current_token.value
            self._next_token(TokenType.VALUE_INT)
            return nodes.Integer(value)

        return None

    def _parse_double_value(self):

        if self.current_token.type == TokenType.VALUE_DOUBLE:
            value = self.current_token.value
            decimal_value = self.current_token.decimalValue
            denominator = self.current_token.denominator
            self._next_token(TokenType.VALUE_DOUBLE)
            return nodes.Float(value, decimal_value, denominator)

        return None

    def _parse_string_value(self):

        if self.current_token.type == TokenType.VALUE_STRING:
            value = self.current_token.value
            self._next_token(TokenType.VALUE_STRING)
            return nodes.String(value)

        return None

    def _parse_parenth_expression(self):

        if self.current_token.type != TokenType.LEFT_PARENT:
            return None

        self._next_token(TokenType.LEFT_PARENT)
        condition = self._parse_condition()
        self._next_token(TokenType.RIGHT_PARENT)
        if condition:
            return condition

        raise ParserError(self.current_token.value, self.current_token.end, "Couldn't parse parentheses.")

    def _parse_variable_or_method(self):

        if self.current_token.type != TokenType.VALUE_ID:
            return None

        name = self.current_token.value
        self._next_token(TokenType.VALUE_ID)

        object_name = []
        while self.current_token.type == TokenType.DOT:
            self._next_token(TokenType.DOT)
            object_name.append(self.current_token.value)
            self._next_token(TokenType.VALUE_ID)

        expression = self._parse_rest_of_function_call(name, object_name)
        if expression:
            if object_name:
                return nodes.ObjectMethod(name, object_name, expression.params)
            return expression

        if object_name:
            return nodes.ObjectVariable(name, object_name)
        return nodes.Variable(name)

    def _next_token(self, token_type=None):
        if not token_type or token_type == self.current_token.type:
            self.current_token = self.lexer.get_token()
            return True

        raise ParserError(self.current_token, self.current_token.start,
                          f'Expected:{token_type}, got:{self.current_token}')

    def is_a_relation_operation(self, operator):
        return self.current_token.type == operator

    def _parse_function_type(self):
        if self.current_token.type not in function_types:
            return None

        fun_type = self.current_token.type
        self._next_token(self.current_token.type)

        return fun_type

    def _parse_parameter_type(self):
        if self.current_token.type not in parameter_types:
            return None

        par_type = self.current_token.type
        self._next_token(self.current_token.type)

        return par_type

    @staticmethod
    def is_token_relation_operator(token):
        if token in [TokenType.LESS,
                     TokenType.LESS_EQUAL,
                     TokenType.GREATER,
                     TokenType.GREATER_EQUAL]:
            return True

        return False
