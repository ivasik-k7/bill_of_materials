class Dependency:
    def __init__(
        self,
        name: str,
        version: str,
        description=None,
        license=None,
        homepage=None,
    ):
        self.name = name
        self.version = version
        self.description = description
        self.license = license
        self.homepage = homepage

    def __repr__(self):
        return f"<Dependency name='{self.name}', version='{self.version}'>"
