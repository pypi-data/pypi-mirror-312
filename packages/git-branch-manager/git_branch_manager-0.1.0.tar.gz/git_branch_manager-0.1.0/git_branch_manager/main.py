import argparse
from git_branch_manager.repository_operations import process_repositories
from git_branch_manager.summary_printer import print_summary


def main():
    parser = argparse.ArgumentParser(description="Delete Git branches based on a YAML configuration.")
    parser.add_argument('--remote', action='store_true', help="Delete branches from remote as well.")
    parser.add_argument("basedirectory", help="The base directory to search for Git repositories.")
    parser.add_argument("branches", help="Comma-separated list of branches to delete (local and/or remote).")

    args = parser.parse_args()
    
    branches = [branch.strip() for branch in args.branches.split(",")]
    basedirectory = args.basedirectory

    summary, remote_only, not_found = process_repositories(branches, basedirectory, args.remote)
    print_summary(summary, remote_only, not_found)


if __name__ == "__main__":
    main()
