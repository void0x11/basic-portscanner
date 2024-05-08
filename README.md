[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/IvIaveIG)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=12669896&assignment_repo_type=AssignmentRepo)
**Objective:** The objective of this assignment is to create a Python script for a port scanner, which provides functionality for scanning target hosts and ports, saving scan results, and retrieving saved scan results. Students will demonstrate their understanding of network programming, user interaction, file handling, and data serialization in Python.  

Be sure to follow cybersecurity best practices and ethics when testing and using this script.  Only use it again devices that you have permission/authorization to scan.  See: SANS - Ethics and Legality of Port Scanning

**Requirements:**
- Main Menu: Create a user-friendly main menu that remains available until the user chooses to exit the program.

**Target Scanning:**
- Prompt the user to enter a target host or a range of target hosts to scan.
- Scan all provided target hosts.
- Provide feedback on whether each target is active or not.

**Port Scanning:**
- Prompt the user to enter a single port or a range of ports to scan.
- Scan all provided ports for each target.
- Present results on whether the ports are open or not.

**Saving Scan Results:**
- Save all scan results as separate JSON files.
- Files should be named with the date and target for easy identification.
- Create a directory for saving scan result files in.

**Retrieving Scan Results:**
- Implement functionality that allows the user to retrieve and display saved scan results.
- Present a list of all saved scan result files.
- Allow the user to select a file and display its contents.
- When displaying file contents, only display the open ports for the target(s)

**Only use standard library imports:**
- Only standard Python library imports may be used.  




**Grading Rubric:**

This assignment can be graded on the following criteria:

**Functionality (40 points):**

Main menu and user interaction (10 points)
Target scanning and feedback (10 points)
Port scanning and feedback (10 points)
Saving scan results as JSON files (5 points)
Retrieving and displaying saved scan results (5 points)

**Code Quality (20 points):**

Code organization and structure (5 points)
Proper use of functions (5 points)
Use of appropriate variable names and comments (5 points)
Error handling and robustness (5 points)

**Documentation (10 points):**

Clear and concise explanation of the code's purpose and usage (5 points)
In-code comments and explanations (5 points)

**Directory Creation and File Management (10 points):**

The script should create a results directory if it doesn't exist (5 points).
Proper handling of file operations, such as saving and retrieving scan results (5 points).

**Presentation (10 points):**

A fully functioning and error free script is submitted (10 points)

**Creativity and Additional Features (10 points):**

Implement additional features beyond the basic requirements (e.g., displaying scan results in a user-friendly format)

**Total: 100 points**




**Note:**

Be sure to test and troubleshoot your program before submitting it.  If the program is executed and raises any unhandled errors while being graded, it will be graded as a late submission.  

All code must be completed and uploaded to GitHub by the due date.  Code that is not in GitHub by the due date will be considered late.  Additionally, code submissions will not be accepted outside of GitHub (ex: email or Canvas messages).

Only standard Python library imports may be used.  Scripts that install and import third party modules/packages will have points deducted.  
