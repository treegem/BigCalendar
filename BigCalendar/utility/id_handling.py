def opposite_id(id):
    split_id = id.split('_')
    this_id_category = split_id[0]
    this_id_number = split_id[1]
    other_id_category = opposite_id_category(this_id_category)
    other_id = '_'.join([other_id_category, this_id_number])
    return other_id


def opposite_id_category(this_id_category):
    if this_id_category == 'yes':
        other_id_category = 'no'
    elif this_id_category == 'no':
        other_id_category = 'yes'
    return other_id_category