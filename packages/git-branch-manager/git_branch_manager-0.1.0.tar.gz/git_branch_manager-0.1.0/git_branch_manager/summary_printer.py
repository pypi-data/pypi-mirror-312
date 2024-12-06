def print_summary(summary, remote_only, not_found):
    print("\nSummary:")

    if summary:
        print("\nDeleted branches:")
        print(f"{'Project link':<50} {'Branch name':<30} {'Scope':<20}")
        print("-" * 100)
        for repo in summary:
            for branch in repo['branches']:
                scope = " ".join(branch['scope'])
                print(f"{repo['repository']:<50} {branch['branch']:<30} {scope:<20}")

    if remote_only:
        print("\nRemote branches:")
        print(f"{'Project link':<50} {'Branch name':<30}")
        print("-" * 80)
        for entry in remote_only:
            print(f"{entry['repository']:<50} {entry['branch']:<30}")

    if not_found:
        print("\nNot Found Branches:")
        print(f"{'Branch name':<30}")
        print("-" * 30)
        for branch in not_found:
            print(f"{branch:<30}")
