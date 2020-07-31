#!/usr/bin/env python
# coding: utf-8

# # System tools to herd the dumps into something useful

# In[126]:


get_ipython().run_line_magic('pylab', 'nbagg')

import os
import re

from topas2numpy import read_ntuple
from datetime import datetime
from pylab import figure, cm
from matplotlib.colors import LogNorm


# ## Making a new analysis directory

# In[171]:


now = datetime.now()

dt_string = now.strftime("%Y-%m-%d-h%Hm%M")

print(dt_string)

os.mkdir(f'analysis/{dt_string}')


# ## Reformat the dump

# In[ ]:


get_ipython().system('rename -e \'s/\\d+/sprintf("%04d",$&)/e\' -- *.csv')
get_ipython().system("ls *.csv | grep -o '[0-9][0-9]*' > energies.txt")
get_ipython().system("cat *.csv | awk 'NR % 6 == 0' > deposition.txt")
get_ipython().system('rename -e \'s/\\d+/sprintf("%04d",$&)/e\' -- *.phsp')
get_ipython().system('rename -e \'s/\\d+/sprintf("%04d",$&)/e\' -- *.header')


# In[123]:


#!cat energies.txt deposition.txt
#!cat deposition.txt


# In[111]:


with open('energies.txt') as f:
    energies = np.array([[x for x in line.split()] for line in f]).astype(np.float).flatten()
    
with open('deposition.txt') as f:
    array = np.array([[x for x in line.split()] for line in f]).flatten()
    deposition = array.astype(np.float)


# In[172]:


np.save(f'analysis/{dt_string}/EnergyDeposition.npy',[deposition,energies])


# In[190]:


plt.figure()
plt.semilogx(energies,deposition/energies,'bx')
plt.xlabel('MeV')
plt.ylabel('$\eta$')
plt.savefig(f'analysis/{dt_string}/EnergyDeposition.png')


# In[185]:


rootdir = "."
regex = re.compile('(.*phsp$)|(.*rar$)|(.*r01$)')

phase_spaces = []
plt.figure()

xedges = np.linspace(-1.5876,1.5876,82)
yedges = np.linspace(-1.5876,1.5876,82)

for root, dirs, files in os.walk(rootdir):
    for file in files:
        if regex.match(file):
            
            y = read_ntuple(file)
            xx = [y[kk][0] for kk in range(y.size)]
            yy = [y[kk][1] for kk in range(y.size)]
            
            h,xs,yx,ima = plt.hist2d(xx,yy, bins = [xedges,yedges], cmap=cm.jet, norm=LogNorm())
            plt.title(f'{file}')
            plt.savefig(f'analysis/{dt_string}/{file}.png')
            
            np.save(f'analysis/{dt_string}/{file}',h)

