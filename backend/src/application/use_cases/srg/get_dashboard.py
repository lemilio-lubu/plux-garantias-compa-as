from application.dto.dashboard import DashboardDTO, StatusCount, TypeStatusCount
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType


class GetDashboardUseCase:
    """Read-model query — bypasses domain entities, returns aggregated stats directly."""

    def __init__(self, repository) -> None:
        self._repository = repository

    def execute(self, concesionaria: str) -> DashboardDTO:
        raw = self._repository.get_dashboard_stats(concesionaria)

        total = sum(row["count"] for row in raw)

        by_status_map: dict[str, int] = {s.value: 0 for s in SrgStatus}
        by_type_map: dict[str, int] = {t.value: 0 for t in SrgType}
        breakdown: list[TypeStatusCount] = []

        for row in raw:
            by_status_map[row["status"]] = by_status_map.get(row["status"], 0) + row["count"]
            by_type_map[row["srg_type"]] = by_type_map.get(row["srg_type"], 0) + row["count"]
            breakdown.append(TypeStatusCount(
                srg_type=row["srg_type"],
                status=row["status"],
                count=row["count"],
            ))

        by_status = [StatusCount(status=k, count=v) for k, v in by_status_map.items()]

        return DashboardDTO(
            concesionaria=concesionaria,
            total=total,
            by_status=by_status,
            by_type=by_type_map,
            breakdown=breakdown,
        )
