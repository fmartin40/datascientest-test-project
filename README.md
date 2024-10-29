# Datascientest | Test Project

## Introduction
This project is carried out as part of the Data Engineer (Datascientest) training program.

## Technology Used
1. Programming Language - Python
2. Scripting Language - SQL

## Code Structure
The project architecture is organized as follows:

```plaintext
datascientest-test-project/
│
├── env/                  # Virtual environment folder
│
├── src/                  # Source code of the application
│   ├── __init__.py       # File to mark the folder as a Python package
│   ├── main.py           # Main file of the application
│   ├── config.py         # Configuring and loading environment variables
│   ├── auth.py           # Authentication functions (for access token)
│   └── job_search.py     # Functions to interact with the Job Postings API
│
├── tests/                # Folder for unit tests
│   ├── __init__.py       # File to mark the folder as a package
│   └── test_main.py      # Test file for the code in main.py
│
├── requirements.txt      # List of project dependencies
│
├── README.md             # Project documentation
│
├── .env                  # Environment file for credentials
│
└── .gitignore            # File to ignore unnecessary files for Git
project_folder/
│


```

### Details of Directories and Files

- **env/** : Contains the virtual environment of the project. This directory is ignored by Git thanks to the `.gitignore` file.
- **src/** : Contains all the source code of the application, including the main entry point `main.py`.
- **tests/** : Contains unit tests and other automated tests to ensure code quality.
- **requirements.txt** : Lists the Python dependencies that the project uses. It can be used to quickly install all the necessary packages with `pip install -r requirements.txt`.
- **README.md** : Project documentation explaining its purpose, how to set it up, and how to use it.
- **.gitignore** : Defines files and directories that Git should ignore (such as the virtual environment and compiled files).

## GitHub Collaboration Rules

These rules define the collaboration process between the two users of the project. They aim to ensure effective and organized management of the source code and contributions.

1. Each user must clone the GitHub repository to start working locally.
2. Branches
- main branch : This branch contains the stable production code. No direct modifications are allowed on this branch.
- dev branch : This branch contains the development code.
- feature branches : For each new feature or bug fix, create a new branch with a descriptive name in CamelCase format.
- branch naming convention :  
`=> feature/NomFonctionnalite pour les nouvelles fonctionnalités.`  
`=> bugfix/NomCorrection pour les corrections de bugs.`
3. Commits
- Commit messages should be clear, concise, and in English. They should accurately describe the change made.
- Use the imperative in commit messages as if giving an order. For example: Add login feature.  
=> Example of a good commit message : `git commit -m "Fix user authentication issue"`
4. Pull Requests (PR)
- A Pull Request (PR) must be created for each new feature or bug fix, from the feature branch to dev.
- Add a clear description of the PR and refer to GitHub issues if necessary.
- PRs must be reviewed and approved by at least one other user before being merged.
- After approval, the PR can be merged into the dev branch.
- Once the PR is merged, delete the corresponding branch to avoid clutter.
