def calculate_points(width, height):
    x_start = -3
    x_end = 3
    scale = 10
    accuracy = 4
    points = []

    for x in range(x_start * accuracy, (x_end + 1) * accuracy):
        x = x / accuracy

        ready_x = x * scale + width / 2
        ready_y = x**3 * scale + height / 2

        points.extend((ready_x, ready_y))

    return tuple(points)


piechart_data = {
    "Grey": (45, (0.5, 0.5, 0.5, 1)),
    "Brown": (25, (0.6, 0.3, 0, 1)),
    "Yellow": (15, (0, 1, 1, 1)),
    "Red": (10, (1, 0, 0, 1)),
    "Purple": (5, (1, 0, 1, 1))
}
