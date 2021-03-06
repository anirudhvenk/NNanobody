"""
Preprocess docking information for a single run.

Usage:
    preprocess.py --folded_sequences=<folded_dir> --antigen=<antigen>
"""
import subprocess
import shutil
from docopt import docopt
from Bio import SeqIO
from Bio.PDB import PDBList, PDBIO, PDBParser
import os
import numpy as np
import time

def clean_pdb(prot):
    """
    clean_pdb parses through the PDB file in order to remove atoms that would cause issues in the docking process.

    :param prot: Protein PDB file to parse and clean
    """
    
    my_file = open(os.path.join(out_dir, prot), 'r')
    content = my_file.readlines()
    content[-2] = 'TER\n'
    with open(os.path.join(out_dir, prot), 'w') as f:
        f.write(''.join(content)) # Write the PDB file out


def load_pdb(prot1, prot2, out_dir):
    """
    load_pdb loads the PDB files, identifies their active residues, and writes them into the temp_params directory.
    
    :param prot1: First protein to be docked (nanobody PDB file)
    :param prot2: Second protein to be docked (Ranibizumab, PDB file)
    :param out_dir: Directory to store output (both proteins)
    :return: Active residues of both proteins
    """
    
    # Get FASTA sequence to identify active residues
    with open(prot1, 'r') as pdb:
        for record in SeqIO.parse(pdb, 'pdb-atom'):
            fasta = record.seq
        
    parser = PDBParser()
    io = PDBIO()
    
    protein1_structure = parser.get_structure('protein1', prot1)
    for model in protein1_structure:
        for chain in model:
            chain.id = 'A'
            
    io.set_structure(protein1_structure)
    io.save(os.path.join(out_dir, 'protein1.pdb'))
    clean_pdb('protein1.pdb')
    
    protein2_structure = parser.get_structure('protein1', prot2)
    for model in protein2_structure:
        for chain in model:
            chain.id = 'B'
            
    io.set_structure(protein2_structure)
    io.save(os.path.join(out_dir, 'protein2.pdb'))
    clean_pdb('protein2.pdb')
    
    cdr1 = np.arange(26, 39)
    cdr2 = np.arange(53, 70)
    cdr3 = np.arange(102, len(fasta)-9)
    active_residues_1 = np.concatenate((cdr1, cdr2, cdr3))
    active_residues_2 = [24,25,26,27,28,29,30,31,32,33,34,50,51,52,53,54,55,56,89,90,91,92,93,94,95,96,97,239,240,241,242,243,244,245,246,247,248,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,312,313,314,315,316,317,318,319,320,321,322,323,324,325]
    return(active_residues_1, np.asarray(active_residues_2))


def generate_run_param(out_dir, run_dir):
    """
    generate_run_param generates the run parameters for the HADDOCK run.
    
    :param out_dir: Directory containing all files for docking
    :param run_dir: Directory to perform the docking run
    """
    
    # Create run.param file
    with open(os.path.join(out_dir, 'run.param'), 'w') as f:
        f.write('AMBIG_TBL=ambig.tbl\n')
        f.write('UNAMBIG_TBL=unambig.tbl\n')
        f.write('HADDOCK_DIR=/home/ec2-user/software/haddock2.4-2021-05\n')
        f.write('N_COMP=2\n')
        f.write(f'PDB_FILE1=protein1.pdb\n')
        f.write('PROT_SEGID_1=A\n')
        f.write(f'PDB_FILE2=protein2.pdb\n')
        f.write('PROT_SEGID_2=B\n')
        f.write(f'PROJECT_DIR=/home/ec2-user/software/runs/{run_dir}\n') #run_dir = cdr3 sequence
        f.write('RUN_NUMBER=1\n')

def generate_unambig(out_dir):
    """
    generate_unambig determines the unamibiguous residues of Ranibizumab and saves them to unambig.tbl
    
    :param out_dir: Directory containing all files for docking
    """
    
    with open(os.path.join(out_dir, 'unambig.tbl'), 'w') as f:
        f.write('! Molecule #2 gap(s) restraint(s)\n')
        f.write('assign (resid 34 and name CA and segid B) (resid 247 and name CA and segid B) 17.546 0.00 0.00\n')
        f.write('assign (resid 34 and name CA and segid B) (resid 357 and name CA and segid B) 40.908 0.00 0.00\n')
        f.write('assign (resid 235 and name CA and segid B) (resid 36 and name CA and segid B) 21.306 0.00 0.00\n')
        f.write('assign (resid 235 and name CA and segid B) (resid 357 and name CA and segid B) 32.100 0.00 0.00\n')
        f.write('assign (resid 356 and name CA and segid B) (resid 36 and name CA and segid B) 33.992 0.00 0.00\n')
        f.write('assign (resid 356 and name CA and segid B) (resid 247 and name CA and segid B) 40.087 0.00 0.00\n')
        
def active_passive_to_ambig(active1, active2, out_dir, segid1='A', segid2='B'):
    """
    active_passive_to_ambig writes the active and passive residues of each protein into a .tbl file.
    
    :param active1: Active residues of first protein (nanobody)
    :param active2: Active residues of second protein (Ranibizumab)
    :param out_dir: Directory containing all files for docking
    """
    
    all1 = active1
    all2 = active2

    with open(os.path.join(out_dir, 'ambig.tbl'), 'w') as f:
        for resi1 in active1:
            f.write('assign (resi {:d} and segid {:s})\n'.format(resi1, segid1))
            f.write('(\n')
            c = 0
            for resi2 in all2:
                f.write('       (resi {:d} and segid {:s})\n'.format(resi2, segid2))
                c += 1
                if c != len(all2):
                    f.write('        or\n')

            f.write(') 2.0 2.0 0.0\n\n')
                
        for resi2 in active2:
            f.write('assign (resi {:d} and segid {:s})\n'.format(resi2, segid2))
            f.write('(\n\n')
            c = 0
            for resi1 in all1:
                f.write('       (resi {:d} and segid {:s})\n'.format(resi1, segid1))
                c += 1
                if c != len(all1):
                    f.write('        or\n\n')

            f.write(') 2.0 2.0 0.0\n\n')
        

if __name__ == '__main__':
    args = docopt(__doc__)
    folded_dir = args['--folded_sequences']
    antigen = args['--antigen']
    process_dir = os.getcwd()
    
    for protein in os.listdir(folded_dir):
        os.chdir(process_dir)
        protein_file = os.path.join(folded_dir, protein)
        out_dir = os.path.join(process_dir, 'temp_params')
        
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        
        active1, active2 = load_pdb(protein_file, antigen, out_dir)
        os.mkdir('/home/ec2-user/software/runs/' + protein.split('_')[0])
        generate_run_param(out_dir, protein.split('_')[0])
        generate_unambig(out_dir)
        active_passive_to_ambig(active1, active2, out_dir)
        os.chdir(out_dir)
        time.sleep(5)
        subprocess.call("/usr/bin/python /home/ec2-user/software/haddock2.4-2021-05/Haddock/RunHaddock.py", shell=True)
