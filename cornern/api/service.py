from datetime import datetime, timedelta, timezone

import pandas as pd

from .models import Corner, Measurement


class MeasurementService:
    @classmethod
    def get_service(cls):
        return cls()

    def get_intervall(self, corner: Corner, hours: int, frequency: str, count: int, default: int = 40):
        m_qs = Measurement.objects.filter(
            created_at__gte=datetime.now().replace(second=0, microsecond=0, minute=0) - timedelta(hours=hours + 1),
            sensor__corner=corner,
        ).values("created_at", "value")

        ms = list(m_qs)
        ms.insert(0, {"created_at": datetime.now(timezone.utc) - timedelta(hours=hours + 1), "value": default})
        ms.append({"created_at": datetime.now(timezone.utc), "value": default})

        df = (
            pd.DataFrame(ms, columns=["created_at", "value"])
            .set_index("created_at")
            .resample(frequency)
            .mean()
            .fillna(default)
            .round(1)
            .tail(count)
        )

        return [
            {
                "timestamp": t.isoformat(),
                "value": v,
                "price_factor": round(min(max(0.0216667 * v - 0.1668, 0.7), 2.0), 1),
            }
            for t, v in df.to_dict().get("value", {}).items()
        ]

    def get_next(self):
        dt = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        mins = dt.minute // 5 * 5
        return (dt.replace(minute=mins) + timedelta(minutes=5)).isoformat()
