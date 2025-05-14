import json
import sys
import os

def load_json_file(filepath):
    """Loads JSON data from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {filepath}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: Невозможно декодировать JSON из файла: {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при чтении файла {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

def create_translation_map(translation_data):
    """Creates a dictionary mapping original titles to new titles."""
    translation_map = {}
    if not isinstance(translation_data, list):
        print("Предупреждение: Файл перевода не является списком объектов.", file=sys.stderr)
        return translation_map

    for item in translation_data:
        if isinstance(item, dict) and 'title' in item and 'new-title' in item:
            translation_map[item['title']] = item['new-title']
        else:
            print(f"Предупреждение: Некорректный формат элемента в файле перевода: {item}", file=sys.stderr)
    return translation_map

def translate_workflow_titles(workflow_data, translation_map):
    """Recursively traverses the workflow data and translates 'title' attributes."""

    if isinstance(workflow_data, dict):
        # If it's a dictionary, check for 'title' and recurse on values
        if 'title' in workflow_data:
            original_title = workflow_data['title']
            if original_title in translation_map:
                workflow_data['title'] = translation_map[original_title]
                # print(f"Переведено: '{original_title}' -> '{workflow_data['title']}'") # Optional: for debugging

        for key, value in workflow_data.items():
            workflow_data[key] = translate_workflow_titles(value, translation_map)

    elif isinstance(workflow_data, list):
        # If it's a list, recurse on each item
        for i in range(len(workflow_data)):
            workflow_data[i] = translate_workflow_titles(workflow_data[i], translation_map)

    # If it's neither dict nor list, return as is (base case)
    return workflow_data

def save_json_file(data, filepath):
    """Saves data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Переведенный рабочий процесс успешно сохранен в: {filepath}")
    except Exception as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Define input and output filenames
    workflow_file = '/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflows/Change_Background_redraw_bg_clothers/chngbg2.json'
    translation_file = '/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflow-descr/Change_Background_redraw_bg_clothers/title-translate.json'
    output_file = '/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflows/Change_Background_redraw_bg_clothers/chngbg2_translated_ru.json' # You can change the output name

    # Check if input files exist
    if not os.path.exists(workflow_file):
        print(f"Ошибка: Файл рабочего процесса не найден: {workflow_file}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(translation_file):
        print(f"Ошибка: Файл перевода не найден: {translation_file}", file=sys.stderr)
        sys.exit(1)

    print(f"Загрузка рабочего процесса из: {workflow_file}")
    workflow_data = load_json_file(workflow_file)

    print(f"Загрузка переводов из: {translation_file}")
    translation_data = load_json_file(translation_file)

    print("Создание карты переводов...")
    translation_map = create_translation_map(translation_data)
    print(f"Загружено {len(translation_map)} переводов.")

    print("Перевод заголовков рабочего процесса...")
    translated_workflow_data = translate_workflow_titles(workflow_data, translation_map)
    # Note: The function modifies in place, so workflow_data is already translated.
    # We assign to a new variable just to be explicit, but it's the same object.

    print(f"Сохранение переведенного рабочего процесса в: {output_file}")
    save_json_file(translated_workflow_data, output_file)

    print("Перевод завершен.")