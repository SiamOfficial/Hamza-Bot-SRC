def convert_to_arabic_number(number_string) -> str:
    dic = {
        '0': '۰',
        '1': '١',
        '2': '٢',
        '3': '۳',
        '4': '٤',
        '5': '٥',
        '6': '٦',
        '7': '٧',
        '8': '٨',
        '9': '۹',
        ':': ':'
    }
    return "".join([dic[char] for char in number_string])


def convert_from_arabic_number(number_string) -> str:
    dic = {
        '۹': '9',
        '٨': '8',
        '٧': '7',
        '٦': '6',
        '٥': '5',
        '٤': '4',
        '۳': '3',
        '٢': '2',
        '١': '1',
        '۰': '0',
        ':': ':'
    }
    return "".join([dic[char] for char in number_string])