import subprocess


def get_local_branches():
    try:
        result = subprocess.check_output(['git', 'branch'], text=True).splitlines()
        return [branch.strip().lstrip('*').strip() for branch in result]
    except subprocess.CalledProcessError:
        return []


def get_remote_branches():
    try:
        result = subprocess.check_output(['git', 'ls-remote', '--heads', 'origin'], text=True).splitlines()
        return [line.split('/')[-1] for line in result]
    except subprocess.CalledProcessError:
        return []


def get_current_branch():
    try:
        result = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        return result
    except subprocess.CalledProcessError:
        return None


def delete_local_branch(branch_name):
    try:
        if branch_name == 'master':
            print("Cannot delete master branch.")
            return False

        current_branch = get_current_branch()
        if current_branch == branch_name:
            print(f"Currently checked out branch is '{branch_name}'. Switching to 'master' before deletion.")
            subprocess.check_output(['git', 'checkout', 'master'], stderr=subprocess.STDOUT)

        subprocess.check_output(['git', 'branch', '-D', branch_name], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error deleting local branch {branch_name}: {e}")
        return False


def delete_remote_branch(branch_name):
    try:
        if branch_name == 'master':
            print("Cannot delete master branch.")
            return False
        subprocess.check_output(['git', 'push', '--delete', 'origin', branch_name], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        print(f"Error deleting remote branch {branch_name}")
        return False
