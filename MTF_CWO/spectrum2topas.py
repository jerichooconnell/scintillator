n = 1
x = 0
energies = []
values = []
with open('Al_spectrum.txt') as f:
    for line in f:
        energies.append(float(line.split()[0]))
        values.append(float(line.split()[1]))
        n+=1
        
print(energies,values,n)