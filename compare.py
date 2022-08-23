from rdkit import Chem
from rdkit import DataStructs
from multiprocessing import Pool

from functools import partial

def haha(x):
    return Chem.RDKFingerprint(x, maxPath=10)
def hehe(x):
    return Chem.RDKFingerprint(x, maxPath=15)

def nt(x, fp1, fp2, lines1, lines2):
    sm = DataStructs.FingerprintSimilarity(fp1[x[0]], fp2[x[1]])
    if sm > 0.75:
        return [sm, x[0], x[1], lines1[x[0]], lines2[x[1]]]
    else: return

if __name__ == '__main__':
    pool = Pool(16)
    lines1 = [line.strip("\r\n ") for line in open('chembl.txt')]
    lines2 = [line.strip("\r\n ") for line in open('refined.txt')]
    mols1 = [Chem.MolFromSmiles(line) for line in lines1]
    mols2 = [Chem.MolFromSmiles(line) for line in lines2]
    #print(haha(mols1[0]))
    mols1_fp = pool.map(haha, mols1)
    mols2_fp = pool.map(hehe, mols2)
    index_pair = []





    #print('begin!')
    for i in range(len(mols1)):
        for j in range(len(mols2)):
            index_pair.append((i, j))
            #sm = DataStructs.FingerprintSimilarity(mols1_fp[i], mols2_fp[j])
            # if sm > 0.75:
            #     result.append([sm, i, j, lines1[i], lines2[j]])

    result = pool.map(partial(nt, fp1=mols1_fp, fp2=mols2_fp, lines1=lines1, lines2=lines2), index_pair)
    for item in result:
        if item is not None:
            print(item)
