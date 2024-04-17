from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "MyAIApp"
    DEBUG: bool = True

    # Database settings
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/mydatabase"

    # # Security settings
    # SECRET_KEY: str = "your_secret_key_here"  # Use a strong and unique secret key
    # Generate a random secret key
    SECRET_KEY = secrets.token_hex(32)

    print(SECRET_KEY)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30



# Create an instance of Settings
settings = Settings()