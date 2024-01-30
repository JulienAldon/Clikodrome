def generate_filter_condition(arguments: dict[str, any]) -> (str, list[any]):
    """Create a filter condition for SQL request.

    Args:
        arguments (dict[str, any]): dict containing all arguments and their value (locals()).

    Returns:
        filter_condition (str):  WHERE clause with all arguments and placeholder argument (%s).
        filter_instructions (list[any]): List the values of the filter condition.
    Exceptions:
        TypeError: If arguments is not a dict.
    """
    if type(arguments) != dict:
        raise TypeError
    added_condition = 0
    filter_instructions = []
    filter_condition = 'WHERE'
    for i in list(arguments):
        if arguments[i] != '':
            filter_condition += f'{" AND" if added_condition > 0 else ""} {i}=%s'
            filter_instructions.append(arguments[i])
            added_condition += 1
    return filter_condition, filter_instructions