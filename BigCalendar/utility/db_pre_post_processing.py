def collective_availability(column_names, user_availabilities):
    id_availability = 1
    for user in column_names:
        if user_availabilities[user] == 0:
            id_availability = 0
            break
        elif user_availabilities[user] == 2:
            id_availability = 2
    return id_availability


def comma_separated_entries(list_):
    joined_entries = ', '.join(list_)
    return joined_entries

def who_is_unavailable():
    pass