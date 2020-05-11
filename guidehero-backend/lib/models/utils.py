def validate_points(value):
    if value < 0:
        raise ValueError('points can not be less than 0')
    return value
