import re
import datetime
import os

# Function to validate email format
def validate_email(email):
    """
    Function to validate email format.
    """
    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
        return True
    return False

# Function to validate Egyptian phone numbers
def validate_mobile(mobile):
    """
    Function to validate Egyptian phone numbers.
    """
    if re.match(r'^01[0-2]\d{8}$', mobile):
        return True
    return False

# Function to validate first name and last name
def validate_name(name):
    """
    Function to validate first name and last name.
    """
    if name and name.isalpha():
        return True
    return False

# Function to validate date format
def validate_date(date_text):
    """
    Function to validate date format.
    """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to generate a unique ID based on the number of lines in a file
def get_unique_id(filename):
    """
    Function to generate a unique ID based on the number of lines in a file.
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                last_id = int(last_line.split(",")[0])
                return last_id + 1
            else:
                return 1
    except FileNotFoundError:
        return 1

# Function to create files if they do not exist
def create_files_if_not_exist():
    """
    Function to create files if they do not exist.
    """
    files_to_create = ["user_credentials.txt", "projects.txt"]
    for file_name in files_to_create:
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                # Write headers if necessary
                if file_name == "user_credentials.txt":
                    file.write("user_id,first_name,last_name,email,password,mobile\n")
                elif file_name == "projects.txt":
                    file.write("project_id,user_id,title,details,total_target,start_date,end_date\n")
            print(f"File '{file_name}' created successfully.")

# Function to register a new user
def register_user():
    """
    Function to register a new user.
    """
    print("Please register to continue.")
    while True:
        first_name = input("Enter your First name: ").strip()
        if validate_name(first_name):
            break
        else:
            print("Invalid first name. Please try again.")
    while True:
        last_name = input("Enter your Last name: ").strip()
        if validate_name(last_name):
            break
        else:
            print("Invalid last name. Please try again.")
    while True:
        email = input("Enter your Email: ").strip()
        if validate_email(email):
            # Check if email already exists
            with open("user_credentials.txt", "r") as file:
                for line in file:
                    stored_email = line.strip().split(",")[3]
                    if email == stored_email:
                        print("This email is already registered. You can log in directly.")
                        return False
            break
        else:
            print("Invalid email format. Please try again.")
    while True:
        password = input("Enter your Password: ")
        confirm_password = input("Confirm your Password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")
    while True:
        mobile = input("Enter your Mobile phone number: ").strip()
        if validate_mobile(mobile):
            break
        else:
            print("Invalid mobile number format. Please try again.")

    # Generate unique ID
    user_id = get_unique_id("user_credentials.txt")

    # Save user details to file
    with open("user_credentials.txt", "a") as file:
        file.write(f"{user_id},{first_name},{last_name},{email},{password},{mobile}\n")

    print("Registration successful.")
    return True

# Function to create a new fundraising project
def create_project(user_id):
    """
    Function to create a new fundraising project.
    """
    print("Create a new project:")
    while True:
        title = input("Enter the project title: ").strip()
        if title:
            break
        else:
            print("Title cannot be empty. Please try again.")
    details = input("Enter project details: ").strip()
    while True:
        total_target = input("Enter the total target amount (e.g., 250000 EGP): ").strip()
        if total_target.isdigit():
            break
        else:
            print("Invalid total target amount. Please enter a valid number.")
    while True:
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        if validate_date(start_date):
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")
    while True:
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
        if validate_date(end_date) and end_date > start_date:
            break
        else:
            print("Invalid end date. End date must be after start date.")

    # Generate unique project ID
    project_id = get_unique_id("projects.txt")

    # Save project details to file
    with open("projects.txt", "a") as file:
        file.write(f"{project_id},{user_id},{title},{details},{total_target},{start_date},{end_date}\n")

    print("Project created successfully.")
    return True

# Function to view all projects
def view_all_projects():
    """
    Function to view all projects.
    """
    try:
        with open("projects.txt", "r") as file:
            for line in file:
                project_data = line.strip().split(",")
                print(f"Project ID: {project_data[0]}")
                print(f"Title: {project_data[2]}")
                print(f"Details: {project_data[3]}")
                print(f"Total Target Amount: {project_data[4]}")
                print(f"Start Date: {project_data[5]}")
                print(f"End Date: {project_data[6]}")
                print("-------------------------")
    except FileNotFoundError:
        print("No projects found.")

# Function to edit user's own projects
def edit_project(user_id):
    """
    Function to edit user's own projects.
    """
    project_id = input("Enter the project ID you want to edit: ")
    try:
        with open("projects.txt", "r") as file:
            projects = file.readlines()
        with open("projects.txt", "w") as file:
            project_found = False
            for project in projects:
                project_data = project.strip().split(",")
                if project_data[1] == str(user_id) and project_data[0] == project_id:
                    project_found = True
                    print("Select field to edit:")
                    print("1. Title")
                    print("2. Details")
                    print("3. Total Target Amount")
                    print("4. Start Date")
                    print("5. End Date")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        project_data[2] = input("Enter new title: ").strip()
                    elif choice == "2":
                        project_data[3] = input("Enter new details: ").strip()
                    elif choice == "3":
                        while True:
                            new_total_target = input("Enter new total target amount: ").strip()
                            if new_total_target.isdigit():
                                project_data[4] = new_total_target
                                break
                            else:
                                print("Invalid total target amount. Please enter a valid number.")
                    elif choice == "4":
                        while True:
                            new_start_date = input("Enter new start date (YYYY-MM-DD): ").strip()
                            if validate_date(new_start_date):
                                project_data[5] = new_start_date
                                break
                            else:
                                print("Invalid date format. Please use YYYY-MM-DD.")
                    elif choice == "5":
                        while True:
                            new_end_date = input("Enter new end date (YYYY-MM-DD): ").strip()
                            if validate_date(new_end_date) and new_end_date > project_data[5]:
                                project_data[6] = new_end_date
                                break
                            else:
                                print("Invalid end date. End date must be after start date.")
                    else:
                        print("Invalid choice. No fields updated.")
                        return False

                    file.write(','.join(project_data) + '\n')
                    print("Project updated successfully.")
                else:
                    file.write(project)  # Write unchanged project back to file
            if not project_found:
                print("Sorry, you are not the owner of this project.")
    except FileNotFoundError:
        print("No projects found.")

# Function to delete user's own projects
def delete_project(user_id):
    """
    Function to delete user's own projects.
    """
    project_id = input("Enter the project ID you want to delete: ")
    try:
        with open("projects.txt", "r") as file:
            projects = file.readlines()
        found_project = False
        with open("projects.txt", "w") as file:
            for project in projects:
                project_data = project.strip().split(",")
                if project_data[1] == str(user_id) and project_data[0] == project_id:
                    print("Project deleted successfully.")
                    found_project = True
                else:
                    file.write(project)
        if not found_project:
            print("Sorry, you are not the owner of this project.")
    except FileNotFoundError:
        print("No projects found.")

# Function to search for projects by date
def search_project_by_date():
    """
    Function to search for projects by date.
    """
    search_date = input("Enter the date (YYYY-MM-DD) to search for projects: ")
    try:
        with open("projects.txt", "r") as file:
            found = False
            for line in file:
                project_data = line.strip().split(",")
                if project_data[5] <= search_date <= project_data[6]:
                    print(f"Project ID: {project_data[0]}")
                    print(f"Title: {project_data[2]}")
                    print(f"Details: {project_data[3]}")
                    print(f"Total Target Amount: {project_data[4]}")
                    print(f"Start Date: {project_data[5]}")
                    print(f"End Date: {project_data[6]}")
                    print("-------------------------")
                    found = True
            if not found:
                print("No projects found for the given date range.")
    except FileNotFoundError:
        print("No projects found.")

# Main menu of the crowdfunding app
def main_menu():
    """
    Main menu of the crowdfunding app.
    """
    print("Welcome to the Crowdfunding App!")
    logged_in = False
    user_id = None
    while True:
        if logged_in:
            print("\n1. View all projects")
            print("2. Create a project")
            print("3. Edit project")
            print("4. Delete project")
            print("5. Search project by date")
            print("6. Logout")
            print("7. Exit")
        else:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")
        choice = input("Enter your choice: ")
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        if logged_in:
            if choice == "1":
                view_all_projects()
            elif choice == "2":
                create_project(user_id)
            elif choice == "3":
                edit_project(user_id)
            elif choice == "4":
                delete_project(user_id)
            elif choice == "5":
                search_project_by_date()
            elif choice == "6":
                print("Logged out successfully.")
                logged_in = False
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            if choice == "1":
                logged_in, user_id = login_user()
            elif choice == "2":
                register_user()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

# Function to log in existing user
def login_user():
    """
    Function to log in existing user.
    """
    print("Please login.")
    while True:
        email = input("Enter your Email: ").strip()
        if validate_email(email):
            break
        else:
            print("Invalid email format. Please try again.")
    
    # Check if email exists
    email_exists = False
    with open("user_credentials.txt", "r") as file:
        for line in file:
            stored_email = line.strip().split(",")[3]
            if email == stored_email:
                email_exists = True
                break
    
    if not email_exists:
        print("You are a new user. Your email is not registered. Please register first.")
        return False, None
    
    password = input("Enter your Password: ")

    # Check credentials
    with open("user_credentials.txt", "r") as file:
        for line in file:
            user_data = line.strip().split(",")
            stored_email, stored_password, user_id = user_data[3], user_data[4], user_data[0]
            if email == stored_email and password == stored_password:
                print("Login successful!")
                return True, user_id
    print("Invalid email or password. Please try again.")
    return False, None


if __name__ == "__main__":
    create_files_if_not_exist()
    main_menu()
