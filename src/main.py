from sys import argv
from datetime import datetime
import sys
import os
import requests
import git

lists_of_blacklists = ["https://v.firebog.net/hosts/lists.php?type=tick"]
lists_of_whitelists = []

blacklist = []
whitelist = ["https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt"]

def print_warning_message():
    print("WARNING: This application will force-push to the master branch of the local Git repository.")
    print("This could lead to potentially destructive changes, especially if run in the wrong directory.")
    print("Ensure you are in the correct repository and understand the consequences of a force push.")
    print("If you wish to proceed, run the application with the '--disable-safety-lock' argument.")
    print("Do not run this application in a repository where force-pushing to master could overwrite important data.")

def fetch_urls_from_list(list_of_urls):
    urls = []
    for url in list_of_urls:
        try:
            print(f"Fetching: {url}")
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
    log_file_path = 'output_log.txt'

    with open(log_file_path, 'w') as f:
        # Write the initial log message with the current date and time
        current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        f.write(f"# {current_time}\n\n# Start log:\n\n")

        sys.stdout = f

        if argc == 1 or (argc == 2 and argv[1] != "--disable-safety-lock"):
            print_warning_message()
            sys.exit(0)
        elif argc > 2:
            print("Too many arguments.")
            sys.exit(0)

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

            # Initialize the Git repository object
        repo = git.Repo('.')

        # Fetch and merge with the remote branch (force update)
        repo.git.fetch('--all')
        repo.git.reset('--hard', 'origin/master')  # Replace 'origin/master' with the branch you want to force pull

        print("Force pulled the repository.")

        # Attempt to add changes
        try:
            print("Adding changes to the staging area...")
            repo.git.add('lists/')
            # repo.git.add('output_log.txt')  # Optional

            # Check if there are any changes
            if repo.is_dirty(untracked_files=True):
                print("Changes detected, updating the repository...")

                # Commit changes
                print("Committing changes...")
                repo.git.commit('-m', 'Update detected in lists. Applying update.')

                # Push changes
                print("Pushing changes to remote repository...")
                repo.git.push('origin', 'master')
                print("Changes pushed successfully.")
            else:
                print("No changes detected. No update required.")
        except git.exc.GitCommandError as e:
            print(f"An error occurred with Git operations: {e}")

if __name__ == "__main__":
    main(len(argv), argv)
