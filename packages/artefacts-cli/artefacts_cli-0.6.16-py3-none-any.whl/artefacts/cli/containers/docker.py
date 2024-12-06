from collections.abc import Generator
import json
import os
from pathlib import Path
from typing import Any, Tuple
from uuid import uuid4

from artefacts.cli.constants import DEFAULT_API_URL
from artefacts.cli.containers import CMgr
from artefacts.cli.utils import ensure_available

ensure_available("docker")

import docker
from docker import APIClient


class DockerManager(CMgr):
    def __init__(self):
        self.client = APIClient()

    def build(self, **kwargs) -> Tuple[str, Generator]:
        kwargs["tag"] = kwargs.pop("name")
        logs = []
        img_id = None
        for entry in self.client.build(**kwargs):
            line_data = [
                json.loads(v) for v in entry.decode("utf-8").split("\r\n") if len(v) > 0
            ]
            for data in line_data:
                if "stream" in data:
                    line = data["stream"].strip()
                    if not line.startswith("---") and len(line) > 0:
                        print(line)
                        logs.append(line)
                elif "aux" in data and "ID" in data["aux"]:
                    img_id = data["aux"]["ID"]
        if img_id is None:
            img_id = self.client.inspect_image(kwargs["tag"])["Id"]
        return img_id, iter(logs)

    def run(
        self,
        image: str,
        project: str,
        jobname: str = None,
        artefacts_dir: str = Path("~/.artefacts").expanduser(),
        api_url: str = DEFAULT_API_URL,
    ) -> Tuple[Any, Generator]:
        if not self._valid_artefacts_api_key(project, artefacts_dir):
            return None, iter(
                [
                    "Missing API key for the project. Does `~/.artefacts/config` exist and contain your key?"
                ]
            )
        try:
            env = {
                "JOB_ID": str(uuid4()),
                "ARTEFACTS_JOB_NAME": jobname,
                "ARTEFACTS_API_URL": api_url,
            }

            container = self.client.create_container(
                image,
                environment=env,
                detach=False,
                volumes=["/root/.artefacts"],
                host_config=self.client.create_host_config(
                    binds={
                        artefacts_dir: {
                            "bind": "/root/.artefacts",
                            "mode": "ro",
                        },
                    },
                ),
            )
            self.client.start(container=container.get("Id"))
            for entry in self.client.logs(container=container.get("Id"), stream=True):
                print(entry.decode("utf-8").strip())
            return container, iter([])
        except docker.errors.ImageNotFound:
            return None, iter(
                [f"Image {image} not found by Docker. Perhaps need to build first?"]
            )
        except Exception as e:
            return None, iter([f"Failed to run from {image}. All we know: {e}"])
