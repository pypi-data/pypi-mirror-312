import tempfile
import zipfile
import tomllib

from dataclasses import dataclass
from contextlib import contextmanager
from urllib.request import urlretrieve
from typing import List


def make_url(tag):
    return f"https://codeberg.org/api/packages/helge/generic/fediverse-features/{tag}/fediverse_features.zip"


@contextmanager
def fediverse_features_archive(tag):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = f"{tmpdirname}/features.zip"
        urlretrieve(make_url(tag), filename)
        with zipfile.ZipFile(filename) as fp:
            yield fp


@dataclass
class Config:
    tag: str
    features: List[str]


def load_config() -> Config:
    with open("fediverse-features.toml", "rb") as fp:
        data = tomllib.load(fp)
    return Config(tag=data["tag"], features=data["features"])
