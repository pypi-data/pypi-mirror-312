# Git Branch Manager

## Description
`git-branch-manager` is a Python package that automates the process of managing Git repositories. It allows you to search for Git repositories in a specified directory and delete specified branches locally and/or remotely.

## Features
- Automatically search for Git repositories under a specified base directory.
- Delete specified branches locally.
- Optionally delete branches from remote repositories.

## Installation
Install the package using pip:

```bash
pip install git-branch-manager
```

## Usage
Run the command in your terminal as follows:

```bash
git-branch-manager <basedirectory> <branches> [--remote]
```

### Arguments:
- `<basedirectory>`: The base directory to search for Git repositories.
- `<branches>`: Comma-separated list of branches to delete.
- `--remote`: Optional. Include this flag to delete branches from remote repositories.

### Example:
To delete branches `feature1` and `feature2` locally and remotely under the `/my/projects` directory:

```bash
git-branch-manager /my/projects feature1,feature2 --remote
```

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Dhruba Dahal
