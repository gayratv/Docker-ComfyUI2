import argparse
import requests


def get_latest_version(package_name):
    """
    Функция для получения последней версии пакета с PyPI.
    :param package_name: Имя пакета на PyPI.
    :return: Строка с последней версией пакета.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["info"]["version"]
    else:
        raise ValueError(f"Package {package_name} not found on PyPI.")


if __name__ == "__main__":
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(description="Get the latest version of a Python package from PyPI.")

    # Добавляем аргумент для имени пакета
    parser.add_argument(
        "--package_name",
        type=str,
        default="comfyui-frontend-package",
        help="The name of the Python package to check (e.g., comfyui-frontend-package)."
    )

    # Парсим аргументы командной строки
    args = parser.parse_args()

    try:
        # Получаем последнюю версию указанного пакета
        latest_version = get_latest_version(args.package_name)
        print(f"The latest version of {args.package_name} is {latest_version}")
    except ValueError as e:
        print(e)