#!/usr/bin/env python

"""
Python script to convert a list of active and passive residues into 
ambiguous interaction restraints for HADDOCK
"""


def active_passive_to_ambig(active1, passive1, active2, passive2, outdir, segid1='A', segid2='B'):
    all1 = active1 + passive1
    all2 = active2 + passive2

    with open(os.path.join(outdir, 'ambig.tbl'), 'w') as f:
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
