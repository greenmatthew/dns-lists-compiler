from sys import argv
import os
import requests

lists_of_blacklists = ["https://v.firebog.net/hosts/lists.php?type=tick"]
lists_of_whitelists = []

blacklist = []
whitelist = ["https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt"]

def fetch_urls_from_list(list_of_urls):
    urls = []
    for url in list_of_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            urls.extend(response.text.splitlines())
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
    return urls

def fetch_and_compile(urls):
    compiled_data = ""
    for url in urls:
        try:
            print(f"Fetching: {url}")
            response = requests.get(url)
            response.raise_for_status()
            compiled_data += response.text + "\n"
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
    return compiled_data

def main(argc: int, argv: list):
    global blacklist, whitelist

    os.makedirs('lists', exist_ok=True)

    print("Fetching blacklist URLs...")
    blacklist.extend(fetch_urls_from_list(lists_of_blacklists))

    print("Fetching whitelist URLs...")
    whitelist.extend(fetch_urls_from_list(lists_of_whitelists))

    print("Compiling blacklists...")
    with open("lists/compiled_blacklist.txt", "w") as file:
        file.write(fetch_and_compile(blacklist))

    print("Compiling whitelists...")
    with open("lists/compiled_whitelist.txt", "w") as file:
        file.write(fetch_and_compile(whitelist))

    print("Lists compiled successfully.")

if __name__ == "__main__":
    main(len(argv), argv)
