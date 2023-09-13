from pathlib import Path

import check_peps  # NoQA: inserted into sys.modules in conftest.py

PEP_9002 = Path(__file__).parent.parent / "peps" / "pep-9002.rst"


def test_with_fake_pep():
    content = PEP_9002.read_text(encoding="utf-8").splitlines()
    warnings = list(check_peps.check_peps(PEP_9002, content))
    assert warnings == [
        (1, "PEP must begin with the 'PEP:' header"),
        (8, "Must not have duplicate header: Sponsor "),
        (9, "Must not have invalid header: Horse-Guards"),
        (1, "Must have required header: PEP"),
        (1, "Must have required header: Type"),
        (
            1,
            "Headers must be in PEP 12 order. Correct order: Title, "
            "Author, Sponsor, BDFL-Delegate, Discussions-To, Status, Topic, "
            "Requires, Created, Python-Version, Post-History, "
            "Resolution",
        ),
        (4, "Author continuation lines must end with a comma"),
        (5, "Author line must not be over-indented"),
        (6, "Python-Version major part must be 1, 2, or 3: 4.0"),
        (
            7,
            "Sponsor entries must begin with a valid 'Name': "
            r"'Sponsor:\nHorse-Guards: Parade'",
        ),
        (10, "Created must be a 'DD-mmm-YYYY' date: '1-Jan-1989'"),
        (11, "Delegate entries must begin with a valid 'Name': 'Barry!'"),
        (12, "Status must be a valid PEP status"),
        (13, "Topic must not contain duplicates"),
        (13, "Topic must be properly capitalised (Title Case)"),
        (13, "Topic must be for a valid sub-index"),
        (13, "Topic must be sorted lexicographically"),
        (14, "PEP references must be separated by comma-spaces (', ')"),
        (15, "Discussions-To must be a valid thread URL or mailing list"),
        (16, "Post-History must be a 'DD-mmm-YYYY' date: '2-Feb-2000'"),
        (16, "Post-History must be a valid thread URL"),
        (17, "Post-History must be a 'DD-mmm-YYYY' date: '3-Mar-2001'"),
        (17, "Post-History must be a valid thread URL"),
        (18, "Resolution must be a valid thread URL"),
        (21, "Use the :pep:`NNN` role to refer to PEPs"),
    ]
