import random
from datetime import date, datetime, timedelta

from api.models import Measurement

sensors = []
sdt = datetime.combine(date.today(), datetime.min.time()) - timedelta(days=8)
edt = datetime.combine(date.today(), datetime.min.time()) + timedelta(days=1)

for sensor in sensors:
    while sdt < edt:
        Measurement.objects.create(value=random.randint(30, 100), prediction=0, sensor_id=2, created_at=sdt)
        sdt += timedelta(minutes=1)
