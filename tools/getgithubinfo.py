import requests
import json
import sys


def get_repositories(username: str):
    """
    Fetch public repositories of a GitHub user using GitHub API.
    """

    url = f"https://api.github.com/users/{username}/repos"

    headers = {
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API Error {response.status_code}: {response.text}"
        )

    return response.json()


def extract_repo_data(repos):
    """
    Extract important project details from repositories.
    """

    extracted_data = []

    for repo in repos:
        project = {
            "name": repo.get("name"),
            "description": repo.get("description"),
            "language": repo.get("language"),
            "topics": repo.get("topics", []),
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "repo_url": repo.get("html_url"),
            "homepage": repo.get("homepage"),
            "is_fork": repo.get("fork"),
            "size_kb": repo.get("size"),
            "default_branch": repo.get("default_branch"),
        }

        extracted_data.append(project)

    return extracted_data


def save_to_json(username: str, data):
    """
    Save extracted repository data into JSON file.
    """

    filename = f"{username}_projects.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Data saved to {filename}")


def main():
    # Check if username argument is provided
    if len(sys.argv) != 2:
        username = input("Please enter your GitHub username: ")
        with open('githubusername.txt', 'w') as f:
            f.write(username)
    else:
        username = sys.argv[1]

    try:
        print(f"\n🔍 Fetching repositories for: {username}")

        repos = get_repositories(username)

        extracted_data = extract_repo_data(repos)

        save_to_json(username, extracted_data)

        print(f"✅ Extracted {len(extracted_data)} repositories")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    main()