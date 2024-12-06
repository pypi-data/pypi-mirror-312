from sympy import parse_expr

def simplify(expression: str) -> str:
    """ Simplify a matrix expression

    Parameters
    ----------
    expression (str): A string representing a mathematical expression.

    Returns
    -------
    str: The simplified expression.
    """
    expr = parse_expr(expression)
    result = str(expr)
    return result
