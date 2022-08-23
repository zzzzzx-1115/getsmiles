import argparse
import os
import glob
from rdkit import Chem

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)


if __name__ == '__main__':
    args = parser.parse_args()
    dirs = glob.glob(os.path.join(args.path, '????'))
    for dir in dirs:
        pt = os.path.join(args.path, dir)
        temp = glob.glob(os.path.join(pt, '*.sdf'))
        assert len(temp) == 1
        file = temp[0]
        mol = Chem.MolFromMolFile(file, removeHs=True)
        if mol is None:
            continue
        s_mol = Chem.MolToSmiles(mol)
        print(s_mol)
