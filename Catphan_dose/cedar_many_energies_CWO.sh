#!/bin/bash

#SBATCH --ntasks=1

#SBATCH --time=8:0:0

#SBATCH --cpus-per-task=20

#SBATCH --mem-per-cpu=1024M

#SBATCH --account=def-bazalova

for i in Al_spectrum_25topas.txt C_spectrum_6topas.txt Al_spectrum_6topas.txt W_spectrum_25topas.txt W_spectrum_6topas.txt C_spectrum_25topas.txt
do
        sed -i '$ d'  Catphan_515.txt
        sed -i '$ d'  Catphan_515.txt
        sed -i '$ d'  Catphan_515.txt
        tail -2 $i  >>  Catphan_515.txt
        echo "" >> Catphan_515.txt
        echo s:Sc/Dose_Al_6/OutputFile = \"Dose_$i\" >>  Catphan_515.txt
        ~/topas/bin/topas Catphan_515.txt

done