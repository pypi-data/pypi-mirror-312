import os
from git_branch_manager.branch_operations import (
    get_local_branches,
    get_remote_branches,
    delete_local_branch,
    delete_remote_branch
)


def find_git_repos(basedirectory):
    git_repos = []
    for root, dirs, files in os.walk(basedirectory):
        if ".git" in dirs:
            git_repos.append(root)
    return git_repos
def process_repositories(branches, basedirectory, delete_remote):
    summary = []
    remote_only = []
    not_found = set(branches)

    repositories=find_git_repos(basedirectory)

    for repo_path in repositories:
        print(f"Processing repository: {repo_path}")
        repo_result = {'repository': repo_path, 'branches': []}

        try:
            os.chdir(repo_path)  # Change to repository directory

            # Fetch all local and remote branches
            local_branches = get_local_branches()
            remote_branches = get_remote_branches()

            # Process each branch
            for branch in branches:
                branch_result = {'branch': branch, 'scope': []}

                # Check for existence
                branch_exists_locally = branch in local_branches
                branch_exists_remotely = branch in remote_branches

                if branch_exists_locally:
                    if delete_local_branch(branch):
                        print(f"Deleted local branch: {branch}")
                        branch_result['scope'].append('local')

                if branch_exists_remotely:
                    if delete_remote and delete_remote_branch(branch):
                        print(f"Deleted remote branch: {branch}")
                        branch_result['scope'].append('remote')
                    elif not delete_remote:
                        remote_only.append({'repository': repo_path, 'branch': branch})

                # Remove branch from the not_found set if it exists locally or remotely
                if branch_exists_locally or branch_exists_remotely:
                    not_found.discard(branch)

                if branch_result['scope']:  # Add to summary if successfully deleted
                    repo_result['branches'].append(branch_result)

        except Exception as e:
            print(f"Error processing repository {repo_path}: {e}")

        if repo_result['branches']:  # Add repositories with successfully deleted branches
            summary.append(repo_result)

    return summary, remote_only, sorted(not_found)
