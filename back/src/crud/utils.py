def generate_filter_condition(arguments):
    added_condition = 0
    exec_list = []
    filter_condition = 'WHERE'
    for i in list(arguments):
        if arguments[i] != '':
            filter_condition += f'{" AND" if added_condition > 0 else ""} {i}=%s'
            exec_list.append(arguments[i])
            added_condition += 1
    return filter_condition, exec_list