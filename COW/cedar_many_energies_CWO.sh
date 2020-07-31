#!/bin/bash

#SBATCH --ntasks=1

#SBATCH --time=8:0:0

#SBATCH --cpus-per-task=20

#SBATCH --mem-per-cpu=1024M

#SBATCH --account=def-bazalova

for i in 30 40 50 60 70 80 90 100 300 500 700 900 1000 2000 4000 6000
do
        sed -i '$ d'  Ge_COW.txt
        sed -i '$ d'  Ge_COW.txt
        echo d:So/PencilBeam/BeamEnergy = $i keV >>  Ge_COW.txt
        echo s:Sc/Readout/OutputFile = \"runs/PhotodiodeSurface_keV_$i\" >>  Ge_COW.txt
        ~/topas/bin/topas Ge_COW.txt
        cat runs/*.csv | awk 'NR % 6 == 0' >> runs/deposition.txt

done