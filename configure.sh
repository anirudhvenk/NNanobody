cd ../cns_solve_1.3/
make install

unset -v latest
for file in "/home/ec2-user/software/cns_solve_1.3/intel-x86_64bit-linux/source"/*; do
  [[ $file -nt $latest ]] && latest=$file
done

sed -i "s|^set CNSTMP=.*|set CNSTMP=${latest}|" /home/ec2-user/software/haddock2.4-2021-05/config.local 

cd /home/ec2-user/software/haddock2.4-2021-05
./install.csh config.local

sed -i "s/^export.*/export HADDOCK HADDOCKTOOLS PYTHONPATH/" /home/ec2-user/software/haddock2.4-2021-05/haddock_configure.sh
sed -i "14,17d" /home/ec2-user/software/haddock2.4-2021-05/haddock_configure.sh

cd ../haddock2.4-2021-05
source ./haddock_configure.sh
