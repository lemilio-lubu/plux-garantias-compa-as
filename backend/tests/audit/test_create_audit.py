import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from application.dto.audit import AuditAttachmentDTO, CreateAuditDTO
from application.use_cases.audit.create_audit import CreateAuditUseCase
from application.use_cases.audit.update_audit import UpdateAuditUseCase
from application.dto.audit import UpdateAuditDTO
from domain.entities.audit import AuditEntity, AuditAttachment
from domain.entities.srg import SrgEntity
from domain.exceptions.base import EntityNotFoundException, ValidationException


@pytest.fixture
def audit_repo():
    return MagicMock()


@pytest.fixture
def srg_repo():
    return MagicMock()


def _srg(concesionaria="SURMOTOR"):
    return SrgEntity(id=uuid4(), ot="202601739", concesionaria=concesionaria)


def _create_dto(srg_id, concesionaria="SURMOTOR"):
    return CreateAuditDTO(
        srg_id=srg_id,
        ot_factura="F202601739",
        observations="cumple con los requisitos de garantia kia",
        auditor_id=uuid4(),
        concesionaria=concesionaria,
        additional_emails=["jefe@surmotor.com"],
        attachments=[AuditAttachmentDTO(file_name="garantia.pdf", file_url="https://storage.example.com/garantia.pdf")],
    )


def test_create_audit_success(audit_repo, srg_repo):
    srg = _srg()
    srg_repo.find_by_id.return_value = srg
    expected = AuditEntity(id=uuid4(), srg_id=srg.id, ot_factura="F202601739", observations="CUMPLE CON LOS REQUISITOS DE GARANTIA KIA", concesionaria="SURMOTOR")
    audit_repo.save.return_value = expected

    result = CreateAuditUseCase(audit_repo, srg_repo).execute(_create_dto(srg.id))

    saved = audit_repo.save.call_args[0][0]
    assert saved.observations == "CUMPLE CON LOS REQUISITOS DE GARANTIA KIA"
    assert saved.ot_factura == "F202601739"
    assert saved.attachments[0].file_name == "GARANTIA.PDF"
    assert saved.additional_emails == ["jefe@surmotor.com"]


def test_create_audit_srg_not_found(audit_repo, srg_repo):
    srg_repo.find_by_id.return_value = None
    with pytest.raises(EntityNotFoundException):
        CreateAuditUseCase(audit_repo, srg_repo).execute(_create_dto(uuid4()))


def test_create_audit_wrong_concesionaria(audit_repo, srg_repo):
    srg = _srg(concesionaria="SHYRIS")
    srg_repo.find_by_id.return_value = srg

    dto = _create_dto(srg.id, concesionaria="SURMOTOR")
    with pytest.raises(ValidationException) as exc:
        CreateAuditUseCase(audit_repo, srg_repo).execute(dto)
    assert "does not belong" in exc.value.message


def test_update_audit_observations_uppercased(audit_repo):
    audit = AuditEntity(id=uuid4(), srg_id=uuid4(), observations="OLD", concesionaria="SURMOTOR")
    audit_repo.find_by_id.return_value = audit
    audit_repo.save.return_value = audit

    dto = UpdateAuditDTO(id=audit.id, observations="nueva observacion con minusculas")
    UpdateAuditUseCase(audit_repo).execute(dto)

    saved = audit_repo.save.call_args[0][0]
    assert saved.observations == "NUEVA OBSERVACION CON MINUSCULAS"


def test_update_audit_not_found(audit_repo):
    audit_repo.find_by_id.return_value = None
    with pytest.raises(EntityNotFoundException):
        UpdateAuditUseCase(audit_repo).execute(UpdateAuditDTO(id=uuid4(), observations="X"))
