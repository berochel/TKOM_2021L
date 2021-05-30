class Integer:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print_string = "Integer:"
        print_string += f'\n{self.value}'

        return print_string

    def accept(self, visitor):
        visitor.scope_manager.last_operation_result = self.value
        return self


class Float:
    def __init__(self, value, decimalValue, denominator):
        self.value = value
        self.decimalValue = decimalValue
        self.denominator = denominator

    def __repr__(self):
        decimal_part = self.decimalValue / 10 ** self.denominator

        print_string = "Float:"
        print_string += f'\nInteger value:{self.value}'
        print_string += f'\nDecimal value:{decimal_part}'

        return print_string

    def accept(self, visitor):
        visitor.scope_manager.last_operation_result = self.value + self.decimalValue / 10 ** self.denominator
        return self


class String:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print_string = "String:"
        print_string += f'\n{self.value}'

        return print_string

    def accept(self, visitor):
        visitor.scope_manager.last_operation_result = self.value
        return self


class Boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print_string = "Boolean:"
        print_string += f'\n{self.value}'

        return print_string

    def accept(self, visitor):
        visitor.scope_manager.last_operation_result = self.value
        return self


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        print_string = "Variable:"
        print_string += f'\n{self.name}'

        return print_string

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def accept(self, visitor):
        visitor.scope_manager.last_operation_result = visitor.scope_manager.get_var_or_attr(self.name)
        return self


class ObjectVariable:
    def __init__(self, parent_name, name):
        self.parent_name = parent_name
        self.name = name

    def __repr__(self):
        print_string = "Object Member:"
        print_string += f'\nParent name:'
        print_string += f'\n{self.parent_name}'
        print_string += f'\nName:'
        for x in self.name:
            print_string += f'\n{x}'

        return print_string

    def __eq__(self, other):
        if self.name == other.name and self.parent_name == other.parent_name:
            return True
        return False

    def accept(self, visitor):
        temp = visitor._return_var_name(self)

        visitor.scope_manager.last_operation_result = visitor.scope_manager.get_var_or_attr(temp)
        return self


class NotOperation:
    def __init__(self, right):
        self.right = right

    def __repr__(self):
        print_string = "Not:"
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_not_operation(self)

class OrOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Or:"
        print_string += f'\nLeft or operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight or operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_or_operation(self)


class AndOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "And:"
        print_string += f'\nLeft and operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight and operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_and_operation(self)


class AddOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Add:"
        print_string += f'\nLeft add operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight add operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_add_operation(self)


class SubOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Sub:"
        print_string += f'\nLeft sub operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight sub operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_sub_operation(self)


class MulOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Mul:"
        print_string += f'\nLeft mul operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight mul operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_mul_operation(self)


class DivOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Div:"
        print_string += f'\nLeft div operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight div operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_div_operation(self)


class EqualOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Equal:"
        print_string += f'\nLeft equal operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight equal operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_equal_operation(self)


class NotEqualOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Not Equal:"
        print_string += f'\nLeft not equal operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight not equal operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_not_equal_operation(self)


class LessOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Less:"
        print_string += f'\nLeft less operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight less operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_less_operation(self)


class GreaterOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Greater:"
        print_string += f'\nLeft greater operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight greater operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_greater_operation(self)


class LessEqualOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Less or Equal:"
        print_string += f'\nLeft less or equal operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight less or equal operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_less_equal_operation(self)


class GreaterEqualOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Greater or Equal:"
        print_string += f'\nLeft greater or equal operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight greater or equal operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_greater_equal_operation(self)


class Class:
    def __init__(self, name, member_variables, member_methods):
        self.name = name
        self.member_variables = member_variables
        self.member_methods = member_methods

    def __repr__(self):
        print_string = "Class:"
        print_string += f'\nName:{self.name}'
        print_string += f'\nVariables:'
        for x in self.member_variables:
            print_string += f'\n{x}'
        print_string += f'\nMethods:'
        for x in self.member_methods:
            print_string += f'\n{x}'

        return print_string


class Parameter:
    def __init__(self, par_type, name, is_refer):
        self.type = par_type
        self.name = name
        self.is_refer = is_refer

    def __repr__(self):
        print_string = "Parameter:"
        print_string += f'\nName:{self.name}'
        print_string += f'\nType:{self.type}'
        print_string += f'\nRefer:{self.is_refer}'

        return print_string

    def accept(self, visitor):
        visitor.scope_manager.last_operation_result = self
        return self.name


class FunctionDef:
    def __init__(self, type, name, params, instructions):
        self.type = type
        self.name = name
        self.params = params
        self.instructions = instructions

    def __repr__(self):
        print_string = "Function:"
        print_string += f'\nName:{self.name}'
        print_string += f'\nType:{self.type}'
        print_string += f'\nParameters:'
        for x in self.params:
            print_string += f'\n{x}'
        print_string += f'\nInstructions:'
        for x in self.instructions:
            print_string += f'\n{x}'

        return print_string

    def accept(self, visitor):
        visitor._visit_function_def_operation(self)

class FunctionCall:
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def __repr__(self):
        print_string = "Function Call:"
        print_string += f'\n{self.name}'

        if self.params:
            print_string += "\nParameters:"
            for x in self.params:
                print_string += f'\n{x}'

        return print_string

    def __eq__(self, other):
        if self.name == other.name and self.params == other.params:
            return True
        return False

    def accept(self, visitor):
        visitor._visit_function_call_operation(self)


class ObjectMethod:
    def __init__(self, parent_name, name, params):
        self.parent_name = parent_name
        self.name = name
        self.params = params

    def __repr__(self):
        print_string = "Object Method Call:"
        print_string += f'\nParent name:'
        print_string += f'\n{self.parent_name}'
        print_string += f'\nName:'
        for x in self.name:
            print_string += f'\n{x}'

        if self.params:
            print_string += "\nParameters:"
            for x in self.params:
                print_string += f'\n{x}'

        return print_string

    def __eq__(self, other):
        if self.name == other.name and self.params == other.params and self.parent_name == other.parent_name:
            return True
        return False

    def accept(self, visitor):
        visitor._visit_object_method_operation(self)


class ReturnStat:
    def __init__(self, return_value):
        self.return_value = return_value

    def __repr__(self):
        print_string = "Return statement:"
        print_string += f'\nReturn value:\n{self.return_value}'

        return print_string

    def accept(self, visitor):
        visitor._visit_return_stat_operation(self)


class IfElseStat:
    def __init__(self, condition, instructions, else_instr):
        self.condition = condition
        self.instructions = instructions
        self.else_instr = else_instr

    def __repr__(self):
        print_string = "If statement:"
        print_string += f'\nCondition:\n{self.condition}'

        print_string += f'\nInstructions:'
        for x in self.instructions:
            print_string += f'\n{x}'

        if self.else_instr:
            print_string += f'\nElse statement:'

            print_string += f'\nInstructions:'
            for x in self.else_instr:
                print_string += f'\n{x}'

        return print_string

    def accept(self, visitor):
        visitor._visit_if_else_operation(self)


class WhileStat:
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __repr__(self):
        print_string = "While statement:"
        print_string += f'\nCondition:\n{self.condition}'

        print_string += f'\nInstructions:'
        for x in self.instructions:
            print_string += f'\n{x}'

        return print_string

    def accept(self, visitor):
        visitor._visit_while_operation(self)


class AssignStat:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        print_string = "Assign:"
        print_string += f'\nLeft assign operand:'
        print_string += f'\n{self.left}'
        print_string += f'\nRight assign operand:'
        print_string += f'\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_assign_operation(self)


class InitStat:
    def __init__(self, init_type, name, right):
        self.type = init_type
        self.name = name
        self.right = right

    def __repr__(self):
        print_string = "Init statement:"
        print_string += f'\nType:\n{self.type}'
        print_string += f'\nName:\n{self.name}'

        if self.right:
            print_string += f'\nAssigned:\n{self.right}'

        return print_string

    def accept(self, visitor):
        visitor._visit_init_operation(self)


class Program:
    def __init__(self, functions_dict, classes_dict):
        self.functions_dict = functions_dict
        self.classes_dict = classes_dict

    def __repr__(self):
        print_string = "Program:"
        for key, value in self.functions_dict.items():
            print_string += f'\n{value}'
        for key, value in self.classes_dict.items():
            print_string += f'\n{value}'
        return print_string

    def accept(self, visitor):
        visitor._visit_program(self)
