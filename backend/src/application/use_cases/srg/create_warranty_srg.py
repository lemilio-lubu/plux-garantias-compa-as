from application.dto.srg import CreateWarrantySrgDTO
from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg import SrgEntity
from domain.exceptions.base import BusinessRuleViolationException
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType


class CreateWarrantySrgUseCase:
    def __init__(self, repository: ISrgRepository) -> None:
        self._repository = repository

    def execute(self, dto: CreateWarrantySrgDTO) -> SrgEntity:
        ot = dto.ot.upper()
        if self._repository.find_by_ot(ot) is not None:
            raise BusinessRuleViolationException(f"Ya existe un SRG con la OT {ot}.")

        entity = SrgEntity(
            ot=ot,
            srg_type=SrgType.WARRANTY,
            status=SrgStatus.PROCESO,
            concesionaria=dto.concesionaria,
            asesor_id=dto.asesor_id,
            vin=dto.vin.upper(),
            vehicle_model=dto.vehicle_model.upper(),
            vehicle_color=dto.vehicle_color.upper(),
            vehicle_year=dto.vehicle_year,
            km_apertura=dto.km_apertura,
            sede=dto.sede,
            nro_garantia=dto.nro_garantia.upper(),
            warranty_type_code=dto.warranty_type_code.upper(),
            warranty_type_name=dto.warranty_type_name.upper(),
        )
        return self._repository.save(entity)
