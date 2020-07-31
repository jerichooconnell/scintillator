#!/usr/bin/env python
# coding: utf-8

# # System tools to herd the dumps into something useful

# In[126]:
import os
import re

from topas2numpy import read_ntuple
from datetime import datetime
from pylab import figure, cm
from matplotlib.colors import LogNorm
from IPython.core.getipython import get_ipython
import numpy as np
from matplotlib import pyplot as plt

y = read_ntuple('PhotodiodeSurface.phsp')

particle_type = y['Particle Type (in PDG Format)']
event_id = y['Event ID']
xx = y['Position X [cm]']
yy = y['Position Y [cm]']

optical_event = particle_type == 0

plt.figure()

for ii in range(max(event_id)):

    indeces = event_id == ii

    if sum(indeces) > 0:

        plt.hist2d(xx[indeces],yy[indeces])



# %%
