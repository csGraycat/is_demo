import locale


def sort_enumerated_field(data):
    locale.setlocale(locale.LC_ALL, '')

    def sort_key(item):
        return locale.strxfrm(item['VALUE'])

    sorted_data = sorted(data, key=sort_key)
    for index, item in enumerate(sorted_data):
        item['SORT'] = index + 1

    return sorted_data

