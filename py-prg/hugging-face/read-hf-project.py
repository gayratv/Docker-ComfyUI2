import argparse
from huggingface_hub import HfApi, hf_hub_url
import os


def get_download_info(repo_id, repo_type="model", revision="main", download_dir="models/"):
    api = HfApi()
    repo_info = api.repo_info(repo_id=repo_id, repo_type=repo_type, revision=revision)

    entries = []
    for file in repo_info.siblings:
        url = hf_hub_url(repo_id=repo_id, filename=file.rfilename, revision=revision, repo_type=repo_type)
        filename = os.path.basename(file.rfilename)
        entry = f"{url}\n      dir={download_dir}\n      out={filename}"
        entries.append(entry)

    return entries


if __name__ == "__main__":
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Получить список файлов из репозитория Hugging Face и сформировать строки для загрузки.")

    # Добавляем аргументы
    parser.add_argument("--repo_id", type=str, required=True,
                        help="Идентификатор репозитория (например: 'Gayrat1968/buffalo_l')")
    parser.add_argument("--download_dir", type=str, default="models/",
                        help="Каталог для сохранения файлов (по умолчанию: 'models/')")
    parser.add_argument("--repo_type", type=str, default="model", choices=["model", "dataset", "space"],
                        help="Тип репозитория (по умолчанию: 'model')")
    parser.add_argument("--revision", type=str, default="main", help="Ветка или хэш коммита (по умолчанию: 'main')")

    # Парсим аргументы
    args = parser.parse_args()

    # Получаем информацию о файлах
    entries = get_download_info(
        repo_id=args.repo_id,
        repo_type=args.repo_type,
        revision=args.revision,
        download_dir=args.download_dir
    )

    # Выводим результат на экран
    for entry in entries:
        print(entry)

    # Сохраняем в файл
    with open("../../comfyui-union2/aria2/templates/models/Wan2.1-VACE/hf-dl.txt", "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry + "\n\n")

    print("\nСписок сохранен в файл: hf-dl.txt")