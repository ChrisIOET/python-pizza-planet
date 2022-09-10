def check_required_keys(keys: tuple, element: dict):
    return all(element.get(key) for key in keys)

def format_currency_with_double_decimals(element: dict) -> float:
    return float("{:.2f}".format(round(element, 2)))

