from datetime import datetime, timedelta

import pandas as pd

from .models import Corner, Measurement


class MeasurementService:
    @classmethod
    def get_service(cls):
        return cls()

    def get_intervall(self, corner: Corner, hours: int, frequency: str, count: int):
        m_qs = Measurement.objects.filter(
            created_at__gte=datetime.now().replace(second=0, microsecond=0, minute=0) - timedelta(hours=hours + 1),
            sensor__corner=corner,
        ).values("created_at", "value")

        df = pd.DataFrame(m_qs).set_index("created_at").resample(frequency).mean().round(1).tail(count)

        return [{"timestamp": t.isoformat(), "value": v} for t, v in df.to_dict().get("value", {}).items()]
