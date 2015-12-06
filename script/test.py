#! /usr/bin/env python3
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Test number.')
parser.add_argument('integers', type=int ,nargs = '*',action = 'store',
                   help='Number of test to run')

args = parser.parse_args()

#1
if 1 in args.integers or not args.integers :
	print ( "1. Basic Test" )
	subprocess.call(['./animated_graph.py','Tests/data','-S','10','-F','30','-n','Tests/basic','-v'])

#2
if 2 in args.integers or not args.integers :
	print ("2. Data from url")
	subprocess.call(['./animated_graph.py','http://filebin.ca/20lOzA2LS7iO/data','-S','10','-F','30','-n','Tests/url','-v'])

#3
if 3 in args.integers or not args.integers :
	print( "3. Multiple data files test not in order" )
	subprocess.call(['./animated_graph.py','Tests/data2','Tests/data1','-S','10','-F','30','-n','Tests/multiple_files21'])

#4
if 4 in args.integers or not args.integers :
	print( "4. Multiple data files test" )
	subprocess.call(['./animated_graph.py','Tests/data1','Tests/data2','-S','10','-F','30','-n','Tests/multiple_data_files12'])
#5
if 5 in args.integers or not args.integers :
	print( "5. Multiple data files with overlay test" )
	#subprocess.call(['./animated_graph.py','Tests/overlay1','Tests/overlay2','-S','10','-F','30','-n','Tests/overlay','-v'])
	subprocess.call(['./animated_graph.py','Tests/overlay1','Tests/copy','-S','10','-F','30','-n','Tests/overlay','-v'])

#6
if 6 in args.integers or not args.integers :
	print ("6. Diffrent time format test") 
	subprocess.call(['./animated_graph.py','Tests/timeformat','-S','10','-F','30','-t','[%H:%M:%S %d.%m.%Y]','-n','Tests/timeformat'])

#7
if 7 in args.integers or not args.integers :
	print ("7. Additional effect test (Color Madness)")
	subprocess.call(['./animated_graph.py','Tests/data','-S','10','-F','30','-e','ColorMadness=true','-n','Tests/color_madness'])

#8
if 8 in args.integers or not args.integers :
	print ("8. Additional effect test (Changed color)")
	subprocess.call(['./animated_graph.py','Tests/data','-S','10','-F','30','-e','ColorUp=pink','-n','Tests/color_change'])

#9
if 9 in args.integers or not args.integers :
	print ("9. Xmax/Xmin test")
	subprocess.call(['./animated_graph.py','Tests/data','-S','10','-F','30','-X','[2009/05/11 19:52:00]','-x','[2009/05/11 09:09:00]','-n','Tests/X'])

#10
if 10 in args.integers or not args.integers :
	print ("10. Ymax/Ymin test")
	subprocess.call(['./animated_graph.py','Tests/data','-S','10','-F','30','-y','0.1','-Y','0.6','-n','Tests/Y'])

#11
if 11 in args.integers or not args.integers :
	print ("11. Config overide test") 
	#subprocess.call(['./animated_graph.py','Tests/data','-e','ColorUp=black','-f','Tests/test.conf','-n','Tests/conf_overide'])
	subprocess.call(['./animated_graph.py','Tests/data','-T','5','-f','Tests/test.conf','-n','Tests/conf_overide'])

#12
if 12 in args.integers or not args.integers :
	print ("12. Arguments overide") 
	subprocess.call(['./animated_graph.py','Tests/data1','-S','10','-F','30','-n','Tests/not_this','-n','Tests/this'])

#=======================================================================================================================================================

#13
if 13 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/nonexistingfile'])

#14
if 14 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/data','-S','10'])

#15
if 15 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/emptyfile'])

#16
if 16 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/badYdata'])

#17
if 17 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/badXdata'])

#18
if 18 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','-t','[Notctualforma%]','Tests/data'])

#19
if 19 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','http://probablynotvalidurl.com/data','-S','10','-F','30','-n','Tests/url'])

#20
if 20 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/data','-f','Tests/bad.conf','-n','Tests/nothing'])

#21
if 21 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/data','-f','Tests/nonexisting.conf','-n','Tests/nothing'])
#22
if 22 in args.integers or not args.integers :
	subprocess.call(['./animated_graph.py','Tests/data','-t','[%H:%M:%S %d.%m.%Y]','-n','Tests/wrongtimeformat'])




