import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from uuid import uuid4

from application.dto.catalog import CreateSparePartDTO
from application.use_cases.catalog.manage_spare_parts import CreateSparePartUseCase
from domain.entities.catalog import SparePartEntity
from domain.exceptions.base import ValidationException


@pytest.fixture
def repository():
    return MagicMock()


def test_create_spare_part_uppercases_name(repository):
    repository.exists_by_code.return_value = False
    expected = SparePartEntity(catalog_code="82210P1000", name="LAMEVIDRIO EXT PUERTA DEL LH", unit_price=Decimal("250.00"), concesionaria="SURMOTOR")
    repository.save.return_value = expected

    dto = CreateSparePartDTO(
        catalog_code="82210p1000",
        name="lamevidrio ext puerta del lh",
        unit_price=Decimal("250.00"),
        concesionaria="SURMOTOR",
    )
    result = CreateSparePartUseCase(repository).execute(dto)

    saved = repository.save.call_args[0][0]
    assert saved.catalog_code == "82210P1000"
    assert saved.name == "LAMEVIDRIO EXT PUERTA DEL LH"


def test_create_spare_part_duplicate_raises(repository):
    repository.exists_by_code.return_value = True

    dto = CreateSparePartDTO(
        catalog_code="82210P1000",
        name="LAMEVIDRIO",
        unit_price=Decimal("250.00"),
        concesionaria="SURMOTOR",
    )
    with pytest.raises(ValidationException):
        CreateSparePartUseCase(repository).execute(dto)

    repository.save.assert_not_called()
