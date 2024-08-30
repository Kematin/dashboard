from dataclasses import dataclass

from environs import Env


@dataclass(frozen=True)
class AdminConfig:
    username: str
    password: str


@dataclass(frozen=True)
class APIConfig:
    host: str
    port: int
    origins: list
    session_secret: str
    debug: bool


@dataclass(frozen=True)
class Database:
    db: str
    username: str
    password: str
    port: int
    host: str


@dataclass(frozen=True)
class Config:
    admin: AdminConfig
    api: APIConfig
    database: Database


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        admin=AdminConfig(
            username=env.str("ADMIN_USERNAME"), password=env.str("ADMIN_PASSWORD")
        ),
        api=APIConfig(
            host=env.str("HOST"),
            port=env.int("PORT"),
            origins=env.list("ORIGINS"),
            session_secret=env.str("SESSION_SECRET_KEY"),
            debug=env.bool("DEBUG"),
        ),
        database=Database(
            db=env.str("POSTGRES_DATABASE"),
            username=env.str("POSTGRES_USER"),
            password=env.str("POSTGRES_PASSWORD"),
            port=env.int("POSTGRES_PORT"),
            host=env.str("POSTGRES_HOST"),
        ),
    )


config = load_config()
