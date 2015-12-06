#! /usr/bin/env python3
from subprocess import call
import argparse
import sys
import time
import signal
import configparser
import tempfile
import shutil
import os
from os import listdir
import subprocess
import random
import urllib.request
import unittest


def check_value(tocheck):
  """
  **Args:**
    *tocheck (str)*: string to check_value

  **Returns:**
    *float*. The return code of this function is string coverted to float value.
    If string cannot by coverted to float program halt.
  """
  try:
    return float (tocheck)
  except ValueError:
    print ("Error in data file")
    shutil.rmtree(dirpath) 
    sys.exit(1)

def check_fts (speed,fps,time):
  """ Check exclusivity of sped,fps,time.

  **Args:**
    *speed (float)*: speed to check

    *fps (float)*: fps to check

    *time (float)*: time to check

   Program halt when there is only one value passed from user.
  """
  count=0
  if not speed:
    count+=1
  if not fps:
    count+=1
  if not time:
    count+=1
  if count==2:
    print ("Invalid fps|speed|time !")
    shutil.rmtree(dirpath)
    sys.exit(1)
def check_time (data,format):
  """
  **Args:**
    *data (str)*: string to check_time

    *format (str)*: format to check

  **Returns:**
    *time.strptime*. The return code of this function is time.strptime.
    If string cannot by coverted to time.strptime program halt.
  """
  try:
    return time.strptime(data,format)
  except ValueError:
    print ("Bad time format")
    shutil.rmtree(dirpath)
    sys.exit(1)
#def effect_params (string):
def parse_effects (string):
  """
   This is custom type for argparser
  **Args:**
    *string (str)*: string to parse

  **Returns:**
    *string*. The return code of this function is string
    If string cannot by coverted to time.strptime program halt.

  **Raises:**
       *argparse.ArgumentTypeError*
  """
     
  effect_par=['ColorMadness','ColorUp','ColorDown','ColorMiddle']
  ef_par=''.join(string)
  ef_par=ef_par.split(':')
  a=all( y.split('=')[0] in effect_par for y in ef_par)     
  b=all(len(y.split('='))==2 for y in ef_par)
  if not a or not b:
    raise argparse.ArgumentTypeError("Invalid Effect parameters")
  else:
   return string
def merge_files(file_data):
  """
  Merge input files to one temporary file

  **Args:**
    *file_data (str)*: data from file

  """
  #data = file_data.readlines()
  
  data = []
  with open(dirpath+'/tmp_data', 'w') as outfile:
    for x in file_data:
      data += x.readlines()
        
    data.sort(key = lambda x: x.split()[:-1])

     #Resolve duplicates
    out = []
    for x in data:
      if x.split()[:-1] not in [y.split()[:-1] for y in out]:
        out.append(x)

    for line in out:
      outfile.write(line)


    #print (data)
    #data.sort(key = lambda x: x.split()[:-1])
   # print (data)

def effect(effectpar):
  """
   This function process data from effect parameters
  **Args:**
    *effectpar (str)*: string to parse

  **Returns:**

    *string ColorMadness* - if effect ColorMadness should be applied

    *string ColorUp*     -color of inverse bars above zero

    *string ColorDown*   -color of inverse bars belowe zero

    *string ColorMiddle* -color of actuall data

  """
  ColorMadness="false"
  ColorUp=""
  ColorDown=""
  ColorMiddle=""

  ef_par=''.join(effectpar)
  ef_par=ef_par.split(':')
  for y in ef_par:
    if y.split('=')[0] =='ColorMadness':
      if y.split('=')[1] == "true" or y.split('=')[1] == "false":
        ColorMadness=y.split('=')[1]
        
    if y.split('=')[0] =='ColorUp':
          ColorUp=y.split('=')[1]

    if y.split('=')[0] =='ColorDown':
         ColorDown=y.split('=')[1]
      
    if y.split('=')[0] =='ColorMiddle':
          ColorMiddle=y.split('=')[1]
  return (ColorMadness,ColorUp,ColorDown,ColorMiddle)  

def url_parser(url):
  if url[0:4]=="http":
    try:
      urllib.request.urlretrieve(url,dirpath+'/tmp_netfile')
    except EnvironmentError:
       print (url,'not found !')
       shutil.rmtree(dirpath)
       sys.exit(1)

    infile = open(dirpath+'/tmp_netfile','r')
    return (infile)
  else:
      try:
        infile = open(url,'r')
        return (infile)
      except EnvironmentError:
        print ('File',url,'not found !')
        shutil.rmtree(dirpath)
        sys.exit(1)

def main():
  '''Generate animation from given data; return a video file''' 
  global dirpath 
  dirpath= tempfile.mkdtemp()
  #Parsing arguments
  conf_parser = argparse.ArgumentParser(
  
    add_help=False
      )
  conf_parser.add_argument("-f", "--conf_file",
  help="Specify config file", metavar="FILE")
  args, remaining_argv = conf_parser.parse_known_args()
  defaults = {
  "xmax" : "max",
  "xmin" : "min",
  "ymax" : "max",
  "ymin" : "min",
  "timeformat" : "[%Y/%m/%d %H:%M:%S]",
  "name" : "skj",
  }


  items=["blue","red","blue","green","orange","purple","yellow"]
  if args.conf_file:
      config = configparser.RawConfigParser(delimiters=(' '), comment_prefixes=('#'))
      config.read([args.conf_file])
      defaults = dict(config.items("Defaults"))
      if "effectparams" in defaults:
        ColorMadness,ColorUp,ColorDown,ColorMiddle=effect(defaults["effectparams"])
        if ColorUp:
          items[0]=ColorUp
        if ColorMiddle:
          items[1]=ColorMiddle
        if ColorDown:
          items[2]=ColorDown


   
  parser = argparse.ArgumentParser(
  parents=[conf_parser],
  description=__doc__,
  formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.set_defaults(**defaults)

  parser.add_argument('data', metavar='file',type=url_parser,help='data to proccess',nargs='+')


  parser.add_argument('-t','--TimeFormat', action='store',dest="timeformat",
                     help='Set value of timestamp format')

  parser.add_argument('-x','--Xmin', action='store',
                     dest='xmin',
                     help='x-min (default: min)')

  parser.add_argument('-X','--Xmax', action='store',
                     dest='xmax',
                     help='x-max (default:  max )')

  parser.add_argument('-y','--Ymin', action='store',
                     dest='ymin',                   
                     help='y-min (default: min)')

  parser.add_argument('-Y','--Ymax', action='store',
                     dest='ymax',                   
                     help='y-max(default:  max)')


  parser.add_argument('-S','--Speed', action='store',type=float,
                     dest='speed',
                     help='speed (default: 1 record/frame)')

  parser.add_argument('-T','--Time', action='store',type=float,
                     dest='time',
                     help='time (duration)')

  parser.add_argument('-F','--FPS', action='store' ,type=float,
                     dest='fps',
                     help='fps (default: 25)')

  parser.add_argument('-l', action='store',
                     dest='legend',
                     help='legend (default: find the max)')

  parser.add_argument('-g','--GnuplotParams', action='store',nargs='*',
                     dest='gnuplotparams',
                     help='GnuplotParams (default: n/a)')

  parser.add_argument('-e', action='store',nargs=1,
                      dest='effectparams',type=parse_effects,
                     help='EffectParams (default: n/a)')

  parser.add_argument('-n','--Name', action='store',
                     dest='name',
                     help='Name (default: n/a)')

  parser.add_argument('-v','--verbouse', action='store_true',
                      dest='verbouse',
                     help='verbouse (default: false)')

  parser.add_argument('-E','--IgnoreErrors', action='store_true',
                      dest='ignore',
                     help='Ignore errrors (default: false)')


  x=0
  frames=0
  args = parser.parse_args(remaining_argv)
  if not args.ymax:
    args.ymax="max"
  if not args.ymin:
    args.ymin="min"
  if not args.xmax:
    args.xmax="max"
  if not args.xmin:
    args.xmin="min"
  if not args.timeformat:
    args.timeformat="[%Y/%m/%d %H:%M:%S]"
  if not args.name:
    args.name="skj"

  #If file already exist add suffix name_i
  temp = args.name.split('/')[:-1]
  if not temp:
    dirr ="."
  else:
    dirr ="".join(temp)

  filenum=[]
  for subor in listdir(dirr):
    if args.name.split('/')[-1] == subor.rsplit("_")[0]:
      num=(subor.rsplit("_")[-1])[:-4]
      filenum.append(num)
    if args.name.split('/')[-1] == subor[:-4]:
      filenum.append('0')
  
  #result = int (max(filenum))
  results = [int(i) for i in filenum]
  if results:
    args.name =args.name + "_" + str(max(results) + 1)

  '''
  suf = 1
  if (os.path.isfile(args.name+'.mp4')):
    while (os.path.isfile(args.name + "_" + str(suf) +'.mp4')):
      suf +=1
    args.name = args.name + "_" + str(suf) 
  '''


  #Merge input files 
  merge_files(args.data)
            
  #Read data from merged input files
  with open(dirpath+'/tmp_data', 'r') as infile:
    data = infile.readlines()
  #Number of rows in input files
  rows_n=len(data)
  if rows_n==0:
    print ("Empty file !")
    shutil.rmtree(dirpath)
    sys.exit(1)

  #Checking input data file (correct fromat and type of value)
  times=[]
  value=[]
  
  for row in data:
        if row.strip():
          #print (row)
          tmfrmt=row.split()[:-1]
          collum=len(row.split())
          tmfrmt=" ".join(tmfrmt)
          value.append(check_value (row.split()[-1]))
          times.append(time.strftime(args.timeformat,check_time(tmfrmt,args.timeformat)))


  # Finding Ymax
  if args.ymax == "max" : 
        ymax=float (max(value))
  else:
    ymax=check_value(args.ymax)
       
  # Finding Ymin
  if args.ymin == "min" :
        ymin=float (min(value))
  else:
    ymin=check_value(args.ymin)
  
  # Finding Xmax
  if args.xmax == "max" :
        xmax=max(times)
  else:
    xmax=time.strftime(args.timeformat,check_time(args.xmax,args.timeformat))
  
  # Finding Xmin
  if args.xmin == "min" :
        xmin =min(times)
  else:
    xmin=time.strftime(args.timeformat,check_time(args.xmin,args.timeformat))

  if args.fps and args.speed and args.time:
    frames=rows_n/args.speed
    if args.time != frames/args.fps:
      parser.print_usage()
      print ("Invalid fps|speed|time")
      shutil.rmtree(dirpath)
      sys.exit(1)


  # Calculating how many frames have to be generated .
  #check_fts(args.speed,args.fps,args.time)
  if not args.fps  and args.speed and args.time:
    frames=rows_n/args.speed
    args.fps=frames/args.time

  if args.fps  and not args.speed and args.time:
    frames=args.fps * args.time
    args.speed = rows_n /frames

  if args.fps and args.speed and not args.time:
    frames=rows_n/args.speed
    args.time = frames / args.fps



  if args.fps and not args.speed and not args.time:
    args.speed = 1
    frames=rows_n/args.speed
    args.time = frames / args.fps

  if not args.fps and args.speed and not args.time:
    args.fps = 25
    frames=rows_n/args.speed
    args.time = frames / args.fps

  if not args.fps and not args.speed and args.time:
    args.fps = 25
    frames=args.fps * args.time
    args.speed = rows_n /frames


  if not frames :
    args.fps=25
    args.speed=1
    frames=rows_n/args.speed
    args.time = frames / args.fps
  

  #Printing basic information when --verbouse is true
  if args.verbouse:
    print ("FPS: ","%.2f" %args.fps)
    print ("TIME: ","%.2f" %args.time,"s")
    print ("SPEED: ","%.2f" %args.speed)
    print ("ROWS: ",rows_n)
    print ("FRAMES: ","%.2f" %frames)

  if isinstance(args.gnuplotparams, str):
    args.gnuplotparams=args.gnuplotparams.split()

  #Prepare Gnuploparameters to set in gnuplot
  if args.gnuplotparams:
    toset=['set '+y+'\n' for y in args.gnuplotparams]
    toset= ''.join(toset)
  else:
    toset=''
  if not args.legend:
    args.legend = ""

  if args.effectparams:
    #Assign values from function wich proceese effect parameters
    ColorMadness,ColorUp,ColorDown,ColorMiddle=effect(args.effectparams)  
    #List of colors for bars
    if ColorUp:
      items[0]=ColorUp
    if ColorMiddle:
      items[1]=ColorMiddle
    if ColorDown:
      items[2]=ColorDown

  if args.verbouse:
    print ("Generetaing frames...\n")
  #Main loop;each iteration generate temp gnuplot configuration file and call gnuplot to process data
  for x in range(0, int(frames)):
        rnd=dirpath+'/'+str(x)+'.png'
        filename=dirpath+'/temp.gp'
        if args.effectparams:
          if ColorMadness=="true":
            random.shuffle(items)

        if ymin>=0 and ymax>0:
            plot='plot  "'+str(infile.name)+'" every ::0::'+str(rows_n)+' using 1:( '+str(ymin)+'+( ( ($'+str(collum)+'-'+str(ymin)+')/'+str(frames)+')*' +str(x)+') ) axes x1y1 with boxes notitle linecolor rgb "'+items[1]+'",\
            "'+str(infile.name)+'" every ::0::'+str(rows_n)+\
            'using 1:(($'+str(collum)+'*0)+'+str(ymax)+'):('+str(ymax)+'-(('+str(ymax)+'-(($'+str(collum)+' >= 0)  ? $'+str(collum)+' : $'+str(collum)+'*0))/'+str(frames)+')*'+str(x)+'):(($'+str(collum)+'*0)+'+str(ymax)+'):('+str(ymax)+'-(('+str(ymax)+'-$'+str(collum)+')/'+str(frames)+')*'+str(x)+')\
            axes x1y1 with candlesticks notitle linecolor rgb "'+items[0]+'"\
            '
        if ymin<0 and ymax<=0:
            plot='plot  "'+str(infile.name)+'" every ::0::'+str(rows_n)+' using 1:((($'+str(collum)+'/'+str(frames)+')*' +str(x)+') ) axes x1y1 with boxes notitle linecolor rgb "'+items[1]+'",\
            "'+str(infile.name)+'" every ::0::'+str(rows_n)+\
            'using 1:(($'+str(collum)+'*0)'+str(ymin)+'):('+str(ymin)+'-(('+str(ymin)+'-(($'+str(collum)+' <= 0)  ? $'+str(collum)+' : $'+str(collum)+'*0))/'+str(frames)+')*' +str(x)+'):(($'+str(collum)+'*0)'+str(ymin)+'):(($'+str(collum)+'*0)'+str(ymin)+') \
             axes x1y1 with candlesticks notitle linecolor rgb "'+items[2]+'"\n\
            '
        if ymin<0 and ymax>0:
            #print (rows_n , collum , frames , x )
            plot='plot  "'+str(infile.name)+'" every ::0::'+str(rows_n)+' using 1:((($'+str(collum)+'/'+str(frames)+')*' +str(x)+') ) axes x1y1 with boxes notitle linecolor rgb "'+items[1]+'",\
            "'+str(infile.name)+'" every ::0::'+str(rows_n)+\
            'using 1:(($'+str(collum)+'*0)+'+str(ymax)+'):('+str(ymax)+'-(('+str(ymax)+'-(($'+str(collum)+' >= 0)  ? $'+str(collum)+' : $'+str(collum)+'*0))/'+str(frames)+')*'+str(x)+'):(($'+str(collum)+'*0)+'+str(ymax)+'):(($'+str(collum)+'*0)+'+str(ymax)+')\
            axes x1y1 with candlesticks notitle linecolor rgb "'+items[0]+'",\
            "'+str(infile.name)+'" every ::0::'+str(rows_n)+\
            ' using 1:(($'+str(collum)+'*0)'+str(ymin)+'):('+str(ymin)+'-(('+str(ymin)+'-(($'+str(collum)+' <= 0)  ? $'+str(collum)+' : $'+str(collum)+'*0))/'+str(frames)+')*' +str(x)+'):(($'+str(collum)+'*0)'+str(ymin)+'):(($'+str(collum)+'*0)'+str(ymin)+') \
            axes x1y1 with candlesticks notitle linecolor rgb "'+items[2]+'"\n\
            '
 #set style fill solid noborder\n\\n\
        cont='\
        set boxwidth 1 relative\n\
        set terminal png font "/usr/openwin/lib/X11/fonts/TrueType/Arial-Bold.ttf" 8\n\
        set output "'+rnd+\
        '"\n\
        set timefmt "'+ str(args.timeformat) +'"\n\
        set xdata time\n\
        set format x"%H:%M"\n\
         \n\
        set xlabel "Cas"\n\
        set ylabel "Hodnota"\n\
         \n\
        set title "'+str(args.legend)+'"\n\
         \n\
        set grid\n\
        set style fill  transparent solid 0.50 noborder\n\
        set yrange ['+str(ymin)+':'+str(ymax)+']\n\
        set xrange [ "'+str(xmin)+'":"'+str(xmax)+'" ]\n\
          '+toset+'\
        '+plot+'\
        ' 
        #Saving configuration             
        with open(filename, 'w') as out:
            out.write(cont)

         #Calling gnuplot
        with open(os.devnull, 'w') as shutup:    
          subprocess.call(['gnuplot',filename], stdout=shutup,stderr=shutup)

  #Finally genereta video file in mp4 format 
  if args.verbouse:
    print ("Genretaing video...\n")     
  with open(os.devnull, 'w') as shutup:
    subprocess.call(['ffmpeg','-r',str(args.fps),'-y','-i',dirpath+'/%d.png',args.name+'.mp4'], stdout=shutup,stderr=shutup)
 
  if args.verbouse:
    print ("Finsihed.... \nCleaning up...") 
 # Clean up temp files
  shutil.rmtree(dirpath)
  if args.verbouse:
    print ("Halting")
  sys.exit(0)

if __name__ == "__main__":
  try:
      main()

  except KeyboardInterrupt:
    shutil.rmtree(dirpath) 
    sys.exit(1)
  except configparser.Error:
    print ("Error in parsing config file")
    shutil.rmtree(dirpath) 
    sys.exit(1)
