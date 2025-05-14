import re
import argparse

def replace_properties(text, find_cnr_id, find_ver, find_node_name,
                       aux_id, ver, node_name):
    """
    Находит и заменяет блоки "properties" в тексте.

    Args:
        text: Исходный текст.
        find_cnr_id: Значение "cnr_id" для поиска.
        find_ver: Значение "ver" для поиска.
        find_node_name: Значение "Node name for S&R" для поиска.
        aux_id: Значение для "aux_id" в замене.
        ver: Значение для "ver" в замене.
        node_name: Значение для "Node name for S&R" в замене.

    Returns:
        Текст с замененными блоками "properties".
    """

    print(f"find_cnr_id = '{find_cnr_id}'")
    print(f"find_ver = '{find_ver}'")
    print(f"find_node_name = '{find_node_name}'")

    # "properties": {
    #     "cnr_id": "Comfyui-ergouzi-Nodes",
    #     "ver": "0d6ac29773fa03e439dd9deb282453b739403427",
    #     "Node name for S&R": "EG_RY_HT"
    # },

    # Динамическое создание регулярного выражения на основе параметров поиска
    # pattern = re.compile(
    #     r'"properties": {\s*'
    #     rf'"cnr_id": "{re.escape(find_cnr_id)}",\s*'  # re.escape для безопасной обработки спецсимволов
    #     rf'"ver": "{re.escape(find_ver)}",\s*'
    #     rf'"Node name for S&R": "{re.escape(find_node_name)}"\s*'
    #     r'},\s*',
    #     re.DOTALL  # Важно: позволяет . соответствовать символу новой строки
    # )

    pattern = re.compile(r'ergouzi')

    replacement = f'"properties": {{\n' \
                  f'        "aux_id": "{aux_id}",\n' \
                  f'        "ver": "{ver}",\n' \
                  f'        "Node name for S&R": "{node_name}"\n' \
                  f'      }},\n'

    matches = pattern.findall(text)

    print(f"Найдено соответствий: {len(matches)}")
    if matches:
        print(f"Первое соответствие: {matches[0]}")
    else:
        print("Соответствий не найдено.")

    return pattern.sub(replacement, text)


def main(input_file, output_file, find_cnr_id, find_ver, find_node_name, aux_id, ver, node_name):
    """
    Основная функция скрипта.  Получает имена входного и выходного файлов и параметры замены,
    выполняет замену и сохраняет результат.
    """

    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            input_text = infile.read()
        print("Файл успешно прочитан.")


        # input_text = """
        # "properties": {
        #         "cnr_id": "Comfyui-ergouzi-Nodes",
        #         "ver": "0d6ac29773fa03e439dd9deb282453b739403427",
        #         "Node name for S&R": "EG_RY_HT"
        #       },
        # """

        output_text = replace_properties(
            input_text,
            find_cnr_id,
            find_ver,
            find_node_name,
            aux_id,
            ver,
            node_name
        )

        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(output_text)

        print(f"Замена выполнена. Результат сохранен в {output_file}")

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        exit()


if __name__ == "__main__":
    # Задаем значения параметров (примеры):
    # input_file = "/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflows/Change_Background_redraw_bg_clothers/orig/change-bg-redraw-clothes-hair-face.json"
    # input_file = "/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflows/Change_Background_redraw_bg_clothers/change-bg-redraw-clothes-hair-face 2 — копия.json"
    input_file = "/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflows/Change_Background_redraw_bg_clothers/chngbg2.json"

    output_file = "/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflows/Change_Background_redraw_bg_clothers/change-bg-redraw-clothes-hair-face 5.json"

    find_cnr_id = "Comfyui-ergouzi-Nodes"
    find_ver = "0d6ac29773fa03e439dd9deb282453b739403427"
    find_node_name = "EG_RY_HT"

    aux_id = "gayratv/ComfyUI_Gayrat"
    ver = "87e8422b7a57afff90906df671f1ab6ca88acc93"
    node_name = "EG_RY_HT"

    # Вызываем функцию main с заданными параметрами:
    main(input_file, output_file, find_cnr_id, find_ver, find_node_name, aux_id, ver, node_name)