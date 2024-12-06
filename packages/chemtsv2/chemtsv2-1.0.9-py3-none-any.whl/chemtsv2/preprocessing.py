import re
import sys

import selfies as sf


def tokenize_smiles(smiles_list, conf):
    tokenized_smiles_list = []
    unique_token_set = set()
    for smi in smiles_list:
        tokenized_smiles = mol_tokenizer(smi, conf)
        tokenized_smiles.append('\n')
        unique_token_set |= set(tokenized_smiles)
        tokenized_smiles_list.append(tokenized_smiles)
    return sorted(list(unique_token_set)), tokenized_smiles_list


def read_smiles_dataset(filepath):
    with open(filepath, 'r') as f:
        smiles_list = [l.strip('\n') for l in f.readlines()]
    return smiles_list


def mol_tokenizer(mol_repl_str, conf):
    if conf['mol_representation_type'] == 'smiles':
        if conf['use_selfies']:
            token_str = selfies_tokenizer_from_smiles(mol_repl_str)
        else:
            token_str = smi_tokenizer(mol_repl_str)
    elif conf['mol_representation_type'] == 'helm':
        token_str = helm_tokenizer(mol_repl_str)
    else:
        sys.exit(f"[ERROR] `mol_representation_type` must be either `smiles` or `helm`.")
    
    return token_str


def smi_tokenizer(smi):
    """
    This function is based on https://github.com/pschwllr/MolecularTransformer#pre-processing
    Modified by Shoichi Ishida
    """
    pattern =  "(\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|p|\(|\)|\.|=|#|-|\+|\\\\|\/|:|~|@|\?|>|\*|\$|\%[0-9]{2}|[0-9])"
    regex = re.compile(pattern)
    tokens = [token for token in regex.findall(smi)]
    assert smi == ''.join(tokens)
    tokens.insert(0, '&')
    return tokens


def selfies_tokenizer_from_smiles(smi):
    if '[*]' in smi:
        smi = smi.replace("[*]", "[Lr]")  # Because SELFIES (v2.1.0) currently does not support a wildcard (*) representation.
    slfs = sf.encoder(smi)
    tokens = list(sf.split_selfies(slfs))
    assert slfs == ''.join(tokens)
    tokens.insert(0, '&')
    return tokens


def helm_tokenizer(helm):
    pattern = "(\[[^\]]+]|PEPTIDE[0-9]+|RNA[0-9]+|CHEM[0-9]+|BLOB[0-9]+|R[0-9]|A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|Y|\||\(|\)|\{|\}|-|\$|:|,|\.|[0-9]{2}|[0-9])"
    regex = re.compile(pattern)
    tokens = [t for t in regex.findall(helm)]
    assert helm == "".join(tokens)
    tokens.insert(0, '&')
    return tokens