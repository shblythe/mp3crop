mp3crop.py
==========

Python script to allow intuitive command line cropping of mp3 files.  It will also
normalise the volume of an mp3 file so that its max amplitude is 0dB, if it was
originally below that volume.

It makes the task of cropping and sorting a large number of mp3 files much more
efficient than using GUI tools.

# Dependencies
* mplayer
* bash
* python 3.4.1
* python module: getch 1.0 : https://pypi.python.org/pypi/getch

# What does it do?
## Invoking
mp3crop.py will act on either every mp3 file in the current directory (using the -a
switch) or on a specific file you pass to it.
For example `python mp3crop.py -a` would run the code on every file matching \*.mp3 in
the current directory.
`python mp3crop.py test.mp3` would act only on `test.mp3`

## Finding cropping start/end points
It will first play that file with mplayer so that you can preview it to work out what
the output filename should be.
Once you exit mplayer, it will then ask you for the output filename.
Then it will play the file again, but you will then use different keys to navigate
through the file:

Key | Action
----| ------
h | go back 1 second
l | go forward 1 second
j | go back 10 seconds
k | go forward 10 seconds
u | go back 60 seconds
i | go forward 60 seconds
, | go back 0.1 seconds
. | go forward 0.1 seconds
space | replay from the same position

What you are trying to do here is to find the start of the part of the mp3 you want to
keep.
Once you have found the appropriate position, press 'q' to carry on.

Then, you repeat the process, but looking for the end of the part you want to keep -
what you actually want to hear is the first part you want to throw away.  So, keep
going through the file until you hear what you don't want at the beginning of the clip.
Again, once you're done, press 'q' to carry on.

## Fading
You will then be asked if you want to fade.  So that your new mp3 file doesn't end
abruptly, you can tell mp3crop to fade out before cutting at the endpoint.  Enter the
number of seconds you want to fade out across, or 0 to stop dead.

## Processing
Once you've completed this process, mp3crop will do its stuff, and create a new mp3 file
which contains just the audio between the start point and the end point, faded if you
asked it to.
It will run through the file first to find the peak volume - if it's below 0dB, it will
also amplify the mp3 to this point.

## Reviewing, filing and deleting the original
Once it's done, it will run mplayer again so you can review the file.
You'll then be asked if it's OK - if it isn't, you'll be sent back to find the start
position and end position again, defaulting to the positions you selected before.
If it is OK, you'll be asked if you want to move the file to a subdirectory, if you
don't then your new file will be left in the current directory, otherwise you'll be
presented with a list of subdirectories to choose from, or you can press # to create a
new one.
You'll then be asked if you want to delete the original.

Note that all questions asked just require a single keypress - I wanted efficiency here!


