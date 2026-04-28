from app.app import create_app
from models.init_db import create_users_table

app = create_app()

if __name__ == "__main__":
    create_users_table()  # Create table on startup
    app.run(host="0.0.0.0", port=5000, debug=True)