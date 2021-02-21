from coordinate import CoordinateHD, Direction


def run_backend():
    coord1 = CoordinateHD()
    coord2 = CoordinateHD(90, 5, 30, Direction.LONGITUDE)
    return '\n'.join((
        str(coord2.get_format_ddmmssD()),
        str(coord2.get_format_ddddD()),
        str(coord2.get_coordinate_beetween_current_and(coord1)),
        str(CoordinateHD.get_coordinate_beetween(coord1, coord2))
    ))
