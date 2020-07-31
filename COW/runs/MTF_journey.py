#!/usr/bin/env python
# coding: utf-8


import os
import glob

import numpy as np
import matplotlib.pyplot as plt
from pylab import cm
from matplotlib.colors import LogNorm

# dump_files = 'analysis/2020-06-06-h10m44/*.npy'
# spectrum_file = '../../MTF_CWO/Al_spectrum.txt'
# # spectrum_file = '/home/xcite/EGSnrc/egs_home/BEAM_EX16MVp/W_FF_spectrum'
# deposition_efficiency_file = 'analysis/2020-06-04-h08m58/EnergyDeposition.npy'

def plot_MTF(dump_files = 'analysis/2020-06-06-h10m44/*.npy',
            spectrum_file = '../../MTF_CWO/Al_spectrum.txt',
            deposition_efficiency_file = 'analysis/2020-06-04-h08m58/EnergyDeposition.npy',
            Verbose = False):

    files = sorted(glob.glob(dump_files))

    for ii, file in enumerate(files):
        
        if ii == 0:
            
            # Make the first entry zeros
            first_kernel = np.load(file)
            kernels = np.zeros([len(files)+1,first_kernel.shape[0],first_kernel.shape[1]]) 
            
        kernels[ii+1] = np.load(file)


    # In[112]:


    energies = []
    fluence = []
    with open(spectrum_file) as f:
        for line in f:
            energies.append(float(line.split()[0]))
            fluence.append(float(line.split()[1]))
            
    fluence = fluence/sum(fluence)
    
    if Verbose:
        plt.figure(44)
        plt.plot(energies,fluence)


    # In[109]:


    energies = []
    fluence = []
    with open(spectrum_file) as f:
        for line in f:
            energies.append(float(line.split()[0]))
            fluence.append(float(line.split()[1]))
            
    fluence = fluence/sum(fluence)

    if Verbose:

        plt.figure(44)
        plt.plot(energies,fluence)


    # In[88]:


    deposition_summed = np.load(deposition_efficiency_file,allow_pickle=True)
    # deposition_summed = np.append(deposition_summed[0],50000.5)
    deposition_summed = np.insert(deposition_summed,0,0)


    # In[89]:


    original_energies_keV = np.array([0, 30, 40, 50 ,60, 70, 80 ,90 ,100 ,300 ,500 ,700, 900, 1000 ,2000 ,4000 ,6000])
    deposition_interpolated = np.interp(np.array(energies)*1000, original_energies_keV, deposition_summed)


    # In[115]:


    super_kernel = np.zeros([len(fluence),kernels.shape[1],kernels.shape[2]])

    for ii in range(kernels.shape[1]):
        for jj in range(kernels.shape[2]):
            
            super_kernel[:,ii,jj] = np.interp(np.array(energies)*1000, original_energies_keV, kernels[:,ii,jj])
            
    if Verbose:

        plt.figure()
        plt.imshow(super_kernel[:,25,:])

        plt.figure()
        plt.imshow(kernels[:,25,:])


    # In[118]:


    weights = fluence*deposition_interpolated
    weights = weights/sum(weights)


    # In[119]:

    if Verbose:

        plt.figure()
        plt.plot(weights)



    normalized_kernel = super_kernel.copy()

    for ii in range(0,normalized_kernel.shape[0]):
        
        normalized_kernel[ii,:,:] = super_kernel[ii,:,:]/sum(super_kernel[ii,:,:])
    
    if Verbose:

        plt.figure()
        plt.imshow(normalized_kernel[:,25,:], cmap=cm.jet, norm=LogNorm())


    # In[163]:


    actual_kernel_all = normalized_kernel.T*weights

    if Verbose:

        plt.figure()
        plt.imshow(actual_kernel_all[:,25,:], cmap=cm.jet, norm=LogNorm())

    actual_kernel = sum(actual_kernel_all,2)


    # In[215]:


    plt.figure()
    plt.imshow(actual_kernel_all[:,:,165], cmap=cm.jet, norm=LogNorm())
    # axis('image')
    plt.xlabel('X [mm]')
    plt.ylabel('Y [mm]')
    cbar = plt.colorbar()
    cbar.set_label('Counts')


    # In[212]:


    lsf = actual_kernel[25,:]

    # lsf = actual_kernel_all[:,25,170]

    # evens = lsf[::2]
    # odds = lsf[1::2]

    # lsf_binned = (evens +odds)/2

    # lsf = lsf_binned


    # In[213]:


    # mtf = np.absolute(np.fft.fft(lsf, 128))
    # mtf_final = np.fft.fftshift(mtf)


    plt.figure(1)
    # plt.plot(mtf_final[64:]/mtf_final[64])

    T = 0.784
    N = 50

    xf = np.linspace(0.0, 1.0/(2.0*T), int(N/2))

    mtf = np.absolute(np.fft.fft(lsf))
    mtf_final = np.fft.fftshift(mtf)

    plt.plot(xf[:24],mtf_final[25:49]/mtf_final[25])
    plt.ylim(0,1.1)
    # plt.xlim(0,0.784)
    plt.grid(which='both')
