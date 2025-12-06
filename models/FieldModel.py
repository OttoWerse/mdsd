class FieldModel:
    name: str
    type: TypeModel
    visibility: VisibilityModel = VisibilityModel.PUBLIC
    is_static: bool = False
    is_final: bool = False

    def __str__(self):
        mods = []
        if self.is_static:
            mods.append("static")
        if self.is_final:
            mods.append("final")

        modifiers = " ".join(mods)
        return f"{self.visibility.value} {modifiers} {self.type.name} {self.name}".strip()
