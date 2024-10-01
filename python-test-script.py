import requests
import os

# GitHub API token (set in your GitHub Actions secrets or environment variables)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")  # PR ID from the GitHub Actions context
PROJECT_NUMBER = 1  # Replace with your project's number
COLUMN_NAME = 'To Do'  # Replace with your desired column name

# Set headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_project_id(repo_owner, repo_name, project_number):
    """Fetch the project ID from the project number."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/projects"
    response = requests.get(url, headers=headers)
    projects = response.json()
    
    for project in projects:
        if project['number'] == project_number:
            return project['id']
    raise Exception(f"Project {project_number} not found.")

def get_column_id(project_id, column_name):
    """Fetch the column ID from the column name."""
    url = f"https://api.github.com/projects/{project_id}/columns"
    response = requests.get(url, headers=headers)
    columns = response.json()

    for column in columns:
        if column['name'] == column_name:
            return column['id']
    raise Exception(f"Column {column_name} not found in project {project_id}.")

def add_pr_to_project(column_id, pr_id):
    """Add a pull request to a project column."""
    url = f"https://api.github.com/projects/columns/{column_id}/cards"
    payload = {
        "content_id": pr_id,
        "content_type": "PullRequest"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"Pull request {pr_id} successfully added to the project.")
    else:
        print(f"Failed to add PR to project. Response: {response.content}")

if __name__ == "__main__":
    # Get repository owner and name from the GITHUB_REPOSITORY environment variable
    repo_owner, repo_name = GITHUB_REPOSITORY.split("/")

    # Fetch the project ID
    project_id = get_project_id(repo_owner, repo_name, PROJECT_NUMBER)

    # Fetch the column ID
    column_id = get_column_id(project_id, COLUMN_NAME)

    # Add the pull request to the project column
    add_pr_to_project(column_id, PULL_REQUEST_ID)
