from datetime import timedelta
from pathlib import Path

from eips.eips import REPO_DIR, EIPs, filter_doc_files
from eips.enum import EIP1Category, EIP1Status, EIP1Type


def test_eips() -> None:
    freshness = timedelta(seconds=4)
    repo = "http://nowhere.com/nothing.git"
    workdir = Path("/tmp/nowhere").expanduser().resolve()

    eips = EIPs(
        freshness=freshness,
        repo=repo,
        workdir=workdir,
    )

    assert eips.freshness == freshness
    assert eips.repo == repo
    assert eips.workdir == workdir


def test_eips_fetch(eips: EIPs, workdir: Path) -> None:
    orig_count = len(list(workdir.iterdir()))
    assert orig_count == 0
    assert eips.repo_fetch()
    assert len(list(workdir.iterdir())) > orig_count


def test_eips_parse_repo(eips: EIPs, workdir: Path) -> None:
    eips_path = workdir.joinpath(REPO_DIR).joinpath("EIPS")
    eips.repo_fetch()
    print("ttt eips_path.iterdir()", list(eips_path.iterdir()))
    eip_files = filter_doc_files(eips_path)
    print("ttttt eip_files:", eip_files)
    assert len(eip_files) > 0
    assert len(eips) == len(eip_files)
    eip_4626 = eips[4626]
    assert eip_4626 is not None
    assert eip_4626.id == 4626

    for eip in eips:
        assert eip.id > 0
        assert eip.is_valid


def test_eips_stats(eips: EIPs, workdir: Path) -> None:
    stats = eips.stats()
    assert stats.total >= 686
    assert len(stats.categories) <= len(EIP1Category)
    assert len(stats.statuses) <= len(EIP1Status)
    assert len(stats.types) <= len(EIP1Type)
    assert stats.errors == 0
