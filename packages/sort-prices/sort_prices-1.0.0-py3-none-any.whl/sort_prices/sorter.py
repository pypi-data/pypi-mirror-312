def sort_prices_low_to_high(prices):
    """
    Sort a list of prices in ascending order.

    Args:
        prices (list): A list of numeric values representing prices.

    Returns:
        list: Sorted list of prices from low to high.
    """
    if not isinstance(prices, list):
        raise ValueError("Input must be a list.")
    return sorted(prices)
