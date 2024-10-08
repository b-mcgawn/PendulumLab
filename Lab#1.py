#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 19:32:30 2024

@author: bradymcgawn
"""

import numpy as np
import matplotlib.pyplot as plt

plt.ion()

######################################################################
# Function

def P_calc(rObs, COM, CtoS):
    
    #return 2*np.pi*(((COM**2)+(rObs-COM)**2)/g*(rObs-COM))**-.5
    return 2*np.pi/(2*g*(rObs-COM)/(COM**2+(CtoS)**2+2*(rObs-COM)**2))**.5
    #return 2*np.pi*((COM**2+2*(rObs-COM)**2)/2*g*(rObs-COM))**.5

    
def P_calc_simple(rObs, COM):
    return 2*np.pi/(g/(rObs-COM))**.5

def rObs(a, b, l, E):
    
    #radius of rotation
    rObs = l/(1-a/b)
    #distance from ski edge to center of mass
    COM = rObs/goldr
    #Distance from COM to start of skate
    CtoS = COM - E
    
    return [rObs, COM, CtoS]


######################################################################
# Constants

goldr = 1.618
g = 9.8 #m/s^2
size = 1000000


######################################################################
# measurements 
a = .27 #m
b = .41 #m
l = .35 #m
E = .04 #m

meterstick_err = .01 #m

pObs = np.array([4.36,4.20,4.14,4.20]) #time for 2 periods
timer_err = .1 #seconds

h_eq = 0.09 #meters

h_0 = .175 #meters


######################################################################
# Error analysis: 

# Calculate period: 
a_hist = np.random.normal(a, meterstick_err, size)
b_hist = np.random.normal(b, meterstick_err, size)
l_hist = np.random.normal(l, meterstick_err, size)
E_hist = np.random.normal(E, meterstick_err, size)

rads_hist = rObs(a_hist, b_hist, l_hist, E_hist)
pcalc_simple = P_calc_simple(rads_hist[0], rads_hist[1])
pcalc = P_calc(rads_hist[0], rads_hist[1], rads_hist[2])

pcalc_mean = np.mean(pcalc)
pcalc_std = np.std(pcalc)

simple_mean = np.mean(pcalc_simple)
simple_std = np.std(pcalc_simple)

# Measured period:
pObs_hist = 0
for i in range(len(pObs)):
    #convert each value to a histogram
    hist = np.random.normal(pObs[i], timer_err, size)
    pObs_hist += hist 

#take the mean
pObs_hist /= 2*len(pObs)
#divide by 2
pObs_mean = np.mean(pObs_hist)
pObs_std = np.std(pObs_hist)

#Plots
def Plot_hists(fignum = 88, plot_simple = True, bins = 100):
    plt.figure(fignum)
    plt.clf()

    plt.hist(pcalc, bins = bins, density = True, color = 'red',
             label = "Period modeled with moment of inertia", alpha = .7)
    plt.axvline(pcalc_mean, color = 'red', linewidth = 1)
    plt.axvline(pcalc_mean-pcalc_std, color = 'red', linewidth = 1)
    plt.axvline(pcalc_mean+pcalc_std, color = 'red', linewidth = 1)
    print("Mean of Moment of Inertia Period Model: "+str(pcalc_mean))
    print("Standard Deviation of Inertia Period Model: "+str(pcalc_std))
    
    plt.hist(pObs_hist,bins = bins, density = True, color = 'blue',
             label = 'Observed Period', alpha = .7)
    plt.axvline(pObs_mean, color = 'blue', linewidth = 1)
    plt.axvline(pObs_mean-pObs_std, color = 'blue', linewidth = 1)
    plt.axvline(pObs_mean+pObs_std, color = 'blue', linewidth = 1)
    print("Mean of Observed Period: "+str(pObs_mean))
    print("Standard Deviation of Observed Period: "+str(pObs_std))   

    if(plot_simple):
        plt.hist(pcalc_simple, bins = bins, density = True,
                 color = 'green', label = 'Period model without moment of inertia', alpha = .7)
        plt.axvline(simple_mean, color = 'green', linewidth = 1)
        plt.axvline(simple_mean-simple_std, color = 'green', linewidth = 1)
        plt.axvline(simple_mean+simple_std, color = 'green', linewidth = 1)

        print("Mean of Period model without moment of Inertia: "+str(simple_mean))
        print("Standard Deviation of Period model without moment of Inertia: "+str(simple_std))   


        
    plt.legend()
    plt.title('PDFs of Model Predictions and Data')
    plt.xlabel('Time (seconds)')

    return

Plot_hists()
Plot_hists(fignum = 90, plot_simple = False)
#plt.axvline(pObs_mean
    

######################################################################
# potential energy:

def U(m, rObs, COM, h_r):
    return m*g*h_r*(rObs-COM)/rObs

m_chair = 10 #kg
m_tommy = 55 #kg

m = m_chair + m_tommy

m_err = 5 #kg

mHist = np.random.normal(m, m_err, size)

h_r = h_0-h_eq 
hHist = np.random.normal(h_r, meterstick_err, size)

UHist = U(mHist, rads_hist[0], rads_hist[1], hHist)
