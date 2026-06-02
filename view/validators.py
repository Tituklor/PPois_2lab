import re


def is_valid_name(name: str) -> bool:

    if not name:
        return False
    parts = name.strip().split() # убирает пробелы и разбивает на список слов
    if len(parts) < 2:
        return False
    pattern = r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$'
    return all(re.match(pattern, part) for part in parts)





def is_valid_phone(phone: str) -> bool:

    if not phone:
        return False
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)


    if cleaned.startswith('+375'):
        digits = cleaned[1:]# убирается +
        if len(digits) != 12:
            return False


        code = digits[3:5]
        valid_codes = ["25", "29", "33", "44",
                       "17", "162", "212", "232", "152", "222"]

        return code in valid_codes and digits.isdigit()


    elif cleaned.startswith('8'):
        digits = cleaned[1:]
        if len(digits) != 11:
            return False


        code = digits[0:2]
        valid_codes = ["25", "29", "33", "44",
                       "17", "162", "212", "232", "152", "222"]

        return code in valid_codes and digits.isdigit()

    return False

def is_valid_account(account: str) -> bool:

    if not account:
        return True

    return account.isdigit()


def validate_client_data(data: dict) -> tuple:

    if not data.get('full_name', '').strip():
        return False, "Поле 'ФИО клиента' обязательно для заполнения."

    if not is_valid_name(data['full_name']):
        return False, "ФИО должно содержать минимум 2 слова (Фамилия и Имя) и только буквы."


    if data.get('phone_mobile') and not is_valid_phone(data['phone_mobile']):
        return False, "Неверный формат мобильного телефона."

    if data.get('phone_landline') and not is_valid_phone(data['phone_landline']):
        return False, "Неверный формат городского телефона."


    if data.get('account_number') and not is_valid_account(data['account_number']):
        return False, "Номер счета должен содержать только цифры."

    return True, ""