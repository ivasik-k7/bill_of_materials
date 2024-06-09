import os
from abc import ABC, abstractmethod

from app.informer import (
    PackageInfoInformer,
    PubPackageInfoInformer,
    PyPackageInfoInformer,
)
from app.models import Dependency
from app.utils import get_logger

logger = get_logger(__name__)


class DependenciesParser(ABC):
    def __init__(self, path: str) -> None:
        self.path = path
        self._validate_path()
        self._informer: PackageInfoInformer = self._create_informer()

    def _validate_path(self) -> None:
        if not os.path.isfile(self.path):
            raise FileNotFoundError(f"The file at path {self.path} does not exist.")

    @abstractmethod
    def parse(self) -> dict:
        raise NotImplementedError("The abc method has not been implemented!")

    @abstractmethod
    def _create_informer(self):
        raise NotImplementedError(
            "The abstract method _create_informer has not been implemented!"
        )


class TomlDependenciesParser(DependenciesParser):
    def _validate_path(self) -> None:
        super()._validate_path()
        if not self.path.endswith(".toml"):
            raise ValueError(f"The file at path {self.path} is not a .toml file.")

    def _create_informer(self):
        return PyPackageInfoInformer()

    def parse(self) -> dict:
        import tomllib

        dependencies = []

        with open(self.path, "rb") as f:
            data = tomllib.load(f)

        for _, info in data.items():
            document_dependencies = info.get("poetry", {}).get("dependencies", {})
            for name, version in document_dependencies.items():
                package_info = self._informer.request_info(name)

                if not package_info:
                    continue

                object = Dependency(
                    name=name,
                    version=version,
                    description=package_info.get("info", {}).get("summary", ""),
                    homepage=package_info.get("info", {}).get("package_url", ""),
                    license=package_info.get("info", {}).get("license", ""),
                )

                dependencies.append(object)

        return dependencies


class TextDependenciesParser(DependenciesParser):
    def _validate_path(self) -> None:
        super()._validate_path()
        if not self.path.endswith(".txt"):
            raise ValueError(f"The file at path {self.path} is not .txt file.")

    def _create_informer(self):
        return PyPackageInfoInformer()

    def parse(self):
        dependencies = []
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.startswith("-e"):
                        continue
                        # try:
                        #     dep = line.split("#egg=")[-1]
                        #     dependencies[dep] = line
                        # except IndexError:
                        #     logger.warning(f"Invalid VCS line format: {line}")
                    else:
                        try:
                            if "==" in line:
                                name, version = line.split("==")
                            elif ">=" in line:
                                name, version = line.split(">=")
                            elif "<=" in line:
                                name, version = line.split("<=")
                            elif "~=" in line:
                                name, version = line.split("~=")
                            elif "!=" in line:
                                name, version = line.split("!=")
                            else:
                                name, version = line, ""

                            info = self._informer.request_info(name).get("info", {})

                            object = Dependency(
                                name=name,
                                version=version,
                                description=info.get("summary", ""),
                                license=info.get("license", ""),
                                homepage=info.get("package_url", ""),
                            )

                            dependencies.append(object)
                        except ValueError:
                            logger.warning(f"Invalid dependency line format: {line}")
        return dependencies


class YamlDependenciesParser(DependenciesParser):
    def _validate_path(self) -> None:
        super()._validate_path()
        if not self.path.endswith(".yml") or not self.path.endswith(".yaml"):
            raise ValueError(f"The file at path {self.path} is not .yml file.")

    def _create_informer(self):
        return PubPackageInfoInformer()

    def parse(self):
        import yaml

        with open(self.path, "r") as f:
            return yaml.safe_load(f)


class ParserContext:
    def __init__(self, path: str) -> None:
        self.path = path
        self.parser = self._get_parser()

    def _get_parser(self) -> DependenciesParser:
        if self.path.endswith(".toml"):
            return TomlDependenciesParser(self.path)
        elif self.path.endswith(".txt"):
            return TextDependenciesParser(self.path)
        elif self.path.endswith(".yml") or self.path.endswith(".yaml"):
            return YamlDependenciesParser(self.path)
        else:
            raise ValueError(f"Unsupported file extension for file: {self.path}")

    def __enter__(self) -> DependenciesParser:
        return self.parser

    def __exit__(self, exc_type, exc_value, traceback):
        pass
