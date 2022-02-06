import os
import numpy as np

if __name__ == '__main__':
    seeds = np.loadtxt('../data/seeds/filtered_seed.txt', dtype=str)
    with open('../generated/grafted_seeds.fasta', 'w') as f:
        for seed in seeds:
            if not (("C" in seed) or ("N" in seed) or ("X" in seed)):
                f.write('>{}\n'.format(seed))
                f.write('{}\n'.format(f'QVQLVESGGGLVQPGGSLRLSCAASGGSEYSYSTFSLGWFRQAPGQGLEAVAAIASMGGLTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAA{seed}WGQGTLVTVS'))