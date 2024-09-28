from ninja import NinjaAPI
from ninja.security import HttpBasicAuth

from .models import Corner, Measurement, Sensor
from .schema import CornerOut, CornersOut, MeasurementIn, NextOut
from .service import MeasurementService

api = NinjaAPI()


class SensorBasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        sensor = Sensor.objects.filter(name=username).first()
        if sensor and str(sensor.token) == password:
            return sensor


@api.get("/corner", response=list[CornersOut])
def corners(request):
    return list(Corner.objects.all())


@api.get("/corner/{corner_id}", response=CornerOut)
def corner(request, corner_id: int):
    return Corner.objects.get(id=corner_id)


@api.get("/next", response=NextOut)
def corner_next(request):
    return {"timestamp": MeasurementService.get_service().get_next()}


@api.post("/measurement", auth=SensorBasicAuth())
def create_measurement(request, measurement: MeasurementIn):
    Measurement.objects.create(**measurement.dict(), sensor=request.auth)
    return {}
