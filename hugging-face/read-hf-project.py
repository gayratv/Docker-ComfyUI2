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
    repo_id = "Gayrat1968/buffalo_l"
    entries = get_download_info(repo_id,download_dir="models/insightface/models/buffalo_l")

    for entry in entries:
        print(entry)
