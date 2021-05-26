def print_def(list_of_args):
    if len(list_of_args) == 1:
        print(list_of_args[0])
        return

    str_to_print = ""
    for arg in list_of_args:
        str_to_print += str(arg)

    print(str_to_print)


def load_lib_def():
    lib_methods_dict = {"System.out.print": print_def}

    return lib_methods_dict
