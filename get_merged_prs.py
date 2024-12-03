import requests
import sys
import re

def parse_github_url(url):
    """
    Parse the GitHub repository URL and extract the owner and repository name.
    """
    match = re.match(r"https?://github.com/([^/]+)/([^/]+)", url)
    if not match:
        raise ValueError("Invalid GitHub URL. Please provide a valid repository URL.")
    return match.group(1), match.group(2)

def get_merged_prs(repo_owner, repo_name):
    """
    Fetch merged pull requests grouped by developer for the given repository.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    params = {
        "state": "closed",  # Only closed PRs
        "per_page": 100,    # Max items per page (paginate if necessary)
    }
    headers = {
        "Accept": "application/vnd.github+json",
    }
    
    prs_by_user = {}

    while url:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        prs = response.json()
        
        for pr in prs:
            merged_at = pr.get("merged_at")
            if merged_at:  # Check if the PR was merged
                user = pr["user"]["login"]
                pr_number = pr["number"]
                prs_by_user.setdefault(user, []).append({
                                    "number": pr_number,
                                    "merged_at": merged_at
                })
        # Pagination: Get the 'next' link from the response headers
        url = response.links.get("next", {}).get("url")
    
    return prs_by_user

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <GitHub-Repository-URL>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    try:
        repo_owner, repo_name = parse_github_url(repo_url)
    except ValueError as e:
        print(e)
        sys.exit(1)

    prs_by_user = get_merged_prs(repo_owner, repo_name)
    for user, prs in prs_by_user.items():
        print(f"Developer: {user}")
        for pr in prs:
            print(f"  PR #{pr['number']} merged on {pr['merged_at']}")

if __name__ == "__main__":
    main()

