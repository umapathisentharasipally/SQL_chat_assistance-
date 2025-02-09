from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE_NAME = 'employee_database.db'  # Define database name as a constant

def create_database():
    """
    Creates an SQLite database and tables with sample data if they don't exist.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Department TEXT,
        Salary INTEGER,
        Hire_Date TEXT
    )
    ''')

    # Insert sample data into Employees (only if table is empty)
    cursor.execute("SELECT count(*) FROM Employees")
    if cursor.fetchone()[0] == 0:
        employees_data = [
            (1, 'Alice', 'Sales', 50000, '2021-01-15'),
            (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
            (3, 'Charlie', 'Marketing', 60000, '2022-03-20'),
            (4, 'nandhu', 'Engineering', 45000, '2024-03-20'),
            (5, 'Umapathi', 'Engineering', 60000, '2024-06-20'),
            (6, 'Ganapathi', 'Sales', 50000, '2022-01-15'),
            (7, 'Karthik', 'Engineering', 70000, '2020-05-10'),
            (8, 'Krishna', 'Marketing', 60000, '2021-03-20'),
        ]
        cursor.executemany("INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?, ?)", employees_data)

    # Create Departments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Manager TEXT
    )
    ''')

    # Insert sample data into Departments (only if table is empty)
    cursor.execute("SELECT count(*) FROM Departments")
    if cursor.fetchone()[0] == 0:
        departments_data = [
            (1, 'Sales', 'Alice'),
            (2, 'Engineering', 'Bob'),
            (3, 'Marketing', 'Charlie')
        ]
        cursor.executemany("INSERT INTO Departments (ID, Name, Manager) VALUES (?, ?, ?)", departments_data)

    conn.commit()
    conn.close()
    print("Database and tables created or ensured.")

def execute_query(sql_query):
    """
    Executes an SQL query against the database and returns the results.

    Args:
        sql_query (str): The SQL query to execute.

    Returns:
        list: List of tuples representing the query results, or None if error.
    """
    results = None  # Initialize results to None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Database error in execute_query: {e}") # More specific error message
        return None
    finally:
        print(f"SQL Query executed: {sql_query}") # Debugging print: SQL Query
        print(f"Query Results: {results}") # Debugging print: Query Results

def natural_language_to_sql(query):
    """
    Converts a natural language query to an SQL query.
    Revised version for more accurate department name extraction.
    """
    query = query.lower()
    sql_query = None
    query_type = "unknown"

    print(f"Debugging: Input query (lowercase): '{query}'")

    if "show me all employees in the" in query: # Look for "in the department"
        parts = query.split("show me all employees in the")
        if len(parts) > 1:
            department_part = parts[1].strip()
            print(f"Debugging: Department part before strip: '{department_part}'")
            department = department_part.replace("department", "").strip() # Remove "department" again just in case
            print(f"Debugging: Extracted department name: '{department}'")
            sql_query = f"SELECT * FROM Employees WHERE Department = '{department.capitalize()}'"
            query_type = "employees_in_department"
        else:
            sql_query = None
            print("Debugging: Could not extract department after 'in the department'")

    elif "who is the manager of the" in query: # Look for "of the department"
        parts = query.split("who is the manager of the")
        if len(parts) > 1:
            department_part = parts[1].strip()
            print(f"Debugging: Department part before strip: '{department_part}'")
            department = department_part.replace("department", "").strip() # Remove "department" again just in case
            print(f"Debugging: Extracted department name: '{department}'")
            sql_query = f"SELECT Manager FROM Departments WHERE Name = '{department.capitalize()}'"
            query_type = "department_manager"
        else:
            sql_query = None
            print("Debugging: Could not extract department after 'of the department'")


    elif "list all employees hired after" in query:
        date = query.split("after")[1].strip()
        sql_query = f"SELECT * FROM Employees WHERE Hire_Date > '{date}'"
        query_type = "employees_hired_after"

    elif "what is the total salary expense for the" in query:
        department = query.split("for the")[1].strip().replace("department", "").strip()
        sql_query = f"SELECT SUM(Salary) FROM Employees WHERE Department = '{department.capitalize()}'"
        query_type = "total_salary_expense"

    elif "show all employees" in query:
        sql_query = "SELECT * FROM Employees"
        query_type = "all_employees"
    elif "show all departments" in query:
        sql_query = "SELECT * FROM Departments"
        query_type = "all_departments"
    else:
        query_type = "unknown"

    print(f"Generated SQL Query: {sql_query}")
    print(f"Query Type: {query_type}")

    return sql_query
def format_results(results, query_type):
    """
    Formats the SQL query results into a user-friendly HTML string.

    Args:
        results (list): List of tuples from the SQL query.
        query_type (str): Type of query to format results appropriately.

    Returns:
        str: Formatted HTML string of the results.
    """
    if not results:
        return "<p>No results found.</p>"

    if query_type == "employees_in_department" or query_type == "employees_hired_after" or query_type == "all_employees":
        output = "<table>"
        output += "<tr><th>ID</th><th>Name</th><th>Department</th><th>Salary</th><th>Hire Date</th></tr>"
        for row in results:
            output += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
        output += "</table>"
        return output

    elif query_type == "department_manager":
        return f"<p>Manager: {results[0][0]}</p>"

    elif query_type == "total_salary_expense":
        return f"<p>Total Salary Expense: {results[0][0]}</p>"
    elif query_type == "all_departments":
        output = "<table>"
        output += "<tr><th>ID</th><th>Name</th><th>Manager</th></tr>"
        output += "<tr><th>ID</th><th>Name</th><th>Manager</th></tr>"
        for row in results:
            output += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        output += "</table>"
        return output

    return "<pre>" + str(results) + "</pre>" # Default formatting for unknown types


@app.route("/", methods=['GET', 'POST'])
def chat():
    """
    Flask route for the chat interface.
    Handles user input and displays assistant responses.
    """
    create_database() # Ensure database exists

    response_html = None # Initialize response_html outside the if block

    if request.method == 'POST':
        user_query = request.form['user_query']
        sql_query = natural_language_to_sql(user_query)

        if sql_query:
            results = execute_query(sql_query)
            if results is not None:
                query_type = "unknown" # Default query type
                if "SELECT * FROM Employees WHERE Department" in sql_query:
                    query_type = "employees_in_department"
                elif "SELECT Manager FROM Departments WHERE Name" in sql_query:
                    query_type = "department_manager"
                elif "SELECT * FROM Employees WHERE Hire_Date" in sql_query:
                    query_type = "employees_hired_after"
                elif "SELECT SUM(Salary) FROM Employees WHERE Department" in sql_query:
                    query_type = "total_salary_expense"
                elif "SELECT * FROM Employees" in sql_query:
                    query_type = "all_employees"
                elif "SELECT * FROM Departments" in sql_query:
                    query_type = "all_departments"

                response_html = format_results(results, query_type)
            else:
                response_html = "<p>An error occurred while accessing the database.</p>"
        else:
            response_html = "<p>Sorry, I didn't understand that query. Please try again.</p>"

    return render_template('chat.html', response=response_html) # Pass response_html to template


if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode