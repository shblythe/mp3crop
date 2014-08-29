#!/usr/bin/python

from getch import getch
import os
import shutil
import subprocess
import sys

bitrate='128k'

def seekpos(filename,posname,defaultvalue):
    print("keys: h-1 j-10 u-60 i+60 k+10 l+1 ,-0.1 .+0.1 q-done")
    pos=defaultvalue
    while True:
        print(posname,"=",pos)
        player=subprocess.Popen(
            ["mplayer","-ss",str(pos),"-quiet",filename],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        key=getch()
        player.terminate()
        if key=='h':
            pos-=1
        elif key=='l':
            pos+=1
        elif key=='j':
            pos-=10
        elif key=='k':
            pos+=10
        elif key=='u':
            pos-=60
        elif key=='i':
            pos+=60
        elif key==',':
            pos-=0.1
        elif key=='.':
            pos+=0.1
        elif key=='q':
            break
    return pos

def process_file(filename):
    print("Use mplayer interface to preview file to determine filename:")
    getch()
    player=subprocess.call(
        ["mplayer",filename]
    )
    outfile=input("Enter output filename, leave blank to skip file: ")
    if outfile!="":
        startpos=0
        endpos=0

        while True:
            print("First determine start position")
            startpos=seekpos(filename,"startpos",startpos)

            print("Now determine end position")
            endpos=seekpos(filename,"endpos",endpos if endpos!=0 else startpos)

            print("--------------------------------")
            print("startpos=",startpos)
            print("endpos=",endpos)

            fade=input("Enter fade-out time (0=no fade): ")
            player=subprocess.call(
                ["bash","./normalise",filename,outfile,bitrate,str(startpos),str(endpos),str(fade)]
            )
            print("Now review the output file")
            print("Use mplayer interface to review, press a key to start, q when done:")
            getch()
            player=subprocess.call(
                ["mplayer",outfile]
            )
            print("Was this OK? y/n")
            ok=getch()
            if ok=='y':
                break
        print("Move to directory? y/n")
        if getch()=='y':
            dirs=[d for d in os.listdir() if os.path.isdir(d)]
            dirs.sort()
            print("# > New Folder")
            for i,dirname in enumerate(dirs):
                print(chr(97+i),">",dirname)
            index=getch()
            if index=='#':
                dest=input("Enter directory name:")
                os.mkdir(dest)
            else:
                dest=dirs[ord(index)-97]
            shutil.move(outfile,dest)
    print("Delete original file? y/n")
    if getch()=='y':
        os.remove(filename)

if len(sys.argv)<2:
    print("Usage:",sys.argv[0],"filename - process one file")
    print("Usage:",sys.argv[0],"-a - process all *.mp3 files")
    exit()

if sys.argv[1]=='-a':
    filelist=shutil.fnmatch.filter(os.listdir(),'*.mp3')
    filelist.sort()
    for fn in filelist:
        print("*** FILE: ",fn)
        process_file(fn)
else:
    process_file(sys.argv[1])


