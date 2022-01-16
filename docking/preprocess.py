"""
Preprocess docking information for a single run.
Usage:
    preprocess.py --prot-1=<protein1> --prot-2=<protein2> --out-dir=<out_dir> --run-rumber=<run_number> --active-1=<active1> --active-2=<active2>
"""
from docopt import docopt
from active_passive_to_ambig import active_passive_to_ambig
import os


def generate_run_param(out_dir, run_number):
    with open(os.path.join(out_dir, 'run.param'), 'w') as f:
        f.write('AMBIG_TBL=ambig.tbl\n')
        f.write('UNAMBIG_TBL=unambig.tbl\n')
        f.write('HADDOCK_DIR=/home/ec2-user/software/haddock2.4-2021-05\n')
        f.write('N_COMP=128\n')
        f.write('PDB_FILE1=protein1.pdb\n')
        f.write('PROT_SEGID_1=A\n')
        f.write('PDB_FILE2=protein2.pdb\n')
        f.write('PROT_SEGID_2=B\n')
        f.write('PROJECT_DIR=/home/ec2-user/software/run\n')
        f.write(f'RUN_NUMBER={run_number}\n')

def generate_unambig(out_dir):
    with open(os.path.join(out_dir, 'unambig.tbl'), 'w') as f:
        f.write('! Molecule #2 gap(s) restraint(s)\n')
        f.write('assign (resid 34 and name CA and segid B) (resid 247 and name CA and segid B) 17.546 0.00 0.00\n')
        f.write('assign (resid 34 and name CA and segid B) (resid 357 and name CA and segid B) 40.908 0.00 0.00\n')
        f.write('assign (resid 235 and name CA and segid B) (resid 36 and name CA and segid B) 21.306 0.00 0.00\n')
        f.write('assign (resid 235 and name CA and segid B) (resid 357 and name CA and segid B) 32.100 0.00 0.00\n')
        f.write('assign (resid 356 and name CA and segid B) (resid 36 and name CA and segid B) 33.992 0.00 0.00\n')
        f.write('assign (resid 356 and name CA and segid B) (resid 247 and name CA and segid B) 40.087 0.00 0.00\n')
        
def active_passive_to_ambig(active1, passive1, active2, passive2, out_dir, segid1='A', segid2='B'):
    all1 = active1 + passive1
    all2 = active2 + passive2

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
    
    prot1 = args['--prot-1']
    prot2 = args['--prot-2']
    out_dir = args['--out-dir']
    run_number = args['--run-rumber']
    active1 = args['--active_1']
    active2 = args['--active_2']
    
    generate_run_param(out_dir, run_number)
    generate_unambig(out_dir)
    