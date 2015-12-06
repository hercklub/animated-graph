Developer documentation
*************************
This document descibes all program opertions and tries to explain logic behind them.

Overview
========

Program firstly parse user input from line or from config file. In case when there are both, we save parameters from config file as defaults and overide them with paramaters from command line. For parsing we use standart libraries. *Argparser* handle parsing paramaters from command line and *Configparser* parsing config files.

Functions *parse_effects* and *effect* are used for additional parsing of effect paramaters in format described in manual.

After program identifies user input paramters we procced to read data file from file or url. 
All temp files will be located in directory created by *tempfile.mkdtemp()* .

In case of multiple input files, program merge them to one temp file using function *merge_files(file_data)*. File data is list containing input files.
This function is called even if there is only one input file.

Function then sort values in time using X data.

After that function tries to find duplicties. Duplicty is considered either X value with multiple Y values or multiple X values with same Y value.Function keeps only first occurences of X value and ignores others. After that function writes this values to temp file.

From now on program use only generated temp file for all operations.

We check file for bad Y values using function *check_value(tocheck)*
which tries to convert string to float, if conversion fails function print error messaage and quits. Program assume that Y data are only in last collum (in line separated with spaces), processing more then one Y value per line is not supported.

Similarly using functuion *check_time(data,format)* program tries to convert string to time_struct using *time.strptime(string,format)*.
In this case *format* is either default time format or format provided by user. 

If bad value (wrong time format, wrong value) is found, proram prints error message clean tempfiles and quits.

Now we need to calculate how many frames we have to plot.Program use default values if user did not specified otherwise.

For our animation effect we draw all X values at once with diffrent Y values for each frame. For each frame we generate new configuration file for *Gnuplot*. If user defined any paramaters for gnuplot we add them to configuration file.
For actuall plotting there is hardcoced some logic for gnuplot, generally we differentiate 3 diffrent scenarios.
Ploting only on positive Y axes , only on negative Y axes or on both at the same time. We need to know that for our inversion effect.

After we generated all frames with gnuplot, program calls *ffmpeg* to create video in mp4 format. Program cleans all temp files and quits.


Data Inputs
===========

Data inputs are single/multiple files or urls. They need to have two collums, first collum is considered as X value for ploting, in this case Time.In second collum they can be any number values.If duplicity is found, only first occurence is saved, rest are ignored.

Outputs
===========
Output for this program is one video file in user defined location. If program ends with error message, no output file is generated. If file with output name already exist, program adds *_i* at the end. Where *i* is increasing sequence of integers.

Arguments
=========

Program accepts several arguments from command line, detaily described in :ref:`tutorial`, if there is more then one occurance of given argument, only last is used, rest of them are ignored. If some of the optional arguments are not defined by user, program use default values.


Configuration file
===================

Program can proccess configuration file from user defined location. Arguments from command line have priority over arguments defined in configuration file.Program does not support more than one configuration file at the time.




