from dataclasses import dataclass

from environs import Env


@dataclass
class AdminConfig:
    username: str
    password: str


@dataclass
class APIConfig:
    host: str
    port: int
    origins: list


@dataclass
class Config:
    admin: AdminConfig
    api: APIConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        admin=AdminConfig(
            username=env.str("ADMIN_USERNAME"), password=env.str("ADMIN_PASSWORD")
        ),
        api=APIConfig(
            host=env.str("HOST"), port=env.int("PORT"), origins=env.list("ORIGINS")
        ),
    )


config = load_config()
