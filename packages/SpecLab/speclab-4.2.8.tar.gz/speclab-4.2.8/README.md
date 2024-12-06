# imXam:  v4.2.7

**imXam** is an interactive FITS image viewer for quick-look analysis and data quality assessment.
**imXam** is the first interactive program finished for the **SpecLab** Python
data reduction package.  More (identify, standard, sensfunc, apall) will be added
with the same GUI design (PyQtGraph + Plotly) in the future as these get finished.
**SpecLab** is distributed with the MIT [License](https://choosealicense.com/licenses/mit/).

**imXam** uses [PyQtGraph](https://www.pyqtgraph.org/) 0.13.3, which will be installed automatically below.  
A customized version of a few routines (`ROI.py`, `GraphicsScene.py`, `ImageView.py`) will be copied
to your site-packages/pyqtgraph/ by running the config below.  The installation below will install PyQt6 (6.5.1).

author: Adam F Kowalski (2023-Dec-17)

## Installing imXam 

### Step 1

From terminal (if you want to install to your current conda environment; if not, go to Step 2):

`pip install SpecLab`


### Step 2

Create a conda environment to install into (recommended).  If you already have
run `pip install SpecLab` in that environment, then skip to Step 3 below.

To set up a fresh conda environment:

In a terminal window, type

`conda create --name your_env_name python=3.11`

`conda activate your_env_name`

`pip install SpecLab`


### Step 3

After pip install, run the command (from anywhere), which will untar the modifications to PyQtGraph to your site-packages:

`SpecLab_config.py`

You may have to open a fresh tab in your terminal for your system to see the new routines in .../your_env_name/bin/.  You can also:

`cd /location_of_your_anaconda/anaconda3/envs/your_env_name/bin/`

`python SpecLab_config.py`

If SpecLab_config.py fails, it is likely a permissions issue.  Please check to make sure that you can write and untar to your site-packages/ directory.

### Basic Usage

You will then be able to run imXam.py from anywhere (it is located in .../anaconda3/envs/your_env_name/bin/).

Basic usage (or create an alias for `imXam.py -f` in your .bash_profile):

`imXam.py -f file.fits`

To get a list of command-line options, type in a Unix terminal:

`imXam.py -h`

To load in a spectrum with the dispersion axis vertical (e.g., ARC3.5m/KOSMOS spectrum):

`imXam.py -f KOSMOS_spectrum.fits -dispax 2`

To load in some reasonable parameters for tracing, extracting, etc with an ARCES / echelle spectrum, use:

`imXam.py -f ARCES_spectrum.fits -ec 1`

You can also create your own imXam_param.dat file and specify to load it in with `-i /full_path_to_custom_param/your_custom_param.dat`

You can edit imXam_param.dat directly from Unix command line by typing into a terminal:

`epar_imXam.py`

(requires vim)

Please see KNOWN_ISSUES.

Enjoy!


## Interactive Commands

Will need to left mouse click on PyQtGraph display image for these to register.  Please use the wheel on your mouse to zoom in and out of the PyQtGraph display window.

click 'h' key to print this to screen from within imXam:

The default parameters used to do the calculations are in imXam_param.dat.  You can edit this file from command line by typing `epar_imXam.py'


q:  quit imXam.

r:  plot radial profile, print fwhm, and print aperture photometry w/ sky annulus subtraction centered at cursor location; plot x-range can be set with RMax.

x:  trace and extract spectrum with sky subtraction, at cursor location (can change params in imXam_param.dat).

g:  fits a Gaussian to the spatial profile (uniform weighting in fit) of a spectrum at cursor location. An estimate of a constant background level (e.g., bias in a raw frame) is subtracted before the fit

T:  show (e.g., saturated) pixels above some threshold.  Prompts for a threshold above which to color red.

a:  print fwhm and apperture photometry w/ sky annulus subtraction centered at cursor location.

o:  plot contours at cursor location (not centroided) and shows in +/- Window.

z:  zoom in on cursor location (can change scaling with Zmax and Zmin and color table with Color).  Overplots the aperture photometry annuli.

s:  does exactly what x does but also saves the extraction as tmp.x1d.npy

t:  show a fit to a trace of a spectrum on the 2D image.

m:  prints to terminal various statistics in a box +/- Statsec centered at cursor location.

l:  plot a row (line) through entire image at cursor location

c:  plot a column through entire image at cursor location

p:  show parameters in imXam_param.dat but dont edit.

e:  edit parameters in imXam_param.dat; use p to see which can be edited.

1 & 2:  clicking 1 in lower-left and 2 in upper-right will print stats within that box.

H:  prints header to file.header.txt and lastheader.txt; also prints EXPTIME and DATE-OBS to screen.


# To Upgrade

`pip install SpecLab --upgrade`

# To Uninstall

`pip uninstall SpecLab`

# Acknowledgments

Thanks to Isaiah Tristan and Yuta Notsu for testing and feedback on an early version.  Thanks to Bill Ketzeback for helpful feedback and testing the most recent versions.  Thanks to Gordon MacDonald for helpful suggestions.  Thanks to Graham Kerr and Chris Osborne for suggesting Plotly.

# Troubleshooting
On a Linux, one may have to try these commands if one gets an `xcb` [error](https://stackoverflow.com/questions/68036484/qt6-qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-thou/68058308#68058308) during `pip install SpecLab`:

`sudo apt install libxcb-cursor0`

or

`sudo apt install --reinstall libxcb-cursor0`

or

`sudo apt-get install --reinstall libxcb-xinerama0`

With certain versions of Linux (e.g., CentOS) that I have tested, PyQt6 does not yet install properly (an error message will appear during
installation).  If there is a problem during installation of
PyQt6, I have made a version of SpecLab/imXam available that uses PyQt5:  

`pip install SpecLab_PyQt5`

On Mac, there should be no problem with Intel processors.  For M1/2 processors, a build for PyQt6 will become available shortly.


# Known Issues 

Plotly opens a new tab in a browser each time it is used.  I am not sure how to fix this as searching for solutions for a while did not bring up any browser settings that could be modified.

Have not tested this in Jupyter Notebooks.  I don't think it will work yet in Jupyter Notebooks but you can try.

The spectral trace success relies on a decent to good Gaussian fit in the spatial direction at every ~20-50 columns, so this could fail entirely on spectra that are very out of focus and show double peaks.  I plan to fix this and make it more flexible in a future update.

When running epar_imXam.py, "Greys" is the only option for color map at the moment.  Will be changed in the future.

## Notable Updates

(4.2.7; 2023-Dec-17) Added a link in Troubleshooting to a version of SpecLab/imXam that uses PyQt5 instead of PyQt6.
