from dataclasses import dataclass, field


@dataclass
class StatusCount:
    status: str
    count: int


@dataclass
class TypeStatusCount:
    srg_type: str
    status: str
    count: int


@dataclass
class DashboardDTO:
    concesionaria: str
    total: int
    by_status: list[StatusCount] = field(default_factory=list)
    by_type: dict[str, int] = field(default_factory=dict)
    breakdown: list[TypeStatusCount] = field(default_factory=list)
