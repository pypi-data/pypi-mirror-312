import requests


def create_github_release(owner, repo, tag_name, release_name, body, draft=False, prerelease=False, token='YOUR_GITHUB_TOKEN'):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "tag_name": tag_name,
        "name": release_name,
        "body": body,
        "draft": draft,
        "prerelease": prerelease
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Release created successfully!")
        return response.json()
    else:
        print(f"Failed to create release: {response.status_code}")
        print(response.json())
        return None

# Example usage
create_github_release(
    owner="your-username",
    repo="your-repo",
    tag_name="v1.0.0",
    release_name="Initial Release",
    body="Description of the release",
    token="YOUR_GITHUB_TOKEN"
)
