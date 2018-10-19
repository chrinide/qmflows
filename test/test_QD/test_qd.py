import os
import pytest
import yaml

from os.path import join
from scm.plams import Molecule
import qmflows.qd as QD
from qmflows.components.qd_import_export import (
    read_mol, read_mol_xyz, read_mol_pdb, read_mol_mol,
    read_mol_smiles, read_mol_folder, read_mol_txt,
    read_mol_plams, read_mol_rdkit)

folder_path = os.path.abspath('test/test_QD/test_QD_files')


def test_read_mol_1():
    """
    Test if the AcOH.xyz, .pdb and .mol files return molecules with molecular formulas,
    distances and angles.
    i.e. are all internal coordinates identical?
    """
    print("Folder: ", folder_path)
    xyz = read_mol_xyz('AcOH.xyz', {'mol_path': join(folder_path, 'AcOH.xyz')})
    pdb = read_mol_pdb('AcOH.xyz', {'mol_path': join(folder_path, 'AcOH.pdb')})
    mol = read_mol_mol('AcOH.xyz', {'mol_path': join(folder_path, 'AcOH.mol')})
    mol_list = [xyz, pdb, mol]

    atom_list = [[[at1, at2] for at1 in mol for at2 in mol if at1 != mol[1] and at2 != mol[1]] for
                 mol in mol_list]
    formula_list = [mol.get_formula() for mol in mol_list]
    distance_list = [[mol[1].distance_to(atom) for atom in mol if not mol[1]] for mol in mol_list]
    angle_list = []
    for i, mol in enumerate(mol_list):
        for atom in atom_list[i]:
            if atom[0] != atom[1]:
                angle_list.append([mol[1].angle(atom[0], atom[1], result_unit='degree')])

    assert isinstance(mol_list, list)
    assert len(mol_list) == 3
    for mol in mol_list:
        assert isinstance(mol, Molecule)

    assert [formula_list[0] is formula for formula in formula_list[1:]]
    assert [distance_list[0] is distance for distance in distance_list[1:]]
    assert [angle_list[0] is angle for angle in angle_list[1:]]


def test_read_mol_2():
    """
    Checks parsing if a file with a given extensions returns:
        1. a list
        2. if the list has 1 entry
        3. if that entry is a plams molecule
    """
    mol_name = 'AcOH'
    folder_path = 'test/test_QD/test_qd_files'

    extension_dict = {'xyz': read_mol_xyz, 'pdb': read_mol_pdb,
                      'mol': read_mol_mol, 'smiles': read_mol_smiles,
                      'folder': read_mol_folder, 'txt': read_mol_txt,
                      'plams_mol': read_mol_plams, 'rdmol': read_mol_rdkit}
    key_list = list(extension_dict.keys())
    for item in key_list:
        mol_path = os.path.join(folder_path, mol_name + '.' + item)
        mol_dict = {'mol_name': mol_name, 'mol_path': mol_path, 'folder_path': mol_path,
                    'row': 0, 'column': 0, 'sheet_name': 'Sheet1', 'is_core': False}
        if os.path.exists(mol_path):
            xyz = [extension_dict[key](mol_name + '.' + item, mol_dict) for key in key_list]
            assert isinstance(xyz, list)
            mol = [item for item in xyz if isinstance(item, (Molecule, list))]
            assert len(mol) == 1
            if isinstance(mol[0], list):
                mol = mol[0][0]
            else:
                mol = mol[0]
            assert len(mol) == 8
            assert isinstance(mol, Molecule)


def test_read_mol_3():
    """
    Check if 5 valid SMILES strings return 5 plams molecules
    """
    input_mol = ['OC', 'OCC', 'OCCC', 'OCCCC', 'OCCCCC']
    mol_list = read_mol(input_mol, folder_path)

    assert isinstance(mol_list, list)
    assert len(mol_list) is len(input_mol)
    for mol in mol_list:
        assert isinstance(mol, Molecule)


def test_read_mol_4():
    """
    Check if 2 invalid SMILES strings return an IndexError
    """
    input_mol = ['dwefwefqe', 'fqwdwq']
    with pytest.raises(IndexError):
        assert read_mol(input_mol, folder_path=folder_path)


def test_input():
    path = os.path.abspath('test/test_QD')

    input_cores = yaml.load("""
    -   - Cd68Se55.xyz
        - guess_bonds: False
    """)

    input_ligands = yaml.load("""
    - AcOH.mol
    - AcOH.pdb
    - AcOH.txt
    - AcOH.xyz
    - O=C(O)C
    """)

    argument_dict = yaml.load("""
    dir_name_list: [test_QD_files, test_QD_files, test_QD_files]
    dummy: Cl
    core_indices: []
    ligand_indices: []
    database_name: ligand_database.xlsx
    use_database: True
    core_opt: False
    ligand_opt: True
    qd_opt: False
    maxiter: 10000
    split: True
    """)

    print(path)
    qd_list = QD.prep(input_ligands, input_cores, path, argument_dict)
    QD.prep(input_ligands, input_cores, path, argument_dict)
    formula_set = set([qd.get_formula() for qd in qd_list])

    assert isinstance(qd_list, list)
    assert len(qd_list) is 5
    assert len(formula_set) is 1
    for qd in qd_list:
        assert isinstance(qd, Molecule)

    argument_dict['use_database'] = False
    QD.prep(input_ligands, input_cores, path, argument_dict)
    argument_dict['ligand_opt'] = False
    QD.prep(input_ligands, input_cores, path, argument_dict)
    argument_dict['split'] = False
    QD.prep(input_ligands, input_cores, path, argument_dict)
    argument_dict['dummy'] = 'Cd'
    QD.prep(input_ligands, input_cores, path, argument_dict)