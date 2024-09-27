from ninja import Field, Schema


class CornersOut(Schema):
    id: int
    name: str
    position: tuple[float, float]
    noiseValue: float = Field(..., alias="score")

    @staticmethod
    def resolve_position(obj):
        return (obj.lat, obj.lon)


class CornerOut(Schema):
    id: int
    name: str
    position: tuple[float, float]
    noiseValue: float = Field(..., alias="score")
    description: str

    @staticmethod
    def resolve_position(obj):
        return (obj.lat, obj.lon)