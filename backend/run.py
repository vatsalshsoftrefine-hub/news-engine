from app.app import create_app
from models.init_db import create_users_table, create_news_table, create_interests_table, create_triggers_table

# Create app instance
app = create_app()

if __name__ == "__main__":
    # Initialize tables
    create_users_table()
    create_news_table()
    create_interests_table()
    create_triggers_table()

    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=True)