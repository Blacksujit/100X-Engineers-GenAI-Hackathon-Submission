"""
This is the entry point for the application.
The script performs the following tasks:
1. Imports necessary modules and functions.
2. Creates an instance of the application using the `create_app` function.
3. Ensures that the directories 'uploads' and 'models' exist, creating them if necessary.
4. Runs the application in debug mode on port 200.
If an exception occurs during the execution, it is logged as an error.
Modules:
    os: Provides a way of using operating system dependent functionality.
    logging: Provides a way to configure and use loggers.
Functions:
    create_app: A function imported from the app module to create an instance of the application.
Exceptions:
    Any exception that occurs during the execution is caught and logged.
"""
from app import create_app
import os
import logging

app = create_app()

if __name__ == "__main__":
    try:
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("models", exist_ok=True)
        app.run(debug=True, port=200)
    except Exception as e:
        logging.error(f"An error occurred: {e}")