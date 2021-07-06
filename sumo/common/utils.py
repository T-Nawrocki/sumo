def choices_as_dict(choices):
    """
    Returns django model field choices as a dict.
    The choices argument must be an iterable containing key-value tuples.
    """
    return {choice[0]: choice[1] for choice in choices}