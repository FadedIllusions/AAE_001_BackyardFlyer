# AAE_001_BackyardFlyer
Project 001 of Udacity's Autonomous Aerial Engineer ("Flying Car") Nanodegree, "Backyard Flyer".

![Quad Image](./images/drone.png)

This project was a basic introduction to the Udacidrone simulator, programming the quadrotor as a state machine, and creating waypoints for your quadrotor to follow -- as seen in backyard_flyer.py.

## To complete this project on your local machine, follow these instructions:

### Environment Setup Instructions
Read through the instructions below. If these commands look familiar to you, then you should use these VERY abbreviated instructions to get yourself set up.
  1. [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html) and then install by opening the file/app that you download.
  2. ```git clone https://github.com/udacity/FCND-Term1-Starter-Kit.git``` to clone the starter kit and then ```cd FCND-Term1-Starter-Kit``` nto that directory. If you have a windows machine, you must rename ```meta_windows_patch.yml``` to ```meta.yml``` as well.
  3. ```conda env create -f environment.yml``` to create the miniconda environment: this took me 10 minutes to run due to the large number of installs required.
  4. Cleanup downloaded libraries (remove tarballs, zip files, etc): ```conda clean -tp```
  5. ```source activate fcnd``` to activate the environment (you'll need to do this whenever you want to work in this environment).
  
### Backyard Flyer Setup
  1. Navigate to your ```FCND-Term1-Starter-Kit``` directory.
  2. Clone the backyard flyer repository. ```git clone https://github.com/udacity/FCND-Backyard-Flyer.git```
  3. Navigate to that repo. ```cd FCND-Backyard-Flyer```
  

***To run the above solution, replace the ```backyard_flyer.py``` within the ```FCND-Backyard-Flyer``` directory with one provided above.
