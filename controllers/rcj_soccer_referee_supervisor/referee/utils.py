def time_to_string(time: int) -> str:
    """Convert time to string representation

    Args:
        time (int): Time in seconds

    Returns:
        str: Time in MM:SS format
    """
    return "%02d:%02d" % (time // 60, time % 60)
