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
import getpass

def main(argv):
    """This is a documentation string. Write a description of what your code
    does here. You should generally put documentation strings ("docstrings")
    on all your Python functions."""
    #########################
    #  YOUR CODE GOES HERE  #
    #########################
    script = "Aufschlussdoku.py"
    version = "20131231"
    csvfile = scribus.fileDialog("csv2table :: open file", "*.csv")
    fname_ext = csvfile[csvfile.rfind("/") + 1:]
    fname_noext = fname_ext[:fname_ext.rfind(".")]
    reader = csv.reader(open(csvfile, "rb"), delimiter=";")
    boxes = [["strat_d", 2.25], ["strat_n", 2.25], ["strat_b", 6.5], ["strat_p", 2.3], ["strat_a", 3.9]]
    start_x = float(1.9075)
    start_y = float(10.5)
    strats = []
    strat_ct = int(0)
    strat_ok = float(0.0)
    print getpass.getuser()

    for line in reader:
        if line[0].find("Tiefe bis [m]") <> 0:
            start_x_0 = start_x
            strat_ct = strat_ct + 1
            strat_d = line[0].replace(",", ".");
            strat_uk = float(strat_d) + float(strat_ok)
            strat_draw = float(strat_d) * 2.0
            strat_uk_draw = start_y + strat_draw

            if strat_uk_draw > 26.8:
                nPage = scribus.currentPage() + 1
                pageendtext = "Fortsetzung nächste Seite"
                #print nPage
                scribus.createText(start_x_0 + 0.1, start_y + 0.1, 17, 0.5, "box_txt_pageend")
                scribus.sentToLayer("profil_txt", "box_txt_pageend")
                scribus.setText(pageendtext, "box_txt_pageend")
                scribus.setStyle("Buchner_sehrklein", "box_txt_pageend")
                scribus.newPage(-1,"Buchner_Standard")
                scribus.gotoPage(nPage)
                start_y = float(5.5)
                strat_uk_draw = start_y + strat_draw
                
            box_nr = int(0)
            #print strat_uk
            #print "aktuelle Seite:", scribus.currentPage()

            #print strat_uk
            strat_uk_txt = str(strat_uk).replace(".", ",");
            #print strat_uk_txt
            strat_h = line[0]
            strat_n = line[1]
            strat_b = line[2]
            strat_p = line[3]
            strat_a = line[4]
            strat = [strat_d, strat_uk, strat_h, strat_n, strat_b, strat_p, strat_a]
            #print strat
            strats.append(strat)

            for box in boxes:
                box_n = box[0] + str(strat_ct)
                box_txt = strat[box_nr + 2]
                box_txt_n = box_n + "txt"
                
                #print box_nr
                #print box_txt
                #print box_n, box_txt_n, dimensions[1], position
                scribus.createRect(start_x_0, start_y, float(box[1]), strat_draw, box_n)
                scribus.setLineWidth(0.567, box_n)
                scribus.sentToLayer("profil_rahmen", box_n)
                if box_nr == 0:
                    scribus.createText(start_x_0 + 0.1, start_y + (strat_draw) - 0.4, float(box[1]) - 0.2, 0.4, box_txt_n)
                    #print strat_uk_txt
                    scribus.setText(strat_uk_txt, box_txt_n)
                else:
                    scribus.createText(start_x_0 + 0.1, start_y + 0.1, float(box[1]) - 0.2, (strat_draw) - 0.1, box_txt_n)
                    scribus.setText(box_txt, box_txt_n)
                scribus.setStyle("Buchner_Standard", box_txt_n)
                scribus.sentToLayer("profil_txt", box_txt_n)
                start_x_0 = start_x_0 + float(box[1])
                box_nr = box_nr + 1
            #print "end: strat count:", strat_ct
            start_y = strat_uk_draw
            start_x_0 = start_x
            strat_ok = strat_ok + float(strat_d)
    print "end: all"
    scribus.createText(start_x_0 + 0.1, start_y + 0.1, 17, 0.5, "box_txt_end")
    scribus.sentToLayer("profil_txt", "box_txt_end")
    endtext = "Erstellt von " + getpass.getuser() + " mit " + fname_ext + ", " + script + " (V" + version + ")"
    scribus.setText(endtext, "box_txt_end")
    scribus.setStyle("Buchner_sehrklein", "box_txt_end")
    scribus.saveDocAs(fname_noext + ".sla")

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
