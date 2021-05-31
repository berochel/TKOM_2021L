import my_parser
import nodes

import error.error_handlers as error
from lexer.types import TokenType
from my_interpreter.scope_manager import ScopeManager


class Interpreter:
    def __init__(self, visitor, lib):
        self.visitor = visitor
        self.lib = lib
        self.return_val = None

    def interpret(self):
        lib_dict = self.lib.load_lib_def()

        self.visitor.visit_program(lib_dict)
        self.return_val = self.visitor.scope_manager.return_result


class Visitor:
    def __init__(self, tree: nodes.Program):
        self.tree = tree
        self.scope_manager = ScopeManager()

    def visit_program(self, lib_dict):

        for function_name, function in self.tree.functions_dict.items():
            self.scope_manager.add_function(function_name, function)

        for lib_method_name, lib_method in lib_dict.items():
            self.scope_manager.add_lib_method(lib_method_name, lib_method)

        value = self.tree.functions_dict.get('main')
        if value:
            value.accept(self)
        else:
            raise error.MainNotDeclaredError(f'Main function is not declared.')

    def _visit_not_operation(self, node: nodes.NotOperation):
        node.right.accept(self)

        self.scope_manager.last_operation_result = not self.scope_manager.last_operation_result

    def _visit_or_operation(self, node: nodes.OrOperation):
        node.left.accept(self)

        if self.scope_manager.last_operation_result:
            return

        node.right.accept(self)

    def _visit_and_operation(self, node: nodes.AndOperation):
        result = True

        node.left.accept(self)

        if not self.scope_manager.last_operation_result:
            result = False

        node.right.accept(self)

        if not self.scope_manager.last_operation_result:
            result = False

        self.scope_manager.last_operation_result = result

    def _visit_add_operation(self, node: nodes.AddOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result + self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_sub_operation(self, node: nodes.SubOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result - self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_mul_operation(self, node: nodes.MulOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result * self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_div_operation(self, node: nodes.DivOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if self.scope_manager.last_operation_result == 0:
            raise error.ZeroDivisionError(f'Unexpected: {node}')

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result / self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_equal_operation(self, node: nodes.EqualOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result == self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_not_equal_operation(self, node: nodes.NotEqualOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result != self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_less_operation(self, node: nodes.LessOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result < self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_greater_operation(self, node: nodes.GreaterOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result > self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_less_equal_operation(self, node: nodes.LessEqualOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result <= self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_greater_equal_operation(self, node: nodes.GreaterEqualOperation):
        node.left.accept(self)
        result = self.scope_manager.last_operation_result
        arg1 = self._return_type_based_on_val(result)

        node.right.accept(self)
        arg2 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == arg2:
            self.scope_manager.last_operation_result = result >= self.scope_manager.last_operation_result
            return self.scope_manager.last_operation_result

        raise error.NotTheSameTypesError(f'Unexpected: {node}')

    def _visit_function_call_operation(self, node: nodes.FunctionCall):

        # Get function name - single word for user defined methods and functions, a list for lib functions
        name = node.name.name

        # if function is a library function - serve it here.
        if type(name) == list:
            name = self._return_var_name(node.name)
            if name in self.scope_manager.scope_stack[0][0].vars_or_attrs.keys():
                lib_method_ref = self.scope_manager.get_lib_method(name)
                self._visit_lib_method_operation(lib_method_ref, node)
                return
            else:
                raise error.InvalidCall(" - Called an nonexistent library function.")

        # if function is a class constructor - initialise init.
        if name in self.tree.classes_dict.keys():
            if_object_constructor = self.tree.classes_dict[name]
            self.scope_manager.last_operation_result = if_object_constructor
            return

        # get function from global scope.
        function = self.scope_manager.get_function(name)

        # visit parameters and setup reference checking.
        arguments = []
        is_refer_list = []
        for param in node.params:
            var = param.accept(self)

            is_refer_list.append(var)
            arguments.append(self.scope_manager.last_operation_result)

        # check amount of parameters.
        if len(arguments) != len(function.params):
            raise error.IncorrectArgumentsNumberError(f'Unexpected: {node}')

        # check types if equal. Hard typehint.
        for argument, param in zip(arguments, function.params):
            arg1 = self._return_type_based_on_val(argument)
            arg2 = self._return_type_based_on_val(param)
            if arg1 is not arg2:
                raise error.NotTheSameTypesError(f'Unexpected: {node}')

        # switch scope and add parameters to the scope dictionary.
        self.scope_manager.switch_to_method_scope(function)
        for argument, param in zip(arguments, function.params):
            self.scope_manager.add_var_or_attr(param.name, argument)

        # visit the function instructions.
        self._visit_block(function.instructions)

        # check return value type if equal to function type. Hard typehint.
        returned_value_type = self._return_type_based_on_val(self.scope_manager.return_result)
        if function.type != returned_value_type:
            raise error.NotTheSameTypesError(f'Unexpected: {node}')

        # check if there are referable parameters, before switching the context.
        to_refer_list = []
        for refer_vars, param in zip(is_refer_list, function.params):
            if param.is_refer:
                to_refer_list.append(self.scope_manager.get_var_or_attr(param.name))
            else:
                is_refer_list.remove(refer_vars)

        # switch the context to a previous one
        self.scope_manager.return_from_method_scope()

        # update variables and object members which have been passed to function as references.
        for var, value in zip(is_refer_list, to_refer_list):
            if type(var) == my_parser.nodes.Variable:
                self.scope_manager.update_var_or_attr(var.name, value)
            if type(var) == my_parser.nodes.ObjectVariable:
                object_ = self.scope_manager.get_var_or_attr(var.parent_name)
                object_.member_variables[var.name[0]] = value

    def _visit_object_method_operation(self, node: nodes.ObjectMethod):

        # get object representing class from local scope.
        class_object = self.scope_manager.get_var_or_attr(node.parent_name)

        # get function from local scope.
        function = class_object.member_methods[node.name[0]]

        # visit parameters and setup reference checking.
        arguments = []
        is_refer_list = []
        for param in node.params:
            var = param.accept(self)

            is_refer_list.append(var)
            arguments.append(self.scope_manager.last_operation_result)

        # check amount of parameters.
        if len(arguments) != len(function.params):
            raise error.IncorrectArgumentsNumberError(f'Unexpected: {node}')

        # check types if equal. Hard typehint.
        for argument, param in zip(arguments, function.params):
            arg1 = self._return_type_based_on_val(argument)
            arg2 = self._return_type_based_on_val(param)
            if arg1 is not arg2:
                raise error.NotTheSameTypesError(f'Unexpected: {node}')

        # get method variable values from local scope before switching.
        member_vars_values = []
        for key, value in class_object.member_variables.items():
            member_vars_values.append(value)

        # switch scope and add parameters to the scope dictionary.
        self.scope_manager.switch_to_method_scope(function)
        for argument, param in zip(arguments, function.params):
            self.scope_manager.add_var_or_attr(param.name, argument)

        # set method variable values in new scope
        for attributes, values in zip(class_object.member_variables, member_vars_values):
            self.scope_manager.add_var_or_attr(attributes, values)

        # add methods in a new scope.
        for key, value in class_object.member_methods.items():
            self.scope_manager.add_method(key, value)

        # visit the function instructions.
        self._visit_block(function.instructions)

        # check return value type if equal to function type. Hard typehint.
        returned_value_type = self._return_type_based_on_val(self.scope_manager.return_result)
        if function.type != returned_value_type:
            raise error.NotTheSameTypesError(f'Unexpected: {node}')

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
            member_vars_values.append(self.scope_manager.get_var_or_attr(attributes))

        # switch the context to a previous one
        self.scope_manager.return_from_method_scope()

        # set method variable values in parent scope
        for attributes, values in zip(class_object.member_variables, member_vars_values):
            class_object.member_variables[attributes] = values

        # update variables and object members which have been passed to function as references.
        for var, value in zip(is_refer_list, to_refer_list):
            if type(var) == my_parser.nodes.Variable:
                self.scope_manager.update_var_or_attr(var.name, value)

    def _visit_return_stat_operation(self, node: nodes.ReturnStat):
        node.return_value.accept(self)
        self.scope_manager.return_result = self.scope_manager.last_operation_result

    def _visit_if_else_operation(self, node: nodes.IfElseStat):
        node.condition.accept(self)

        if self.scope_manager.last_operation_result:
            self._visit_block(node.instructions)
            if self.scope_manager.return_result is not None:
                return
        else:
            self._visit_block(node.else_instr)
            if self.scope_manager.return_result is not None:
                return

    def _visit_while_operation(self, node: nodes.WhileStat):
        node.condition.accept(self)

        while self.scope_manager.last_operation_result:
            self._visit_block(node.instructions)
            node.condition.accept(self)

    def _visit_assign_operation(self, node: nodes.AssignStat):

        node.right.accept(self)

        if type(self.scope_manager.last_operation_result) == my_parser.nodes.Class:
            self._visit_new_object(node)
            return

        if type(node.left) == my_parser.nodes.ObjectVariable:
            object_ = self.scope_manager.get_var_or_attr(node.left.parent_name)
            if object_:
                object_.member_variables[node.left.name[0]] = self.scope_manager.last_operation_result
                return

            raise error.UndeclaredSymbol()

        self.scope_manager.update_var_or_attr(self._return_var_name(node.left),
                                              self.scope_manager.last_operation_result)

    def _visit_init_operation(self, node: nodes.InitStat):
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

        raise error.InvalidInitialisationError(f'Unexpected: {node}')

    def _visit_block(self, block: list):

        scope = nodes.Variable("local_block")

        self.scope_manager.switch_to_child_scope(scope)

        for instruction in block:
            if isinstance(instruction, list):
                self._visit_block(instruction)
            else:
                instruction.accept(self)
            if self.scope_manager.return_result is not None:
                return_result = self.scope_manager.return_result
                self.scope_manager.switch_to_parent_scope()
                self.scope_manager.return_result = return_result
                return

        self.scope_manager.switch_to_parent_scope()

    def _visit_function_def_operation(self, node: nodes.FunctionDef):
        if node.instructions is not None:
            return self._visit_block(node.instructions)

        self.scope_manager.return_result = 0

    def _visit_new_object(self, node: nodes.AssignStat):

        class_def = self.scope_manager.last_operation_result

        class_instance = nodes.ClassInstance(node.left.name, class_def, {}, {})

        self._visit_class_instance(node.left.name, class_instance)

    def _visit_class_instance(self, object_name, class_instance: nodes.ClassInstance):

        for variables in class_instance.type.member_variables:
            self._add_class_attr_operation(variables, class_instance)

        for meths in class_instance.type.member_methods:
            self._add_class_method_operation(meths, class_instance)

        self.scope_manager.add_var_or_attr(object_name, class_instance)

    def _add_class_attr_operation(self, node: nodes.InitStat, class_instance: nodes.ClassInstance):
        name = node.name
        default_value = self._return_default_val_of_variable(node)

        if node.right is None:
            class_instance.member_variables[name] = default_value
            return True

        node.right.accept(self)
        arg1 = self._return_type_based_on_val(self.scope_manager.last_operation_result)

        if arg1 == self._return_type_based_on_val(default_value):
            class_instance.member_variables[name] = self.scope_manager.last_operation_result
            return True

        raise error.InvalidInitialisationError(f'Unexpected: {node}')

    @staticmethod
    def _add_class_method_operation(meths, class_instance):
        class_instance.member_methods[meths.name] = meths

    def _visit_lib_method_operation(self, lib_method_ref, node: nodes.FunctionCall):

        arguments = []
        for param in node.params:
            param.accept(self)
            arguments.append(self.scope_manager.last_operation_result)

        lib_method_ref(arguments)

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

    @staticmethod
    def _return_var_name(node):
        if type(node) != my_parser.nodes.ObjectVariable:
            return node.name

        temp = node.parent_name

        for name in node.name:
            temp = temp + "." + name

        return temp

    def _return_type_based_on_val(self, node):
        value = node
        if type(node) == my_parser.nodes.Integer or type(node) == my_parser.nodes.String:
            value = node.value
        elif type(node) == my_parser.nodes.Boolean:
            if node.value == "true":
                value = True
            else:
                value = False
        elif type(node) == my_parser.nodes.Float:
            value = node.value + node.decimalValue / 10 ** node.denominator
        elif type(node) == my_parser.nodes.Variable:
            value = self.scope_manager.get_var_or_attr(node.name)
        elif type(node) == my_parser.nodes.Parameter:
            value = self._return_default_val_of_variable(node)

        if isinstance(value, float):
            return TokenType.K_DOUBLE
        if isinstance(value, bool):
            return TokenType.K_BOOLEAN
        if isinstance(value, int):
            return TokenType.K_INTEGER
        if isinstance(value, str):
            return TokenType.K_STRING

        return TokenType.K_VOID
