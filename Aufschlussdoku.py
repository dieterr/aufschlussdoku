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
    strat_ok = float(0.0)
    for line in reader:
        if line[0].find("Tiefe bis [m]") <> 0:
            strat_ct = strat_ct + 1
            strat_d = line[0].replace(",", ".");
            strat_uk = float(strat_d) + float(strat_ok)
            strat_uk_txt = str(strat_uk).replace(".", ",");
            strat_h = line[0]
            strat_n = line[1]
            strat_b = line[2]
            strat_p = line[3]
            strat_a = line[4]
            strat = [strat_d, strat_uk, strat_h, strat_n, strat_b, strat_p, strat_a]
            print strat
            strats.append(strat)
            start_x_0 = start_x
            box_nr = int(0)

            for box in boxes:
                box_n = box[0] + str(strat_ct)
                box_txt = strat[box_nr + 2]
                box_txt_n = box_n + "txt"
                print box_nr
                print box_txt
                #print box_n, box_txt_n, dimensions[1], position
                scribus.createRect(start_x_0, start_y, float(box[1]), float(strat_d)*2.0, box_n)
                scribus.setLineWidth(0.567, box_n)
                if box_nr == 0:
                    scribus.createText(start_x_0 + 0.1, start_y + (float(strat_d) * 2.0) - 0.4, float(box[1]) - 0.2, 0.4, box_txt_n)
                    box_txt = strat_uk_txt
                else:
                    scribus.createText(start_x_0 + 0.1, start_y + 0.1, float(box[1]) - 0.2, (float(strat_d)*2.0) - 0.1, box_txt_n)
                scribus.setText(box_txt, box_txt_n)
                scribus.setStyle("Buchner_Standard", box_txt_n)
                start_x_0 = start_x_0 + float(box[1])
                #print start_x_0, start_y, box[1], strat_d
                box_nr = box_nr + 1
            start_y = start_y + float(strat_d) * 2.0
            start_x_0 = start_x
        print "end"

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
