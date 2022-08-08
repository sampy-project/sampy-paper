

def create_vaccine_map(shape_map, center, radius, level):
    dict_vacc = dict()
    for i in range(shape_map[0]):
        for j in range(shape_map[1]):
            if (center[0] - i) ** 2 + (center[1] - j) ** 2 <= radius ** 2:
                dict_vacc[(i, j)] = level
            else:
                dict_vacc[(i, j)] = 0.
    return dict_vacc

