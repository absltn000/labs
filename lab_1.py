error_message = "Список невалидный"

# Проверка числа на строку и преобразование в число
def check(x) -> int | float | None:
    new_int = None
    if x <= '':  # Проверка на пустую строку
        return None
    try:
        new_int = int(x)  # Попытка преобразовать в целое число
    except ValueError:
        try:
            new_int = float(x)  # Попытка преобразовать в вещественное число
        except ValueError:
            return new_int
    finally:
        return new_int


# Возвращение строки с информацией о количестве повторений
def out_info_str(temp_int_list) -> str:
    i = 0
    out_str = ""  # Выводимая строка
    sorted(temp_int_list)  # Спортировка для корректной работы алгоритма

    # Составление строки с количеством входа чисел в список
    while i in range(len(temp_int_list)):
        # Добавление информации о числе
        out_str += f'{temp_int_list[i]}({temp_int_list.count(temp_int_list[i])}) '
        # Сдвиг индекса на количество повторяющихся элементов
        i += temp_int_list.count(temp_int_list[i])
    return out_str or error_message


def main() -> int:
    # Разбиение строки на числа
    int_list = list(map(lambda x: check(x), input("Введите список чисел:  ").split(' ')))

    # Проверка на пустоту
    if int_list.count(None) and len(int_list) == 1:
        int_list.clear()
    elif int_list.count(None):
        while int_list.count(None):
            int_list.remove(None)

    print("Полученный список:\n", int_list or error_message)

    # Вывод с вызовом функции для получения информации из вопроса задачи
    print("Список чисел с их повторениями:\n", out_info_str(int_list))
    return 0


if __name__ == '__main__':
    main()
