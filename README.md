# TutorMe
For CSIT321

## Pre-requisites
- Github Account
- Code Editor
- Python 3
- Web Browser

## Start Guide
1. Install git: https://git-scm.com/downloads.
2. Set up your git with your github account.
2. Install pipenv in the command line: `pip3 install pipenv`
  - Make sure folder to Python3 is configured in your PATH.
2. Go to directory or folder to put project.
3. Run these commands in bash or command line:
```
git clone https://github.com/e6654321/TutorMe.git
cd TutorMe
pipenv install django~=3.1.0
pipenv shell
```
4. Go to 'backend' folder: `cd backend`
5. Run this command to start server: `python manage.py runserver`
6. Go to the address specified (http://127.0.0.1:8000/) to see development site.

## Pushing Edits
1. *Be sure that everything runs after all the edits.*
2. Go to bash or command line and run these commands:
```
git checkout -b "LastName/branch-name"
git pull origin master
git add .
git commit -m "[LastName] Message about this commit"
git push --set-upstream origin LastName/branch-name
```
3. Go to github and sign in to your account.
4. Go to the repository (https://github.com/e6654321/TutorMe).
5. Go to *Pull requests*.
6. Create pull request for your branch.
7. Tag @e6654321 as reviewer.
