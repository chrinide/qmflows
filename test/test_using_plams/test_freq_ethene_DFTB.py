from qmflows import (dftb, run, templates)
from scm.plams import Molecule
import pytest


@pytest.mark.slow
def test_freq():
    """
    Do some constraint optimizations then launch a freq calc.
    """

    mol = Molecule("test/test_files/ethene.xyz", "xyz")
    geo_opt = dftb(templates.geometry, mol)
    freq_calc = dftb(templates.freq, geo_opt.molecule, job_name="freq")
    r = run(freq_calc)
    assert int(r.frequencies[0]) == 831
    assert len(r.frequencies) == 12
