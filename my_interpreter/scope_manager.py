import error.error_handlers as error


class Scope:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.vars_or_attrs = {}
        self.methods = {}

    def add_var_or_attr(self, name, value):
        self.vars_or_attrs[name] = value

    def get_var_or_attr(self, name):
        if name not in self.vars_or_attrs.keys():
            raise error.UndeclaredSymbol()

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
        self.global_scope = Scope("global")
        self.current_scope = Scope('main')
        self.last_operation_result = None
        self.return_result = None

    def add_var_or_attr(self, name, variable):
        if name in self.current_scope.vars_or_attrs.keys():
            raise error.OverwriteError(name)
        self.current_scope.add_var_or_attr(name, variable)

    def update_var_or_attr(self, name, variable):
        if name not in self.current_scope.vars_or_attrs.keys():
            raise error.UndeclaredSymbol(name)

        self.current_scope.vars_or_attrs[name] = variable

    def get_var_or_attr(self, name):
        return self.current_scope.get_var_or_attr(name)

    def add_function(self, name, function):
        self.global_scope.add_method(name, function)

    def get_function(self, name):
        return self.global_scope.get_method(name)

    def add_lib_method(self, name, function):
        self.global_scope.add_var_or_attr(name, function)

    def get_lib_method(self, name):
        return self.global_scope.get_var_or_attr(name)

    def add_method(self, name, method):
        if name in self.current_scope.vars_or_attrs.keys():
            raise error.OverwriteError(name)
        self.current_scope.add_method(name, method)

    def get_method(self, name):
        return self.current_scope.get_method(name)

    def switch_to_child_scope(self, function):
        function_scope = Scope(function.name, self.current_scope)
        self.current_scope = function_scope

    def switch_to_parent_scope(self):
        if not self.current_scope.parent:
            raise error.NoParentContextError(self.current_scope.name)

        self.last_operation_result = self.return_result
        self.current_scope = self.current_scope.parent
        self.return_result = None
