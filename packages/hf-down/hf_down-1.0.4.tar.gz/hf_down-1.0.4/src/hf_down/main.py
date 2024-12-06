import argparse
import json
import os
import time
from pathlib import Path
from subprocess import check_output, CalledProcessError

import requests
from configargparse import ArgumentParser
from lxml import etree
from termcolor import colored

repository_structure: dict = {}


def get_config() -> argparse.Namespace:
    parser = ArgumentParser()

    parser.add_argument("--url", type=str, required=True,
                        help="Huggingface repository URL")
    parser.add_argument("--output_dir", type=str, default="downloaded_files",
                        help="Output directory")

    return parser.parse_args()


def get_page(url):
    for _ in range(3):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return etree.HTML(response.text)
        except requests.RequestException as e:
            print(f"Error Request {url}: {e}, Will Retry After 1s")
            time.sleep(1)
            continue
    return None


def parse_page(root, current_path, structure):
    li_elements = root.xpath('/html/body/div/main/div[2]/section/div[3]/ul/li')

    for li in li_elements:
        clazz: str = li.get('class', '')
        a_tags = li.xpath('.//a[@href]')
        if not a_tags:
            continue

        link = a_tags[0]
        href = link.get('href')
        name = Path(href).name

        if clazz.find("relative") == -1:
            folder_url = 'https://huggingface.co' + href
            folder_name = name
            print(f"Find Folder: {current_path}/{folder_name} -> {folder_url}")

            structure[folder_name] = {}

            child_root = get_page(folder_url)
            if child_root is not None:
                parse_page(child_root, os.path.join(current_path, folder_name), structure[folder_name])
                time.sleep(0.5)
        else:
            if '/resolve/main/' in href:
                download_url = 'https://huggingface.co' + href + '?download=true'
                print(f"Find File: {current_path}/{name} -> {download_url}")
                structure[name] = download_url
            else:
                download_url = ('https://huggingface.co' + href).replace("blob", "resolve")
                print(f"Find File: {current_path}/{name} -> {download_url}")
                structure[name] = download_url


def download_files(structure, base_path):
    """
    递归下载文件，并保持目录结构。

    :param structure: 存储文件和文件夹的字典
    :param base_path: 当前下载的基础路径
    """
    for name, value in structure.items():
        for i in range(3):
            if isinstance(value, dict):
                new_path = os.path.join(base_path, name)
                os.makedirs(new_path, exist_ok=True)
                print(f"Makedir: {new_path}")
                download_files(value, new_path)
            else:
                download_url = value
                file_path = os.path.join(base_path, name)
                print(f"Start Download: {colored(download_url, 'green')} -> {colored(file_path, 'green')}")

                cmd = [
                    'aria2c',
                    '-c',
                    '-x', '16',
                    '-s', '16',
                    '-o', name,
                    '-d', base_path,
                    download_url
                ]

                try:
                    check_output(cmd)
                    print(f"Download Success: {colored(file_path, 'green')}")
                    break
                except CalledProcessError as e:
                    print(f"Download Failed: {colored(download_url, 'red')}\nError Message: {colored(e, 'red')}")
                    time.sleep(1)
                    continue
                except Exception as e:
                    print(f"Error: {colored(e, 'red')}")
                    time.sleep(1)
                    continue


def main():
    global repository_structure
    args = get_config()
    root_url: str = args.url
    branch: str = root_url.split("/")[-1]

    if root_url.split("/")[-2] != "tree":
        print(colored("URL should be ended in 'tree/branch' format", "light_yellow"))

    print(f"Start Parsing Repository: {colored(root_url, 'green')}\n")
    print()
    root = get_page(root_url)
    if root is None:
        raise RuntimeError(f"Can't Get Page From {root_url}")

    parse_page(root, branch, repository_structure)

    print("Repository Structure:")
    print(json.dumps(repository_structure, indent=4, ensure_ascii=False))

    with open('repository_structure.json', 'w', encoding='utf-8') as f:
        json.dump(repository_structure, f, indent=4, ensure_ascii=False)
    print()

    print(colored("Start Downloading Files...", "green"))
    download_root = args.output_dir
    os.makedirs(download_root, exist_ok=True)
    download_files(repository_structure, download_root)
    print(colored("All Files Downloaded", "green"))


if __name__ == "__main__":
    main()
