# Examining Explicit Discretization in Spectral Schemes -- Visual Analysis

The repository contains supplemental material for the EuroVis 2019 publication "Examining Explicit Discretization in Spectral Schemes".

The contents include:

- `Examining_EV19.ipynb`: a jupyter notebook with the code to generate the various static and interactive plots mentioned in both the paper and the Supplement.pdf.
- `ConvenienceClasses.py`: a set of convenience classes used by the pdf
- `data/`: a folder with additional resources needed by the jupyter notebook
-  `environment.yml`: the specification for a conda environment containing all the dependencies needed to run the jupyter notebook
- `postBuild`: a script used by the binder instance

To aid in reproducibility, we've made an interactive version of the `Examining_EV18.ipynb` notebook publicly available as part of a executable Binder environment on myBinder.org.
 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/samquinan/Examining_EV19/master?filepath=Examining_EV19.ipynb)

Since the Binder instance being hosted at myBinder.org is part of a research pilot, we have also included the specs for an Anaconda environment with all the relevant dependencies needed to run the jupyter notebook locally. Anaconda is a python and R distribution, with installation and package management tools and a complete overview of `conda` environments can be found in Anaconda's [documentation](https://conda.io/docs/user-guide/tasks/manage-environments.html). Below we outline the basic steps required to set up the included environment. These directions, tested on both macOS and Linux, assume that you have a working version of Anaconda [installed](https://docs.anaconda.com/anaconda/install/). If you are installing Anaconda for the first time, we also recommend familiarizing yourself with the steps in the [user guide](https://conda.io/docs/user-guide/getting-started.html) for starting and managing `conda` environments.

#### Locally Creating the Environment and Running the Jupyter Notebook 

- Navigate to included `Visual Analysis/` directory in your terminal (macOS and Linux) or in Anaconda Prompt (Windows).
- Run `conda env create -f environment.yml` to create the environment from the provided `environment.yml` file.
- Active the Examining2018-Env environment using the command:
	- `activate ExaminingEV19-Env` (Windows)
	- `source activate ExaminingEV19-Env` (macOS and Linux)
- You can verify that the new environment was installed correctly by running `conda env list`. You should see a list of environments with an asterisk (*) next to the `ExaminingEV19-Env` environment.
- From the same `Visual Analysis/` directory run the `jupyter notebook` command. This should launch a browser window containing the contents of the `Visual Analysis/` directory.
- Click on the `Examining_EV19.ipynb`. You now have a running version of the jupyter notebook. Running the cells in order should allow one to reproduce the various static and interactive plots used in our analysis.
- To stop serving the jupyter notebook, use `control-C` to stop the server and shut down all kernels.
- When you are done you can follow the documentation's steps for [deactivating](https://conda.io/docs/user-guide/tasks/manage-environments.html#deactivating-an-environment) and/or [removing](https://conda.io/docs/user-guide/tasks/manage-environments.html#removing-an-environment) the environment.