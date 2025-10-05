Flask File Manager - Development Branch (front) Setup Guide
This guide provides instructions on how to clone, set up the virtual environment, and run the Flask application from the dedicated front development branch.

Prerequisites
Before starting, ensure you have the following installed on your system:

Git: For cloning the repository.

Python 3.x: For running the Flask application.

1. Cloning the Project from the front Branch
Since the main working code is on the front branch, we will clone the repository using the branch flag (-b) to check out that branch immediately.

1.1. Create a clean working directory
Navigate to your desired project location and create a new, empty folder lbff = learnbookfromfile (e.g., lbff_front):

# Create the new, empty folder
```bash
mkdir lbff_front
cd lbff_front
```

1.2. Clone the Repository
Use the git clone -b command to clone the specific branch directly into your current directory (.):
```bash
git clone -b front https://github.com/acac27/learnbookfromfiles.git .
```
2. Setting Up the Python Environment
After cloning the code, you must create and activate a new virtual environment to manage project dependencies.

2.1. Create and Activate the Virtual Environment
Run these commands inside the flask_app_fresh directory:

# Create a new environment named 'env'
```bash
python -m venv env
```
# Activate the environment (PowerShell/CMD)
```bash
.\env\Scripts\activate
```
# (You should now see '(env)' at the start of your prompt)

2.2. Install Dependencies
Install the required framework, which is Flask:
```bash
pip install flask
```

2.3. Create the Uploads Folder
The application relies on an existing uploads folder for file handling:
```bash
mkdir uploads
```

3. Running the Application
With the environment set up and dependencies installed, you can now start the Flask server.
```bash
python app.py
```
Your file manager should be running at http://127.0.0.1:5000/.
The application should now be accessible in your web browser at:

http://127.0.0.1:5000/
