import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Base configuration class
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")