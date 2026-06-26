from uuid import UUID

from application.dto.srg_body import UpsertCampaignBodyDTO
from application.ports.repositories.srg_repository import ISrgRepository
from application.ports.repositories.srg_body_repository import ICampaignBodyRepository
from domain.entities.campaign_body import CampaignBodyEntity
from domain.exceptions.base import BusinessRuleViolationException, EntityNotFoundException
from domain.value_objects.srg_type import SrgType


class UpsertCampaignBodyUseCase:
    def __init__(
        self, srg_repo: ISrgRepository, body_repo: ICampaignBodyRepository
    ) -> None:
        self._srg_repo = srg_repo
        self._body_repo = body_repo

    def execute(self, dto: UpsertCampaignBodyDTO) -> CampaignBodyEntity:
        srg = self._srg_repo.find_by_id(dto.srg_id)
        if srg is None:
            raise EntityNotFoundException("SRG", str(dto.srg_id))
        if srg.srg_type != SrgType.CAMPAIGN:
            raise BusinessRuleViolationException("Campaign body only applies to campaign SRGs")
        if not srg.campaign_body_enabled:
            raise BusinessRuleViolationException(
                f"SRG must be APROBADO to register campaign body. Current status: {srg.status}"
            )

        existing = self._body_repo.find_by_srg(dto.srg_id)
        if existing:
            existing.update_name = dto.update_name.upper()
            existing.image_link = dto.image_link
            existing.modified_by = dto.modified_by
            return self._body_repo.save(existing)

        body = CampaignBodyEntity(
            srg_id=dto.srg_id,
            update_name=dto.update_name.upper(),
            image_link=dto.image_link,
            modified_by=dto.modified_by,
        )
        return self._body_repo.save(body)


class GetCampaignBodyUseCase:
    def __init__(self, body_repo: ICampaignBodyRepository) -> None:
        self._body_repo = body_repo

    def execute(self, srg_id: UUID) -> CampaignBodyEntity | None:
        return self._body_repo.find_by_srg(srg_id)
