from collections.abc import Generator
import configparser
import os
from pathlib import Path
from typing import Any, Tuple, Union

from artefacts.cli.constants import DEFAULT_API_URL


class CMgr:
    def build(self, **kwargs) -> Tuple[str, Generator]:
        """
        Returns the build image ID (e.g. sha256:abcdefghi)
        and an iterator over the build log entries.
        """
        raise NotImplemented()

    def run(
        self,
        image: str,
        project: str,
        jobname: str = None,
        artefacts_dir: str = Path("~/.artefacts").expanduser(),
        api_url: str = DEFAULT_API_URL,
    ) -> Tuple[Any, Generator]:
        """
        Returns a container (Any type as depends on the framework)
        and an iterator over the container log entries.
        """
        raise NotImplemented()

    def _valid_artefacts_api_key(
        self, project: str, path: Union[str, Path] = Path("~/.artefacts").expanduser()
    ) -> bool:
        """
        Check if a valid API key is available to embed in containers.

        1. Check overrides with the ARTEFACTS_KEY environment variable.
        2. If `path` is not given, check the default .artefacts folder for the config file.
        3. If `path` is given, check the file directly is a file, or check for a `config` file if a folder.

        When a config file is found, we check here if the API key for the `project` is available.

        `path` set to None is an error, and aborts execution.
        """
        if not path:
            raise Exception(
                "`path` must be a string, a Path object, or exclusded from the kwargs"
            )
        if os.environ.get("ARTEFACTS_KEY", None):
            return True
        path = Path(path)  # Ensure we have a Path object
        config = configparser.ConfigParser()
        if path.is_dir():
            config.read(path / "config")
        else:
            config.read(path)
        try:
            return config[project].get("apikey") != None
        except KeyError:
            return False
