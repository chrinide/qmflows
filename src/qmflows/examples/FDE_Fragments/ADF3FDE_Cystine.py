__all__ = ['example_ADF3FDE_Cystine']

# Default imports
from qmflows import (templates, run, Settings)
from qmflows.components import mfcc, adf3fde
from noodles import gather

from qmflows.packages.SCM import adf
import scm.plams.interfaces.molecule.rdkit as molkit

import io
import sys
sys.setrecursionlimit(200)


def example_ADF3FDE_Cystine():
    """
    For the purpose of the example, define the pdb file here.

    It turned out important to rename the terminal carboxyl oxygens
    to which hydrogens were connected to "OXT" in order for RDKIT
    to correctly interpret the connectivity of the cys_cys.pdb
    """
    cys_cys_pdb = io.StringIO(
'''HEADER
ATOM      1  N   CYS A   1      10.708  18.274  27.487  1.00  0.00           N
ATOM      2  CA  CYS A   1      11.790  18.118  26.530  1.00  0.00           C
ATOM      3  C   CYS A   1      11.911  16.696  25.950  1.00  0.00           C
ATOM      4  O   CYS A   1      11.274  15.733  26.320  1.00  0.00           O
ATOM      5  CB  CYS A   1      13.111  18.628  27.130  1.00  0.00           C
ATOM      6  SG  CYS A   1      13.606  17.812  28.713  1.00  0.00           S
ATOM      7  H   CYS A   1      10.888  17.663  28.290  1.00  0.00           H
ATOM      8  H   CYS A   1      11.588  18.770  25.664  1.00  0.00           H
ATOM      9  H   CYS A   1      12.965  19.678  27.420  1.00  0.00           H
ATOM     10  H   CYS A   1      13.937  18.567  26.413  1.00  0.00           H
ATOM     11  H   CYS A   1       9.832  17.945  27.080  1.00  0.00           H
ATOM     12  OXT CYS A   1      12.794  16.651  24.907  1.00  0.00           O
ATOM     13  H   CYS A   1      12.787  15.724  24.592  1.00  0.00           H
ATOM     14  N   CYS A   2      16.380  17.608  25.858  1.00  0.00           N
ATOM     15  CA  CYS A   2      16.727  17.837  27.250  1.00  0.00           C
ATOM     16  C   CYS A   2      18.225  18.158  27.351  1.00  0.00           C
ATOM     17  OXT CYS A   2      18.608  18.849  28.464  1.00  0.00           O
ATOM     18  CB  CYS A   2      16.413  16.665  28.207  1.00  0.00           C
ATOM     19  SG  CYS A   2      14.654  16.118  28.163  1.00  0.00           S
ATOM     20  O   CYS A   2      19.042  17.809  26.533  1.00  0.00           O
ATOM     21  H   CYS A   2      15.649  16.899  25.780  1.00  0.00           H
ATOM     22  H   CYS A   2      16.171  18.714  27.635  1.00  0.00           H
ATOM     23  H   CYS A   2      17.819  19.103  28.978  1.00  0.00           H
ATOM     24  H   CYS A   2      16.673  16.910  29.246  1.00  0.00           H
ATOM     25  H   CYS A   2      16.973  15.766  27.908  1.00  0.00           H
ATOM     26  H   CYS A   2      17.213  17.290  25.357  1.00  0.00           H
''')

    supermol = molkit.readpdb(cys_cys_pdb)

    # Calculate  normally
    supermol_job = adf(templates.singlepoint, supermol,
                       job_name='supermol_singlepoint')

    settings = Settings()
    settings.functional = 'bp86'
    settings.charge = '0'
    settings.basis = 'SZ'
    settings.specific.adf.basis.core = 'large'
    settings.specific.adf.stofit = ''
    settings.specific.adf.save = 'tape21'
    settings.specific.adf.eprint.sfo = 'NOEIG NOOVL NOORBPOP'
    settings.specific.adf.eprint.scf = 'NOPOP'
    settings.specific.adf.symmetry = 'tol=1e-2'
    settings.specific.adf.geometry.sp = ""

    # Calculate with mfcc approach
    frags, caps = molkit.partition_protein(supermol)
    mfcc_job = mfcc(adf, frags, caps, settings)

    # Calculate with adf3fde
    fde_settings = Settings({'RHO1FITTED': '', 'CapDensConv': 1e-3})
    fragment_settings = Settings({'fdedenstype': 'SCFfitted'})

    adf3fde_job = adf3fde(
        mfcc_job.frags, mfcc_job.caps, settings, fde_settings, fragment_settings, cycles=2)
    supermol_dipole, mfcc_dipole, adf3fde_dipole = run(
        gather(supermol_job.dipole, mfcc_job.dipole, adf3fde_job.dipole))

    print("Supermolecule dipole: ", supermol_dipole)
    print("mfcc dipole: ", mfcc_dipole)

    return supermol_dipole, mfcc_dipole, adf3fde_dipole
