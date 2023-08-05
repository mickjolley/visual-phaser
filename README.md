# visual-phaser
Visual_Phaser.py automatically downloads chromosome images and data from GEDmatch's 
One-to-One Comparisons and stores them in a .xlsx file.

@author: mick jolley (email: mickj1948@gmail.com)

Visual_Phaser.py automatically downloads a GEDmatch One-to-One match between
individuals. The results are pasted into an .xlsx file which can be read by
Excel 2010, Libre Office or similar spreadsheet application. The result is in a format 
which allows you to start manual phasing immediately. No additional manipulations are 
required.

Any number of individals may be selected.

All 22 chromosomes may be downloaed at once. Alternatively, chromosomes to be
downloaded may be individually selected.

Chromosome 23 can be added to the list of selected chromosomes. In addition,
chromosome 23 can be selected alone.

The length of the downloaded match images can be varied as desired. The default
value of '1' results in the natural size.

Download and install Firefox before running this. 

reCAPTCHA management.
Press the <Enter> key when encountering a reCAPTCHA message. A short tone
alerts the user. If the window does not immediately change to the One-to-One
comparison page and turns opaque, scroll down to the 'VERIFY' captcha and start
clickingon traffic lights or whatever. Resist the urge to minimize the window 
to take a peek at what the program is doing (the answer is "nothing"). If you
do this make sure that you maximize it before the reCAPTCHA time-out expires,
otherwise the program will crash because it's trying to minimize an already 
minimized window. 

reCAPTCHA time-out.
The default time-out is 30 seconds. This can be changed to whatever you desire.

The operating variables are stored in the VPconfig.py file.

You must install the pillow, openpyxl and selenium modules before running this
program.

It is suggested that you creat a new folder to store Visual_Phaser.py
and the .xlsx files generated.

If AUTO_REC_PNTS is set to "True", SCALE_FACTOR, which is display-dependent, may 
have to be adjusted for the recombination lines to line up properly. AUTO_REC_PNTS 
is disabled if all the kits are phased kits. 

©2023 Michael E. Jolley
