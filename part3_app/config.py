import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def database_uri(instance_path: str) -> str:
        """Return DB URI preferring DATABASE_URL env var."""
        if db_url := os.getenv("DATABASE_URL"):
            return db_url
        return f"sqlite:///{os.path.join(instance_path, 'caregiver.db')}"

