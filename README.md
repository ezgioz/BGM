<!-- #region -->

*Monopoly Power and Endogenous Product Variety: Distortions and Remedies* : production of welfare graphs.
========================================================================================================

This code is created by Pablo Winant and further developped by Ezgi Ozsogut.

The code is maintained here https://github.com/ezgioz/BGM

Option 1: Installation
------------

Required programs to produce the graphs are
- a recent distribution of scientific Python for instance [Anaconda Python](https://store.continuum.io/cshop/anaconda/)
- the [dolo](https://github.com/EconForge/dolo) modeling package
- and the https://github.com/ezgioz/BGM is thre repository to be imported

Complete documentation with installation instructions for Dolo available at http://dolo.readthedocs.org/en/latest/


Option 2: Binder (remote machine access)
------------
- Or run the code on the remote machine which has all the necesaary installations the the project folder `(No installation is needed)`

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ezgioz/BGM/master)



Producing the graphs
--------------------

The code to produce the grapsh is contained in a [IPython](http://ipython.org/) notebook. The notebook will solve each version of the model with several values of the parameters. 

 To view and execute it on your __local computer__:
- Open a terminal and change the working directory so that it contains the `Produce Graphs.ipynb` file.
- Launch `ipython notebook`. This should open a list of notebooks in a web browser. Click on `ProduceGraphs.ipynb`.

To view and execute it on the __remote computer__ just clicj on the`Produce Graphs.ipynb` notebook.

##### The main notebook (Produce Graphs.ipynb)

This notebook solve various models for different parameter values and plots the associated welfare gains comparing competetitive equilibrium and planner equilibrium solutions. The models are coded using `dolo` specifications in the different `yaml` files in `model_files` folder. For the model solution code, see `BGM_solver` module. The welfare computations are based on a second order Taylor expansion of the decision-rule.
 For more information on the perturbation method see [the documentation](https://dolo.readthedocs.io/en/latest/perturbations.html) or [the source code](https://github.com/EconForge/dolo/blob/master/dolo/algos/perturbation.py) 

On this notebook run each code block by "ctrl+enter" for the following computation steps. (There is detailed information in this notebook for each step)


1 Define various scenarios

2 Compute welfares calling the "BGM_solver" module. More information in the file itself, see comments at each step. This file
- imports the model
- sets the information such as the paramater to be changed at each step
- solves the model for each case
- return the results 

3 Export results in a table (also export to excel)


Output
------

The resulting graphs and results are stored in the output folder. If you are running the code on the remote machine, you should save them on your local computer before leaving the remote machine. Changes you make on the code or the related ouput files won't be saved remotely. If you install python and dolo to use the BGM folder on your machine, ouput will be updated in the output folder automatically.
<!-- #endregion -->
