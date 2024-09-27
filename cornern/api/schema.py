from ninja import Field, Schema

from .service import MeasurementService


class CornersOut(Schema):
    id: int
    name: str
    position: tuple[float, float]
    noiseValue: float = Field(..., alias="score")
    priceFactor: float = Field(..., alias="price_factor")

    @staticmethod
    def resolve_position(obj):
        return (obj.lat, obj.lon)


class ValueOut(Schema):
    timestamp: str
    value: float
    price_factor: float


class CornerOut(Schema):
    id: int
    name: str
    position: tuple[float, float]
    noise_value: float = Field(..., alias="score")
    noise_value_hour: list[ValueOut]
    noise_value_day: list[ValueOut]
    noise_value_week: list[ValueOut]
    price_factor: float
    description: str

    @staticmethod
    def resolve_position(obj):
        return (obj.lat, obj.lon)

    @staticmethod
    def resolve_noise_value_hour(obj):
        return MeasurementService.get_service().get_intervall(obj, 1, "5min", 12)

    @staticmethod
    def resolve_noise_value_day(obj):
        return MeasurementService.get_service().get_intervall(obj, 24, "1h", 24)

    @staticmethod
    def resolve_noise_value_week(obj):
        return MeasurementService.get_service().get_intervall(obj, 168, "1d", 7)


class MeasurementIn(Schema):
    value: int
    prediction: float
