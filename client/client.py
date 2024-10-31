import requests

BASE_URL = "http://127.0.0.1:5000"


def get_states():
    response = requests.get(f"{BASE_URL}/states")
    print(response.json())


def create_state():
    title = input("Введите название подразделения: ")
    type_ = input("Введите тип подразделения: ")
    harm_allowance = float(input("Введите процент надбавки за вредные условия: "))
    response = requests.post(f"{BASE_URL}/states", json={
        "title": title,
        "type": type_,
        "harm_allowance": harm_allowance
    })
    print(response.json())


def update_state():
    id = int(input("Введите ID подразделения: "))
    title = input("Введите новое название подразделения: ")
    type_ = input("Введите новый тип подразделения: ")
    harm_allowance = float(input("Введите новый процент надбавки за вредные условия: "))
    response = requests.put(f"{BASE_URL}/states/{id}", json={
        "title": title,
        "type": type_,
        "harm_allowance": harm_allowance
    })
    print(response.json())


def delete_state():
    id = int(input("Введите ID подразделения: "))
    response = requests.delete(f"{BASE_URL}/states/{id}")
    print(response.json())


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Показать все подразделения")
        print("2. Создать новое подразделение")
        print("3. Обновить подразделение")
        print("4. Удалить подразделение")
        print("0. Выйти")

        choice = input("Ваш выбор: ")

        if choice == '1':
            get_states()
        elif choice == '2':
            create_state()
        elif choice == '3':
            update_state()
        elif choice == '4':
            delete_state()
        elif choice == '0':
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == '__main__':
    main()
