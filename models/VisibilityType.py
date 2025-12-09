from enum import Enum

class VisibilityType(Enum):
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    PACKAGE = "package"
    UNSPECIFIED = "Unspecified"

    def get_type(self) -> str:
        return self.value

    @staticmethod
    def get_type_from_string(value: str) -> "VisibilityType":
        for v in VisibilityType:
            if v.value.lower() == value.lower():
                return v
        return VisibilityType.PRIVATE
