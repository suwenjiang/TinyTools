import sys
import re
import os
import argparse

def get_formatted_in_a_file(path):
   with open(path) as file:
      allmsg= file.read()
      if "</" not in allmsg and '>' not in allmsg:
          print "unable to retrieve the log file"
          return []
      text0= allmsg.split('</')[0].split('>')
      all_formatted_msg=[]
      #text0 format [<Msg time="" type="" code="" source="" process="" thread="" methodName="" machine="" user="" elapsed=""', "msg..."]
      msg1=text0[0].split(" ") #split text[0] by white space
      msg1.append(text0[1])
      formatted_msg1=msg1[1:]
      all_formatted_msg.append(formatted_msg1)
      for i in allmsg.split('</')[1:-1]:
           msg2=i.split('>')[1:]
           formatted_msg2=msg2[0].split(" ")[1:]
           formatted_msg2.append(msg2[1])
           all_formatted_msg.append(formatted_msg2)
   return all_formatted_msg
def get_logfile_in_dir(log_path):
    try:
        fileslList=[]
        for root,dirname,files in os.walk(log_path):
            #print root,dir,files
            for file in files:
               # print file
                if os.path.splitext(file)[1]=='.log':
                    filePath=os.path.join(root,file)
                    if os.path.getsize(filePath)!=0:
                     fileslList.append(filePath )
        return fileslList
    except IOError,msg:
        print msg


def main_func(files,filter=None):
   count=0
   for i in files:
      filename=os.path.splitext(i)[0]+"_result.txt"
      print filename
      f=open(filename,'w')
      dd=get_formatted_in_a_file(i)
      if not dd is None:
          count=count+1
          for item in sorted(dd,key=lambda item:item[1]):
              for val in item:
                f.write(val+",")
              f.write("\n")
          f.close()


parser = argparse.ArgumentParser()
parser.add_argument("p",help="input directory or path of log file ",action="store")
# parser.add_argument("-f","--filter",help="use msgType[warning,info,fine,verbose,severe,debug] to filter the log",\
#                     choices=["w","i","f","v","s","d"],action="store")
args=parser.parse_args()
files=[]
if os.path.isfile(args.p) and os.path.splitext(args.p)[1]=='.log':
    files.append(args.p)

elif os.path.isdir(args.p):
    files=get_logfile_in_dir(args.p)
    if len(files)==0:
        print "The Current Dirtory don't container any log files"
        sys.exit()
else:
    print "log file is invalid"
    sys.exit()
main_func(files)