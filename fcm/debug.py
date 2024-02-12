debug_values = {}


def debug_value(context, value):
    if context not in debug_values:
        debug_values[context] = {}
    if value not in debug_values[context]:
        debug_values[context][value] = 0
    debug_values[context][value] += 1


def debug_print():
    for context in debug_values:
        print(context)
        for value in debug_values[context]:
            count = debug_values[context][value]
            print("", value, count)
