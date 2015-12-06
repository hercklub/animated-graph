# animated-graph
 Let you create animated data graph.


This is short desription about how to use animeted_graph

**usage**: animated_graph [-h] [-f FILE] [-t TIMEFORMAT] [-x XMIN] [-X XMAX]
                   [-y YMIN] [-Y YMAX] [-S SPEED] [-T TIME] [-F FPS]
                   [-l LEGEND] [-g GNUPLOTPARAMS [GNUPLOTPARAMS ...]]
                   [-e EFFECTPARAMS] [-n NAME]
                   file [file ...]



  -f FILE, --conf_file FILE               Specify config file.

  -t TIMEFORMAT, --TimeFormat 			  Specify timeformat which is udes in data file (default:"[%Y/%m/%d %H:%M:%S]").
                        
  -x XMIN, --Xmin XMIN  				  Specify  minimal x value, 
  can be int/float value or keyword:min (default:min).

  -X XMAX, --Xmax XMAX  				  Specify  maximal x value, can be int/float value or keyword:max (default:max).

  -y YMIN, --Ymin YMIN  				  Specify  minimal y value, can be int/float value or keyword:min (default:min).

  -Y YMAX, --Ymax YMAX  				  Specify  maximal y value, can be int/float value or keyword:max (default:max).

  -S SPEED, --Speed SPEED 				  Specify speed of animation (default:1).                     

  -T TIME, --Time TIME  				  Specify duration of animations in seconds.

  -F FPS, --FPS FPS    					  Specify FPS (frames per second) of animations (default:25).

  -l LEGEND             				  Specify legend (title) if animation

  -g GNUPLOTPARAMS 						  Specify parametrs which will be passed to gnuplot (only set parameters) any previous setting will be overdriven .

                        
  -e EFFECTPARAMS       				  Specify parameters of effect which are : ColorMadness=true/false,ColorUp=color,ColorDown=color,ColorMiddle=color,
  										  color=[red,blue etc..], (parameters are separated with ':')
  -n NAME, --Name NAME  				  Specify name of file to be produced wtih extension (name.mp4)
  -v, --verbouse                            verbouse (default: false)
    -h, --help            				 				 show this help message and exit

Example of usage in command line:
=================================



  ./arg_test.py data -T 10 -F 25 -t "[%Y/%m/%d %H:%M:%S]" -Y max -y min -e ColorMadness=true -X "[2009/05/12 07:29:00]" -x "[2009/05/11 07:30:00]" -n simple -g tics






Example of config file:
=======================



  [Defaults]
  #This need to be here

  #This is signle line comment

  # Graph animation : Simple Effect

  # Example config file
  
  Timeformat [%Y/%m/%d %H:%M:%S]

  Xmin [2009/05/11 07:30:00]

  Xmax [2009/05/12 07:29:00]

  Ymin -1

  Ymax 1

  Speed 20

  FPS 25

  Legend Test animation

  Gnuplotparams title grid

  Effectparams ColorUp=red:ColorDown=green

  Name test


**Example of data file:**

  Data are separate with spaces , last collum is considered as Y-value rest is dataformat as specified in *TimeFormat* 


  [2009/05/11 07:30:00] 0

  [2009/05/11 07:31:00] 0.00999983333416666468

  [2009/05/11 07:32:00] 0.01999866669333307936

  [2009/05/11 07:33:00] 0.02999550020249566076

  [2009/05/11 07:34:00] 0.03998933418663415945



