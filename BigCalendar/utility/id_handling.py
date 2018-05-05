def opposite_id(id_):
    this_id_category, this_id_number = split_id(id_)
    other_id_category = opposite_id_category(this_id_category)
    other_id = '_'.join([other_id_category, this_id_number])
    return other_id


def split_id(id_):
    id_components = id_.split('_')
    this_id_category = id_components[0]
    this_id_number = id_components[1]
    return this_id_category, this_id_number


def opposite_id_category(this_id_category):
    if this_id_category == 'yes':
        other_id_category = 'no'
    elif this_id_category == 'no':
        other_id_category = 'yes'
    return other_id_category
