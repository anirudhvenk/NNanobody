import os
import subprocess

if __name__ == '__main__':
    os.chdir('/home/ec2-user/software/runs')
    for run in os.listdir('./'):
        os.chdir(os.path.join(run, 'run1'))
        subprocess.call("/usr/bin/python /home/ec2-user/software/haddock2.4-2021-05/Haddock/RunHaddock.py", shell=True)
        os.chdir('/home/ec2-user/software/runs')