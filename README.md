# SQLite Chat Assistant

## Overview

This Python-based chat assistant allows users to query an SQLite database using natural language. It's built using Flask and SQLite3, and provides a simple web interface for interacting with employee and department data.

## Functionality

The chat assistant supports the following types of natural language queries:

*   **Show employees:**
    *   "Show all employees"
*   **Show employees by department:**
    *   "Show me all employees in the sales department."
    *    "Show me all employees in the Marketing department."
    *   "Show me all employees in the engineering department."
*   **List employees hired after a date:**
    *   "List all employees hired after [date]." (Date format: YYYY-MM-DD)
*   **Show departments:**
    *   "Show all departments"
*   **Get department manager:**
    *   "Who is the manager of the sales department"
    *   "Who is the manager of the engineering department"
    *  "Who is the manager of the marketing department"
*   **Calculate total salary expense for a department:**
    *   "What is the total salary expense for the sales department"
    *   "What is the total salary expense for the marketing department"
    *   "What is the total salary expense for the engineering department"
   

The assistant converts these natural language queries into SQL queries, executes them against the SQLite database (`employee_database.db`), and displays the results in a formatted HTML table or text.

## How it Works

1.  **Database Creation:** On startup, the Flask application creates an SQLite database file named `employee_database.db` (if it doesn't exist) and populates it with two tables: `Employees` and `Departments`, based on the schema provided in the assignment description. Sample data is inserted if the tables are empty.
2.  **Flask Web Interface:** The application uses Flask to create a simple web interface with a text input field and a display area for the assistant's responses. The HTML template (`chat.html`) is located in the `templates` folder.
3.  **Natural Language Processing (Basic):**  The `natural_language_to_sql` function in `app.py` takes the user's natural language query and uses simple string matching and splitting to convert it into an SQL query. This is a basic implementation and is designed to handle the specific query types listed above.
4.  **SQL Query Execution:** The `execute_query` function establishes a connection to the `employee_database.db`, executes the generated SQL query, fetches the results, and returns them to the Flask application.
5.  **Response Formatting:** The `format_results` function takes the raw SQL query results and formats them into user-friendly HTML output (tables or paragraphs) for display in the web interface.
6.  **Error Handling:** The assistant includes basic error handling for database errors and cases where it cannot understand the user's query. It returns informative messages in these situations.

## Steps to Run the Project Locally

1.  **Prerequisites:**
    *   Python 3.x installed on your system.
    *   pip package installer (usually comes with Python).

2.  **Installation:**
    *   Clone the repository to your local machine.
    *   Navigate to the project directory in your terminal: `cd your_project_directory`
    *   Install Flask: `pip install Flask`

3.  **Run the Application:**
    *   In your terminal, from the project directory, run the Flask application: `python app.py` (or the name of your Python file if you named it differently, e.g., `python aapp.py`)
    *   You should see output in the terminal indicating that the Flask app is running (e.g., "Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)").

4.  **Access the Chat Assistant:**
    *   Open your web browser and go to the URL provided in the terminal output (usually [http://127.0.0.1:5000](http://127.0.0.1:5000) or [http://localhost:5000](http://localhost:5000)).
    *   You should see the "SQLite Chat Assistant" web interface.
    *   Type your natural language queries in the input field and click "Send".

## Project Structure
chat/
app.py             (Python Flask application file)
employee_database.db  (SQLite database file - will be created when you run app.py)
templates/         (Folder for HTML templates)
chat.html      (HTML template for the chat interface)
README.md          (This file)

## Known Limitations and Suggestions for Improvement

*   **Limited Natural Language Understanding:** The current natural language processing is very basic and relies on simple string matching. It may not understand more complex or varied phrasing of the supported queries.
    *   **Improvement:**  Integrate a more robust NLP library (like spaCy or NLTK) or a more advanced natural language understanding model to handle a wider range of queries and variations in phrasing.

*   **Specific Query Types Only:** The assistant is designed to answer only the specific query types listed in the "Functionality" section. It will not be able to answer questions outside of these predefined types.
    *   **Improvement:**  Expand the `natural_language_to_sql` function to handle more query types and more complex questions. This could involve using more sophisticated parsing techniques or potentially incorporating a more advanced query understanding system.

*   **Error Handling is Basic:** Error handling is limited to catching database errors and unrecognised queries.
    *   **Improvement:**  Implement more comprehensive error handling, including input validation, more specific error messages for different types of invalid input, and potentially suggestions for how the user can rephrase their query.

*   **No Deployment Instructions:** This `README.md` does not include instructions for deploying the application to a public hosting platform.
    *   **Improvement:** Add deployment instructions for a platform like Heroku, PythonAnywhere, or a similar service to make the "Hosted Link" deliverable easier to achieve.

*   **Security:**  This is a simple demonstration application and does not include any security considerations.
    *   **Improvement (for real-world applications):** For a production application, security would be a major concern.  Implement appropriate security measures, especially if handling sensitive data, including input sanitization, protection against SQL injection (though parameterized queries in `execute_query` help with this), and secure deployment practices.
