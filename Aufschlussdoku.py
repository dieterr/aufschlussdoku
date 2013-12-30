#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    # Please do not use 'from scribus import *' . If you must use a 'from import',
    # Do so _after_ the 'import scribus' and only import the names you need, such
    # as commonly used constants.
    import scribus
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

#########################
# YOUR IMPORTS GO HERE  #
#########################
import csv

def main(argv):
    """This is a documentation string. Write a description of what your code
    does here. You should generally put documentation strings ("docstrings")
    on all your Python functions."""
    #########################
    #  YOUR CODE GOES HERE  #
    #########################
    csvfile = scribus.fileDialog("csv2table :: open file", "*.csv")
    reader = csv.reader(open(csvfile, "rb"), delimiter=";")
    #boxes = ["strat_d", "strat_n", "strat_b", "strat_p", "strat_a"]
    #boxes_b = [2.25, 2.25, 6.5, 2.3, 3.9]
    boxes = [["strat_d", 2.25], ["strat_n", 2.25], ["strat_b", 6.5], ["strat_p", 2.3], ["strat_a", 3.9]]
    start_x = float(1.9075)
    start_y = float(10.4864)
    strats = []
    strat_ct = int(0)
    for line in reader:
        if line[0].find("Tiefe bis [m]") <> 0:
            strat_ct = strat_ct + 1
            strat_d = line[0].replace(",", ".");
            strat_h = line[0]
            strat_n = line[1]
            strat_b = line[2]
            strat_p = line[3]
            strat_a = line[4]
            strat = [strat_d, line[0], line[1], line[2], line[3], line[4]]
            print strat
            strats.append(strat)
            start_x_0 = start_x

            for box in boxes:
                box_n = box[0] + str(1) #str(strat_ct)
                #dimensions = scribus.getSize(box_n)
                #position = scribus.getPosition(box_n)
                #print box_n, dimensions[1], position
                #box_n_new = box + str(strat_c + 1)
                #h = scribus.createRect(start_x_0, start_y, float(strat_d)*2.0, float(box[1]))
                start_x_0 = start_x_0 + float(box[1])
                print start_x_0, start_y, box[1], strat_d
                #areaname = scribus.getSelectedObject()
                #areaposition= scribus.getPosition(areaname)
                #scribus.sizeObject(dimensions[0],float(strat_d)*2.0,box_n)
                ## scribus.copyObject(box_n)
                ## scribus.pasteObject(box_n)
                ## shiftamount = float(strat_d)*2.0
                ## scribus.moveObject(shiftamount, 0, box_n)
            start_y = start_y + float(strat_d) * 2.0
            start_x_0 = start_x
        print "end"

    ## print strats[:]
    ## if len(strat_h) == 0:
    ##      print "Fertig!"
    ##      sys.exit(1)
    ## else:
    ##      print strat_h
    ##      strat_id = 1
    ##      for c in collist:
    ##           strat = c + str(strat_id)
    ##           print strat
    ##           dimensions=scribus.getSize(strat)
    ##           sizeObject(dimensions[0],float(strat_h)*2.0,strat)
    ##           #setFillColor("green", i,strat)
    ##           #strat_id = strat_id + 1

def main_wrapper(argv):
    """The main_wrapper() function disables redrawing, sets a sensible generic
    status bar message, and optionally sets up the progress bar. It then runs
    the main() function. Once everything finishes it cleans up after the main()
    function, making sure everything is sane before the script terminates."""
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)
