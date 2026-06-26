from enum import StrEnum


class SrgStatus(StrEnum):
    PROCESO = "PROCESO"
    PENDIENTE = "PENDIENTE"
    PREAPROBADO = "PREAPROBADO"
    APROBADO = "APROBADO"
    RETORNADO = "RETORNADO"
    NEGADO = "NEGADO"

    def can_transition_to(self, next_status: "SrgStatus") -> bool:
        allowed: dict[SrgStatus, set[SrgStatus]] = {
            SrgStatus.PROCESO: {SrgStatus.PENDIENTE},
            SrgStatus.PENDIENTE: {SrgStatus.PREAPROBADO, SrgStatus.RETORNADO, SrgStatus.NEGADO},
            SrgStatus.PREAPROBADO: {SrgStatus.APROBADO, SrgStatus.RETORNADO, SrgStatus.NEGADO},
            SrgStatus.APROBADO: set(),
            SrgStatus.RETORNADO: {SrgStatus.PROCESO},
            SrgStatus.NEGADO: set(),
        }
        return next_status in allowed.get(self, set())
