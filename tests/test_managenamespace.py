"""pytest file built from tests/managenamespace.md"""
import sys

import pytest

from phmdoctest.fixture import managenamespace


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires >=py3.8")
def test_code_21_output_32(managenamespace):
    import sys

    a = 10
    print(sys.version_info)

    # Caution- no assertions.
    managenamespace(operation="update", additions=locals())
