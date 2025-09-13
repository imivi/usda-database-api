from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class EnvSchema(BaseSettings):
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = 6379

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


env = EnvSchema()

if __name__ == "__main__":
    print("env:", env.model_dump())
