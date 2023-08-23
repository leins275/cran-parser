from packaging import version


class Package:
    name: str
    version: str 
    
    def __init__(self, name: str, version: str) -> None:
        self.name = name
        self.version = version

    def __eq__(self, __value: object) -> bool:
        if self.name == __value.name and self.version == __value.version:
            return True
        return False

    def __repr__(self) -> str:
        return f"{self.name} {self.version}"
