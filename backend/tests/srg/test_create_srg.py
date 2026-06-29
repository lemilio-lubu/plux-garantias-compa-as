import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from application.dto.srg import CreateWarrantySrgDTO, CreateCampaignSrgDTO
from application.use_cases.srg.create_warranty_srg import CreateWarrantySrgUseCase
from application.use_cases.srg.create_campaign_srg import CreateCampaignSrgUseCase
from domain.entities.srg import SrgEntity
from domain.exceptions.base import BusinessRuleViolationException
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType


@pytest.fixture
def repository():
    repo = MagicMock()
    # No existing SRG with the same OT by default → creation is allowed.
    repo.find_by_ot.return_value = None
    return repo


def _warranty_dto(asesor_id=None, ot="OT2026A001"):
    return CreateWarrantySrgDTO(
        concesionaria="SURMOTOR",
        asesor_id=asesor_id or uuid4(),
        ot=ot,
        vin="U5YPU81DAVL520154",
        placa="PXA-1234",
        vehicle_model="NQ5",
        vehicle_color="PLATEADO",
        vehicle_year=2026,
        km_apertura=30,
        sede="SURMOTOR",
        nro_garantia="3157",
        warranty_type_code="W",
        warranty_type_name="W-RECLAMO NORMAL DE REPARACIÓN MECÁNICA",
    )


def test_create_warranty_srg_uses_provided_ot(repository):
    repository.save.return_value = SrgEntity(
        ot="OT2026A001", srg_type=SrgType.WARRANTY, status=SrgStatus.PROCESO
    )

    CreateWarrantySrgUseCase(repository).execute(_warranty_dto(ot="OT2026A001"))

    saved = repository.save.call_args[0][0]
    assert saved.ot == "OT2026A001"
    assert saved.status == SrgStatus.PROCESO
    assert saved.srg_type == SrgType.WARRANTY


def test_create_warranty_srg_uppercases_ot(repository):
    repository.save.return_value = MagicMock()

    CreateWarrantySrgUseCase(repository).execute(_warranty_dto(ot="ot2026a001"))

    saved = repository.save.call_args[0][0]
    assert saved.ot == "OT2026A001"


def test_create_warranty_srg_duplicate_ot_raises(repository):
    repository.find_by_ot.return_value = SrgEntity(ot="OT2026A001", srg_type=SrgType.WARRANTY)

    with pytest.raises(BusinessRuleViolationException):
        CreateWarrantySrgUseCase(repository).execute(_warranty_dto(ot="OT2026A001"))

    repository.save.assert_not_called()


def test_create_warranty_srg_uppercases_fields(repository):
    repository.save.return_value = MagicMock()

    dto = _warranty_dto()
    dto.vin = "lower_vin"
    dto.vehicle_model = "nq5"

    CreateWarrantySrgUseCase(repository).execute(dto)

    saved = repository.save.call_args[0][0]
    assert saved.vin == "LOWER_VIN"
    assert saved.vehicle_model == "NQ5"


def test_create_campaign_srg_has_correct_type(repository):
    repository.save.return_value = MagicMock()
    dto = CreateCampaignSrgDTO(
        concesionaria="SURMOTOR",
        asesor_id=uuid4(),
        ot="OT2026C500",
        vin="U5YPU81DAVL520200",
        placa="PXA-5678",
        vehicle_model="NQ5",
        vehicle_year=2026,
        km_apertura=10,
        sede="SURMOTOR",
        campaign_code="SC250",
    )

    CreateCampaignSrgUseCase(repository).execute(dto)

    saved = repository.save.call_args[0][0]
    assert saved.ot == "OT2026C500"
    assert saved.srg_type == SrgType.CAMPAIGN
    assert saved.campaign_code == "SC250"
