import os
from uuid import uuid4

import pytest

from artefacts.cli import app_containers as containers


def test_container_package_exists(cli_runner):
    result = cli_runner.invoke(containers.package, [])
    assert result.exit_code == 0


def test_container_package_build_specific_dockerfile(
    cli_runner, dockerfile_available, docker_mocker
):
    dockerfile = "non_standard_dockerfile"
    result = cli_runner.invoke(
        containers.package, ["build", "--dockerfile", dockerfile]
    )
    dockerfile_available.assert_any_call(os.path.join(".", dockerfile))
    assert result.exit_code == 0


def test_container_package_build_specific_dockerfile_missing(
    cli_runner, dockerfile_not_available
):
    dockerfile = "non_standard_dockerfile"
    result = cli_runner.invoke(
        containers.package, ["build", "--dockerfile", dockerfile]
    )
    dockerfile_not_available.assert_any_call(os.path.join(".", dockerfile))
    assert result.exit_code == 1
    assert (
        result.output.strip()
        == f"Error: No {dockerfile} found here. I cannot build the package."
    )


def test_container_package_build_specific_image_name(
    cli_runner, dockerfile_available, docker_mocker
):
    name = str(uuid4())
    before = len(docker_mocker.images())
    result = cli_runner.invoke(containers.package, ["build", "--name", name])
    assert result.exit_code == 0
    assert len(docker_mocker.images()) == before + 1
    assert docker_mocker.get_image(name).Repository == name


def test_container_package_build_default_image_name(
    cli_runner, dockerfile_available, docker_mocker
):
    before = len(docker_mocker.images())
    result = cli_runner.invoke(containers.package, ["build"])
    assert result.exit_code == 0
    assert len(docker_mocker.images()) == before + 1
    assert docker_mocker.get_image("artefacts") is not None
