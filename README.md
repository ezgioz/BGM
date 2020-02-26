<!-- #region -->

*Monopoly Power and Endogenous Product Variety: Distortions and Remedies* : production of welfare graphs.
========================================================================================================


Installation
------------

Required programs to produce the graphs are
- a recent distribution of scientific Python for instance [Anaconda Python](https://store.continuum.io/cshop/anaconda/)
- the [dolo](https://github.com/EconForge/dolo) modeling package

- Or run the code on Mybinder (link here) remote computer which has all the necesaary installations the the project folder `(No installation is needed)`

Complete documentation with installation instructions for Dolo available at http://dolo.readthedocs.org/en/latest/


Producing the graphs
--------------------

The code to produce the grapsh is contained in a [IPython](http://ipython.org/) notebook. The notebook will solve each version of the model with several values of the parameters. 

 To view and execute it on your __local computer__:
- Open a terminal and change the working directory so that it contains the `Produce Graphs.ipynb` file.
- Launch `ipython notebook`. This should open a list of notebooks in a web browser. Click on `ProduceGraphs.ipynb`.

To view and execute it on the __remote computer__ just clicj on the`Produce Graphs.ipynb` notebook.

##### The main notebook (Produce Graphs.ipynb)

This notebook solve the various models for different parameter values and plots the associated welfare gains comparing competetitive equilibrium and planner equilibrium solutions. The models are coded using `dolo` specifications in the different `yaml` files in `model_files` folder. For the model solution code, see "BGM_solver" module. For more information on the perturbation method see [the documentation](https://dolo.readthedocs.io/en/latest/perturbations.html) or [the source code](https://github.com/EconForge/dolo/blob/master/dolo/algos/perturbation.py)

On this notebook run each code block by "ctrl+enter" for the following computation steps


1 Define various scenarios

__Necesarry inputs__
- modfile: name of the model file (ces, cesds, exponential etc.) See 'model_file' folders. Each file includes the model equations, parameters, calibrations, exogenous process. 

- freeparam: name of the free parameter 

- range: range of this parameter (starting value, end value, number of grid points)

__Optional inputs__

- fixedparam: name of the parameter (which will be different than the baseline calbiration) that you want to change and plot

- value: value for this fixed parameter 

2 Compute welfares calling the "BGM_solver" module. More information in the file itself, see comments at each step. This file
- imports the model
- sets the information such as the paramater to be changed at each step
- solves the model for each case
- return the results 

3 Export results in a table (also export to excel)
Number of columns is equal to N which is the number of different values of the free paramater. So each line will give the results for one specific parameter value.
Each column computes

Run each code block by "ctrl+enter"

This is code 

The welfare computations are based on a second order Taylor expansion of the decision-rule.

Output
------

The resulting graphs are stored in the `BGM_welfare_gains.*` files.
<!-- #endregion -->
