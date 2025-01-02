def camel_case_to_snake_case(input_str: str) -> str:
    """
    Преобразовывает написание классов "кэмэл-кейс" в
    "снэйк-кейс" для правильного написания имён таблиц.
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo
    """
    chars = []
    for char_index, char in enumerate(input_str):
        if char_index and char.isupper():
            next_index = char_index + 1
            flag = (
                next_index >= len(input_str) or input_str[next_index].isupper()
            )
            prev_char = input_str[char_index - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)
