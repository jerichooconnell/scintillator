#!/bin/bash

#SBATCH --ntasks=1

#SBATCH --time=8:0:0

#SBATCH --cpus-per-task=20

#SBATCH --mem-per-cpu=1024M

#SBATCH --account=def-bazalova

for i in 30 40 50 60 70 80 90 100 300 500 700 900 1000 2000 4000 6000
do
        sed -i '$ d'  Ge_CuGOS.txt
        sed -i '$ d'  Ge_CuGOS.txt
        sed -i '$ d'  Ge_CuGOS.txt
        echo d:So/PencilBeam/BeamEnergy = $i keV >>  Ge_CuGOS.txt
        echo s:Sc/Readout/OutputFile = \"runs/PhotodiodeSurface_keV_$i\" >>  Ge_CuGOS.txt
        echo s:Sc/EnergyDeposition/OutputFile = \"runs/EnergyDeposit_keV_$i\" >>  Ge_CuGOS.txt
        ~/topas/bin/topas Ge_CuGOS.txt

done