from application.dto.srg import CreateCampaignSrgDTO
from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg import SrgEntity
from domain.exceptions.base import BusinessRuleViolationException
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType


class CreateCampaignSrgUseCase:
    def __init__(self, repository: ISrgRepository) -> None:
        self._repository = repository

    def execute(self, dto: CreateCampaignSrgDTO) -> SrgEntity:
        ot = dto.ot.upper()
        if self._repository.find_by_ot(ot) is not None:
            raise BusinessRuleViolationException(f"Ya existe un SRG con la OT {ot}.")

        entity = SrgEntity(
            ot=ot,
            srg_type=SrgType.CAMPAIGN,
            status=SrgStatus.PROCESO,
            concesionaria=dto.concesionaria,
            asesor_id=dto.asesor_id,
            vin=dto.vin.upper(),
            placa=dto.placa.upper(),
            vehicle_model=dto.vehicle_model.upper(),
            vehicle_year=dto.vehicle_year,
            km_apertura=dto.km_apertura,
            sede=dto.sede,
            campaign_code=dto.campaign_code.upper(),
        )
        return self._repository.save(entity)
