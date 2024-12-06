from datetime import datetime

from eips.enum import EIP1Category, EIP1Status, EIP1Type
from eips.object import EIP, CommitHash

from ._const import TEST_EIP_HEADER


def test_parse_eip() -> None:
    eip = EIP.parse(4200, CommitHash("abc0def"), datetime.min, TEST_EIP_HEADER)
    assert eip.id == 4200
    assert eip.title == "EOF - Static relative jumps"
    assert (
        eip.discussions_to
        == "https://ethereum-magicians.org/t/eip-3920-static-relative-jumps/7108"
    )
    assert eip.status == EIP1Status.REVIEW
    assert eip.type == EIP1Type.STANDARDS
    assert eip.category == EIP1Category.CORE
    assert eip.created == datetime(year=2021, month=7, day=16)

    assert eip.requires is not None
    assert len(eip.requires) == 2
    assert 3540 in eip.requires
    assert 3670 in eip.requires
