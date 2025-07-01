from enum import Enum

from pydantic_settings import BaseSettings


class Environments(Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


def get_configurations(env) -> dict:
    config_details = {
        Environments.LOCAL.value: {
        },
        Environments.DEV.value: {
        },
        Environments.PROD.value: {
        },
    }
    return config_details.get(env, {})
