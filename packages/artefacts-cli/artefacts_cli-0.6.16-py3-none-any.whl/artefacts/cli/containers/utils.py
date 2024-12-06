from collections.abc import Generator
import logging
from typing import Any, Tuple

from artefacts.cli.containers import CMgr


class ContainerMgr:
    SUPPORTED_PRIORITISED_ENGINES = {
        1: "docker",
        # 2: "podman",
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mgr = self._configure()
        if self.mgr is None:
            raise Exception(
                f"Failed to find supported container stack. Please install and start one in {list(self.SUPPORTED_PRIORITISED_ENGINES.values())}, with default settings (custom sockets not supported at this stage)"
            )

    def _configure(self) -> CMgr:
        manager = None
        for idx in sorted(self.SUPPORTED_PRIORITISED_ENGINES):
            engine = self.SUPPORTED_PRIORITISED_ENGINES[idx]
            try:
                handler = getattr(self, f"_configure_{engine}")
                manager = handler()
            except AttributeError:
                self.logger.warning(
                    f"Tried to detect an unsupported engine: {engine}. WIP? Ignore and continue."
                )
            except Exception as e:
                self.logger.warning(
                    f"Problem in detecting {engine} ({e}) Ignore and continue."
                )
            if manager is not None:
                break
        return manager

    def _configure_docker(self):
        from artefacts.cli.containers.docker import DockerManager

        return DockerManager()

    # def _configure_podman(self):
    #     from artefacts.cli.containers import podman
    #     return PodmanManager()

    def build(self, **kwargs) -> Tuple[str, Generator]:
        return self.mgr.build(**kwargs)

    def run(self, **kwargs) -> Tuple[Any, Generator]:
        return self.mgr.run(**kwargs)
