#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')


# 
# Unit cell
# =========
# 
# This example shows how to display the unit cell with matplotlib.
# 

# In[1]:


from abipy.abilab import abiopen
import abipy.data as abidata

# Extract structure from netcdf file.
with abiopen(abidata.ref_file("sio2_kpath_GSR.nc")) as gsr:
    structure = gsr.structure

# Visualize sites structure.
structure.plot(color_scheme="Jmol")

# Wrap sites into first unit cell.
# sphinx_gallery_thumbnail_number = 2
structure.plot(to_unit_cell=True)


# In[2]:


from abipy.abilab import abiopen
import abipy.data as abidata

# Open the output file with GS calculation (Note the .abo extension).
# Alternatively, one can use `abiopen.py run.abo -nb`
# to generate a jupyter notebook.
abo = abiopen(abidata.ref_file("refs/si_ebands/run.abo"))

# Plot all SCF-GS sections found in the output file.
# Use abo.next_d2de_scf_cycle() for DFPT cycles.
scf_cycle = abo.next_gs_scf_cycle()
if scf_cycle is not None:
    scf_cycle.plot()

# If timopt -1, we can extract the timing and plot the data.
timer = abo.get_timer()
timer.plot_pie()

abo.close()


# In[3]:


import abipy.data as abidata
from abipy.abilab import abiopen

with abiopen(abidata.ref_file("sio2_SCR.nc")) as ncfile:
    # The SCR file contains a structure and electron bands in the IBZ.
    # We can thus use the ebands object to plot bands + DOS.
    print(ncfile)

    edos = ncfile.ebands.get_edos()
    ncfile.ebands.plot_with_edos(edos, title="KS energies used to compute the SCR file.")

    # sphinx_gallery_thumbnail_number = 2
    ncfile.plot_emacro(title="Macroscopic dielectric function of $SiO_2$ with local-field effects.")

    ncfile.plot_eelf(title="Electron Energy Loss Function of $SiO_2$")


# In[4]:


from __future__ import print_function

from abipy.abilab import abiopen
import abipy.data as abidata

# Read the Phonon DOS from the netcd file produced by anaddb (prtdos 2)
ncfile = abiopen(abidata.ref_file("trf2_5.out_PHDOS.nc"))
phdos = ncfile.phdos

# Print crystalline structure and zero-point energy.
print(ncfile.structure)
zpe = phdos.zero_point_energy
print("Zero point energy:", zpe, zpe.to("J"), zpe.to("Ha"))

# Compute free energy from 2 to 300 K (20 points)
# By default, energies are is eV and thermodynamic quantities are given
# on a per-unit-cell basis.
f = phdos.get_free_energy(tstart=2, tstop=300, num=20)
#f.plot()

# Plot U, F, S, Cv as a function of T.
# Use J/mol units, results are divided by formula_units.
phdos.plot_harmonic_thermo(units="Jmol", formula_units=1)

ncfile.close()


# In[9]:


from abipy.abilab import abiopen
import abipy.data as abidata

# Open the DEN.nc file
ncfile = abiopen(abidata.ref_file("si_DEN.nc"))

# The DEN file has a `Density`, a `Structure` and an `ElectronBands` object
print(ncfile.structure)

# To plot the KS eigenvalues.
#ncfile.ebands.plot()

density = ncfile.density
print(density)

# To visualize the total charge wih vesta
#visu = density.visualize("vesta"); visu()

# To plot the density along the line connecting
# the first and the second in the structure:
density.plot_line(point1=0, point2=1)

# alternatively, one can define the line in terms of two points
# in fractional coordinates:
density.plot_line(point1=[0, 0, 0], point2=[2.25, 2.25, 2.25], num=300)

# To plot the density along the lines connect the firt atom in the structure
# and all the neighbors within a sphere of radius 3 Angstrom:
density.plot_line_neighbors(site_index=0, radius=3)


# In[2]:


import abipy.abilab as abilab
import abipy.data as abidata

# Open the file (alternatively one can use the shell and `abiopen.py FILE -nb`
# to open the file in a jupyter notebook
# This file has been produced on a k-path so it's not suitable for DOS calculations.
fbnc_kpath = abilab.abiopen(abidata.ref_file("mgb2_kpath_FATBANDS.nc"))

# Print file info (dimensions, variables ...)
# Note that prtdos = 3, so LM decomposition is not available.
print(fbnc_kpath)


# Plot the k-points belonging to the path.
fbnc_kpath.ebands.kpoints.plot()

# NC files have contributions up to L=4 (g channel)
# but here we are intererested in s,p,d terms only so
# we use the optional argument lmax
lmax = 2

# Plot the electronic fatbands grouped by atomic type.
fbnc_kpath.plot_fatbands_typeview(lmax=lmax, tight_layout=True)

# Plot the electronic fatbands grouped by L.
fbnc_kpath.plot_fatbands_lview(lmax=lmax, tight_layout=True)

# Now we read another FATBANDS file produced on 18x18x18 k-mesh
fbnc_kmesh = abilab.abiopen(abidata.ref_file("mgb2_kmesh181818_FATBANDS.nc"))

print(fbnc_kmesh)
#fbnc_kmesh.ebands.kpoints.plot()

# Plot the L-PJDOS grouped by atomic type.
fbnc_kmesh.plot_pjdos_typeview(lmax=lmax, tight_layout=True)

# Plot the L-PJDOS grouped by L.
fbnc_kmesh.plot_pjdos_lview(lmax=lmax, tight_layout=True)

# Now we use the two netcdf files to produce plots with fatbands + PJDOSEs.
# The data for the DOS is taken from pjdosfile.
# sphinx_gallery_thumbnail_number = 6
fbnc_kpath.plot_fatbands_with_pjdos(pjdosfile=fbnc_kmesh, lmax=lmax,
                                    view="type", tight_layout=True)

# fatbands + PJDOS grouped by L
fbnc_kpath.plot_fatbands_with_pjdos(pjdosfile=fbnc_kmesh, lmax=lmax,
                                    view="lview", tight_layout=True)

fbnc_kpath.close()
fbnc_kmesh.close()


# In[ ]:




