from rdkit import Chem
from rdkit import DataStructs
from multiprocessing import Pool



if __name__ == '__main__':
    pool = Pool(16)
    lines1 = [line.strip("\r\n ") for line in open('chembl.txt')]
    lines2 = [line.strip("\r\n ") for line in open('refined.txt')]
    mols1 = [Chem.MolFromSmiles(line) for line in lines1]
    mols2 = [Chem.MolFromSmiles(line) for line in lines2]
    mols1_fp = [Chem.RDKFingerprint(mol1, maxPath=10) for mol1 in mols1]
    mols2_fp = [Chem.RDKFingerprint(mol2, maxPath=15) for mol2 in mols2]
    result = []
    print('begin!')
    for i in range(len(mols1)):
        for j in range(len(mols2)):
            sm = DataStructs.FingerprintSimilarity(mols1_fp[i], mols2_fp[j])
            if sm > 0.75:
                result.append([sm, i, j, lines1[i], lines2[j]])

    for item in result:
        print(item)
