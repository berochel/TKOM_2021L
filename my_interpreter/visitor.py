import my_parser
import nodes
from my_parser.parser import Parser

import error.error_handlers as error
from lexer.types import TokenType
from my_interpreter.scope_manager import ScopeManager


class Visitor:
    def __init__(self, maxIdentLength, maxStringLength, textSource=None):
        self.parser = Parser(maxIdentLength, maxStringLength, textSource)
        self.scope_manager = ScopeManager()

    def interpret(self):
        self.parser.parse()

        for function_name, function in self.parser.functions_dict.items():
            self.scope_manager.add_function(function_name, function)

        import lib_methods as lib
        lib_dict = lib.load_lib_def()
        for lib_method_name, lib_method in lib_dict.items():
            self.scope_manager.add_lib_method(lib_method_name, lib_method)

        value = self.parser.functions_dict.get('main')
        if value:
            value.accept(self)
        else:
            raise error.MainNotDeclaredError()

        print(f'Returned {self.scope_manager.return_result}.')

    def _visit_not_operation(self, node):
        node.right.accept(self)

        self.scope_manager.last_operation_result = not self.scope_manager.last_operation_result

    def _visit_or_operation(self, node):
        node.left.accept(self)

        if self.scope_manager.last_operation_result:
            return

        node.right.accept(self)

    def _visit_and_operation(self, node):
        result = True

        node.left.accept(self)

        if not self.scope_manager.last_operation_result:
            result = False

        node.right.accept(self)

        if not self.scope_manager.last_operation_result:
            result = False

        self.scope_manager.last_operation_result = result

    def _visit_add_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result + self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_sub_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result - self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_mul_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result * self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_div_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result / self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_equal_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result == self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_not_equal_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result != self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_less_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result < self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_greater_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result > self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_less_equal_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result <= self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_greater_equal_operation(self, node):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result >= self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError()

    def _visit_function_call_operation(self, node):

        # Get function name - single word for user defined methods and functions, a list for lib functions
        name = node.name.name

        # if function is a library function - serve it here.
        if type(name) == list:
            name = self._return_var_name(node.name)
            if name in self.scope_manager.global_scope.vars_or_attrs.keys():
                lib_method_ref = self.scope_manager.get_lib_method(name)
                self._visit_lib_method_operation(lib_method_ref, node)
                return
            else:
                raise error.InvalidCall(" - Called an nonexistent library function.")

        # if function is a class constructor - initialise init.
        if name in self.parser.classes_dict.keys():
            if_object_constructor = self.parser.classes_dict[name]
            self.scope_manager.last_operation_result = if_object_constructor
            return

        # get function from global scope.
        function = self.scope_manager.get_function(name)

        # visit parameters and setup reference checking.
        arguments = []
        is_refer_list = []
        for param in node.params:
            is_refer_list.append(param.accept(self))
            arguments.append(self.scope_manager.last_operation_result)

        # check amount of parameters.
        if len(arguments) != len(function.params):
            raise error.IncorrectArgumentsNumberError()

        # check types if equal. Hard typehint.
        for argument, param in zip(arguments, function.params):
            arg1 = self._return_type_based_on_val(argument)
            arg2 = self._return_type_based_on_val(param)
            if arg1 is not arg2:
                raise error.NotTheSameTypesError()

        # switch scope and add parameters to the scope dictionary.
        self.scope_manager.switch_to_child_scope(function)
        for argument, param in zip(arguments, function.params):
            self.scope_manager.add_var_or_attr(param.name, argument)

        # visit the function instructions.
        self._visit_block(function.instructions)

        # check return value type if equal to function type. Hard typehint.
        returned_value_type = self._return_type_based_on_val(self.scope_manager.return_result)
        if function.type != returned_value_type:
            raise error.NotTheSameTypesError()

        # check if there are referable parameters, before switching the context.
        to_refer_list = []
        for refer_vars, param in zip(is_refer_list, function.params):
            if param.is_refer:
                to_refer_list.append(self.scope_manager.get_var_or_attr(param.name))
            else:
                is_refer_list.remove(refer_vars)

        # switch the context to a previous one
        self.scope_manager.switch_to_parent_scope()

        # update variables and object members which have been passed to function as references.
        for var, value in zip(is_refer_list, to_refer_list):
            if type(var) == my_parser.nodes.Variable:
                self.scope_manager.update_var_or_attr(var.name, value)

    def _visit_object_method_operation(self, node):

        # get object representing class from local scope.
        class_object = self.scope_manager.get_var_or_attr(node.parent_name)

        # get function from local scope.
        name = node.parent_name + "." + node.name[0]
        function = self.scope_manager.get_method(name)

        # visit parameters and setup reference checking.
        arguments = []
        is_refer_list = []
        for param in node.params:
            is_refer_list.append(param.accept(self))
            arguments.append(self.scope_manager.last_operation_result)

        # check amount of parameters.
        if len(arguments) != len(function.params):
            raise error.IncorrectArgumentsNumberError()

        # check types if equal. Hard typehint.
        for argument, param in zip(arguments, function.params):
            arg1 = self._return_type_based_on_val(argument)
            arg2 = self._return_type_based_on_val(param)
            if arg1 is not arg2:
                raise error.NotTheSameTypesError()

        # get method variable values from local scope before switching.
        member_vars_values = []
        for attributes in class_object.member_variables:
            name = node.parent_name + "." + attributes.name
            member_vars_values.append(self.scope_manager.get_var_or_attr(name))

        # switch scope and add parameters to the scope dictionary.
        self.scope_manager.switch_to_child_scope(function)
        for argument, param in zip(arguments, function.params):
            self.scope_manager.add_var_or_attr(param.name, argument)

        # set method variable values in new scope
        for attributes, values in zip(class_object.member_variables, member_vars_values):
            name = attributes.name
            self.scope_manager.add_var_or_attr(name, values)

        # add methods in a new scope.
        for meths in class_object.member_methods:
            self.scope_manager.add_method(meths.name, meths)

        # visit the function instructions.
        self._visit_block(function.instructions)

        # check return value type if equal to function type. Hard typehint.
        returned_value_type = self._return_type_based_on_val(self.scope_manager.return_result)
        if function.type != returned_value_type:
            raise error.NotTheSameTypesError()

        # check if there are referable parameters, before switching the context.
        to_refer_list = []
        for refer_vars, param in zip(is_refer_list, function.params):
            if param.is_refer:
                to_refer_list.append(self.scope_manager.get_var_or_attr(param.name))
            else:
                is_refer_list.remove(refer_vars)

        # get method variable values from local scope before switching.
        member_vars_values = []
        for attributes in class_object.member_variables:
            name = attributes.name
            member_vars_values.append(self.scope_manager.get_var_or_attr(name))

        # switch the context to a previous one
        self.scope_manager.switch_to_parent_scope()

        # set method variable values in parent scope
        for attributes, values in zip(class_object.member_variables, member_vars_values):
            name = node.parent_name + "." + attributes.name
            self.scope_manager.update_var_or_attr(name, values)

        # update variables and object members which have been passed to function as references.
        for var, value in zip(is_refer_list, to_refer_list):
            if type(var) == my_parser.nodes.Variable:
                self.scope_manager.update_var_or_attr(var.name, value)

    def _visit_return_stat_operation(self, node):
        node.return_value.accept(self)
        self.scope_manager.return_result = self.scope_manager.last_operation_result

    def _visit_if_else_operation(self, node):
        node.condition.accept(self)

        if self.scope_manager.last_operation_result:
            node.instructions.accept(self)
        else:
            node.else_instr.accept(self)

    def _visit_while_operation(self, node):
        node.condition.accept(self)

        i = 0
        while self.scope_manager.last_operation_result:
            self._visit_block(node.instructions)
            node.condition.accept(self)
            i += 1

    def _visit_assign_operation(self, node):

        node.right.accept(self)

        if type(self.scope_manager.last_operation_result) == my_parser.nodes.Class:
            self._visit_new_object(node)
            return

        self.scope_manager.update_var_or_attr(self._return_var_name(node.left),
                                              self.scope_manager.last_operation_result)

    def _visit_init_operation(self, node):
        name = node.name
        default_value = self._return_default_val_of_variable(node)

        if node.right is None:
            self.scope_manager.add_var_or_attr(name, default_value)
            return True

        node.right.accept(self)
        arg1 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == self._return_type_based_on_val(default_value):
            self.scope_manager.add_var_or_attr(name, self.scope_manager.last_operation_result)
            return True

        raise error.InvalidInitialisationError()

    def _visit_block(self, block):
        if isinstance(block, list):
            list_of_instructions = block
        else:
            list_of_instructions = block.instructions

        for instruction in list_of_instructions:
            if isinstance(instruction, list):
                self._visit_nested_block(instruction)
            else:
                instruction.accept(self)
            if self.scope_manager.return_result is not None:
                return

    def _visit_nested_block(self, block):

        scope = nodes.Variable("local_block")
        dict_of_variables = self.scope_manager.current_scope.vars_or_attrs.copy()

        self.scope_manager.switch_to_child_scope(scope)

        self.scope_manager.current_scope.vars_or_attrs = dict_of_variables.copy()

        for instruction in block:
            if isinstance(instruction, list):
                self._visit_nested_block(instruction)
            else:
                instruction.accept(self)
            if self.scope_manager.return_result is not None:
                return

        dict_of_variables_after_change = self.scope_manager.current_scope.vars_or_attrs.copy()

        self.scope_manager.switch_to_parent_scope()

        self.scope_manager.current_scope.vars_or_attrs = dict_of_variables.copy()

        for key, value in dict_of_variables_after_change.items():
            if key in self.scope_manager.current_scope.vars_or_attrs.keys():
                self.scope_manager.update_var_or_attr(key, value)

    def _visit_function_def_operation(self, node):
        if node.instructions is not None:
            return self._visit_block(node)

    @staticmethod
    def _return_default_val_of_variable(node):
        if node.type == TokenType.K_DOUBLE:
            return 0.0
        if node.type == TokenType.K_INTEGER:
            return 0
        if node.type == TokenType.K_STRING:
            return ""
        if node.type == TokenType.K_BOOLEAN:
            return False

    def _return_type_based_on_val(self, node):
        value = node
        if type(node) == my_parser.nodes.Integer or type(node) == my_parser.nodes.Boolean or type(
                node) == my_parser.nodes.String:
            value = node.value
        elif type(node) == my_parser.nodes.Float:
            value = node.value + node.decimalValue / 10 ** node.denominator
        elif type(node) == my_parser.nodes.Variable:
            value = self.scope_manager.get_var_or_attr(node.name)
        elif type(node) == my_parser.nodes.Parameter:
            value = self._return_default_val_of_variable(node)

        if isinstance(value, float):
            return TokenType.K_DOUBLE
        if isinstance(value, int):
            return TokenType.K_INTEGER
        if isinstance(value, str):
            return TokenType.K_STRING
        if isinstance(value, bool):
            return TokenType.K_BOOLEAN

        return TokenType.K_VOID

    @staticmethod
    def _return_var_name(node):
        if type(node) != my_parser.nodes.ObjectVariable:
            return node.name

        # return object member joint name
        temp = node.parent_name

        for name in node.name:
            temp = temp + "." + name

        return temp

    def _visit_new_object(self, node):

        class_def = self.scope_manager.last_operation_result

        self.scope_manager.add_var_or_attr(node.left.name, class_def)

        for variables in class_def.member_variables:
            name = variables.name
            variables.name = node.left.name + "." + variables.name
            self._visit_init_operation(variables)
            variables.name = name

        for meths in class_def.member_methods:
            name = node.left.name + "." + meths.name
            self.scope_manager.add_method(name, meths)

    def _visit_lib_method_operation(self, lib_method_ref, node):

        arguments = []
        for param in node.params:
            param.accept(self)
            arguments.append(self.scope_manager.last_operation_result)

        lib_method_ref(arguments)
