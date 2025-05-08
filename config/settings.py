from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    database_url: str

    jwt_secret_key: str
    hash_algorithm: str

    merchant_id: str
    callback_url: str
    pay_url: str

    class Config:
        env_file = ".env"

settings = Settings()