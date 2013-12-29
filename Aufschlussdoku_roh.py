#!/usr/bin/python
# -*- coding: utf-8 -*-

#import locale
import csv


reader = csv.reader(open("Test_Bohrprofil_dieter.csv", "rb"), delimiter=";")

strats = []

for line in reader:
    ## print line[0]
    ## x = line[0].find("Tiefe bis [m]")
    ## print x
    if line[0].find("Tiefe bis [m]") <> 0:
        strat_d = line[0].replace(",", ".");
        strat_n = line[1]
        strat_b = line[2]
        strat_p = line[3]
        strat_a = line[4]
        strats.append([float(strat_d),strat_n,strat_b, strat_p, strat_a])
        print strat_d

print strats[:]
