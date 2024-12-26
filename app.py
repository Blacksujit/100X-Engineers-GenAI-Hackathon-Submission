from app import create_app
import os
import logging

app = create_app()

if __name__ == "__main__":
    try:
        os.makedirs("uploads", exist_ok=True)
<<<<<<< HEAD
<<<<<<< HEAD
=======
        os.makedirs("models", exist_ok=True)
>>>>>>> 795a1e6 ( Errors are there in csv to video moddule will do tommorow ✅)
=======
>>>>>>> main
        app.run(debug=True, port=200)
    except Exception as e:
        logging.error(f"An error occurred: {e}")