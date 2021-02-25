import os
import yaml
import conf
from pydantic import BaseModel
from typing import Optional

BASE_DIR: str = os.path.dirname(os.path.abspath(conf.__file__))
CONFIG_PATH: str = os.path.join(BASE_DIR, 'settings.yaml')


class DBSettings(BaseModel):
    HOST: str
    DATABASE: str
    PASSWORD: str
    USER: str


class Settings(BaseModel):

    MODE: str
    HOST: Optional[str] = '0.0.0.0'
    PORT: Optional[int] = 50051
    DB: DBSettings

    @classmethod
    def from_yaml(cls):
        with open(CONFIG_PATH, 'r') as f:
            return cls.parse_obj(yaml.full_load(f.read()))
