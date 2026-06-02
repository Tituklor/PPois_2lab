import os
import random
from model import Client, ClientCollection
from xml_handler import XMLHandler

# Базы данных для генерации реалистичных записей
SURNAMES = [
    "Иванов", "Петров", "Сидоров", "Кузнецов", "Попов", "Смирнов", "Васильев",
    "Новиков", "Федоров", "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов",
    "Егоров", "Павлов", "Козлов", "Степанов", "Николаев", "Орлов", "Андреев",
    "Макаров", "Никитин", "Захаров", "Зайцев", "Соловьев", "Борисов", "Яковлев",
    "Григорьев", "Романов", "Воробьев", "Сергеев", "Кузьмин", "Фролов", "Александров"
]

NAMES = [
    "Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артем",
    "Илья", "Кирилл", "Михаил", "Никита", "Матвей", "Роман", "Егор", "Арсений",
    "Иван", "Денис", "Евгений", "Даниил", "Тимофей", "Владислав", "Игорь",
    "Владимир", "Павел", "Руслан", "Марк", "Константин", "Тимур", "Олег", "Ярослав"
]

PATRONYMICS = [
    "Александрович", "Дмитриевич", "Максимович", "Сергеевич", "Андреевич",
    "Алексеевич", "Иванович", "Федорович", "Григорьевич", "Владимирович",
    "Петрович", "Николаевич", "Васильевич", "Михайлович", "Олегович",
    "Романович", "Евгеньевич", "Юрьевич", "Анатольевич", "Константинович"
]

CITIES = ["г. Минск", "г. Витебск", "г. Брест", "г. Пинск",
          "г. Ивацевичи", "г. Гомель", "г. Ельск", "г. Омск",
          "г. Ветка", "г. Калинковичи", "г. Быхов", "г. Мозырь"]

STREETS = ["ул. Ленина", "пр. Мира", "ул. Пушкина", "ул. Гагарина", "ул. Советская",
           "ул. Кирова", "ул. Экзотическая", "ул. Лермонтова", "ул. Чехова",
           "ул. Толстого", "бул. Юности", "ул. Беды"]


def generate_phone(is_mobile: bool) -> str:
    country_code = "+375"

    if is_mobile:
        # Мобильные операторы: life:) (25), МТС (29, 33), А1 (29, 44)
        prefixes = ["25", "29", "33", "44"]
        operator_code = random.choice(prefixes)
        # Формат: +375 (29) 123-45-67
        number_part = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        return f"{country_code} ({operator_code}) {number_part}"
    else:
        # Городские коды: Минск (17), Брест (162), Витебск (212), Гомель (232), Гродно (152), Могилев (222)
        city_codes = ["17", "162", "212", "232", "152", "222"]
        city_code = random.choice(city_codes)
        # Формат: +375 (17) 123-45-67
        number_part = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        return f"{country_code} ({city_code}) {number_part}"

def generate_client() -> Client:
    """Создание одного случайного клиента"""
    surname = random.choice(SURNAMES)
    name = random.choice(NAMES)
    patronymic = random.choice(PATRONYMICS)
    full_name = f"{surname} {name} {patronymic}"

    # Генерация 20-значного банковского счета (симуляция)
    account = f"40702810{random.randint(10000, 99999)}{random.randint(10000, 99999)}"

    city = random.choice(CITIES)
    street = random.choice(STREETS)
    house = random.randint(1, 180)
    apt = random.randint(1, 450)
    address = f"{city}, {street}, д. {house}, кв. {apt}"

    phone_mobile = generate_phone(is_mobile=True)
    phone_landline = generate_phone(is_mobile=False)

    return Client(full_name, account, address, phone_mobile, phone_landline)


def main():
    """Основная функция генерации"""
    print(" Генерация тестовых данных...")

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    # Создаем 2 файла, как требуется в задании
    target_files = ["clients_batch_1.xml", "clients_batch_2.xml"]
    records_count = 55  # > 50 согласно заданию

    for filename in target_files:
        filepath = os.path.join(data_dir, filename)
        collection = ClientCollection()

        print(f" Формирование {records_count} записей для '{filename}'...")
        for _ in range(records_count):
            collection.add_client(generate_client())

        if XMLHandler.save_to_xml(collection, filepath):
            print(f" Файл '{filepath}' успешно сохранен.")
        else:
            print(f" Ошибка сохранения '{filepath}'.")

    print("\n Генерация завершена. Файлы готовы для загрузки в приложение.")


if __name__ == "__main__":
    main()