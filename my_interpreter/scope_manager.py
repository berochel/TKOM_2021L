import error.error_handlers as error


class Scope:
    def __init__(self, name):
        self.name = name
        self.vars_or_attrs = {}
        self.methods = {}

    def add_var_or_attr(self, name, value):
        self.vars_or_attrs[name] = value

    def get_var_or_attr(self, name):
        symbol = self.vars_or_attrs[name]
        return symbol

    def add_method(self, name, value):
        self.methods[name] = value

    def get_method(self, name):
        if name not in self.methods.keys():
            raise error.UndeclaredMethod()

        method = self.methods[name]
        return method


class ScopeManager:

    def __init__(self):
        self.scope_stack = [[Scope('global')], []]
        self.last_operation_result = None
        self.return_result = None

    def add_var_or_attr(self, name, variable):
        for scope in self.scope_stack[-1]:
            if name in scope.vars_or_attrs.keys():
                raise error.OverwriteError(name)

        self.scope_stack[-1][-1].add_var_or_attr(name, variable)

    def update_var_or_attr(self, name, variable):
        for scope in self.scope_stack[-1]:
            if name in scope.vars_or_attrs.keys():
                scope.vars_or_attrs[name] = variable
                return True

        raise error.UndeclaredSymbol(name)

    def get_var_or_attr(self, name):
        for scope in self.scope_stack[-1]:
            if name in scope.vars_or_attrs.keys():
                return scope.get_var_or_attr(name)

        raise error.UndeclaredSymbol()

    def add_function(self, name, function):
        self.scope_stack[0][0].add_method(name, function)

    def get_function(self, name):
        return self.scope_stack[0][0].get_method(name)

    def add_lib_method(self, name, function):
        self.scope_stack[0][0].add_var_or_attr(name, function)

    def get_lib_method(self, name):
        return self.scope_stack[0][0].get_var_or_attr(name)

    def add_method(self, name, method):
        for scope in self.scope_stack[-1]:
            if name in scope.methods.keys():
                raise error.OverwriteError(name)

        self.scope_stack[-1][-1].add_method(name, method)

    def get_method(self, name):
        for scope in self.scope_stack[-1]:
            if name in scope.methods.keys():
                return scope.get_method(name)

        raise error.UndeclaredSymbol(name)

    def switch_to_child_scope(self, function):
        function_scope = Scope(function.name)

        last_scope = self.scope_stack[-1].copy()
        last_scope.append(function_scope)
        self.scope_stack.append(last_scope)

    def switch_to_method_scope(self, function):
        function_scope = Scope(function.name)

        last_scope = [self.scope_stack[0][0], function_scope]
        self.scope_stack.append(last_scope)

    def switch_to_parent_scope(self):
        if len(self.scope_stack) == 0:
            raise error.NoParentContextError()

        self.scope_stack.pop()
        self.last_operation_result = self.return_result
        self.return_result = None

    def return_from_method_scope(self):
        if len(self.scope_stack) == 0:
            raise error.NoParentContextError()

        self.scope_stack.pop()
        self.last_operation_result = self.return_result
        self.return_result = None
