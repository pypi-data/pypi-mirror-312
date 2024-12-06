import requests


def updater(repo, repo_path, file_url):
    r = requests.get(url=file_url)
    version = r.content.decode()
    return f"{repo}/{repo_path}/{version}"


def writeversion(filepath, version):
    with open(file=f"{filepath}/VERSION", mode="w+") as f:
        f.write(version)


if __name__ == "__main__":
    print(
        updater(
            repo="https://github.com/tct123/simplethanks",
            repo_path="/releases/tag",
            file_url="https://raw.githubusercontent.com/tct123/simplethanks/refs/heads/main/src/simplethanks/VERSION",
        )
    )
