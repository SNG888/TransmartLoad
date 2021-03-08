#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for plots used in the initial clinical data analysis/checking
"""

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

import seaborn as sns
sns.set_style('ticks')
sns.set_palette("muted")


# Function to plot boxplot above histogram for one numeric variable
def plot_1col_boxhist(df, column):
    # Cut the window in 2 parts
    f, ((ax_box, ax_hist)) = plt.subplots(nrows=2, sharex=True, 
                                                gridspec_kw={"height_ratios": (.15, .85)})
 
    # Add a graph in each part
    sns.boxplot(df[column], ax=ax_box)
    sns.distplot(df[column], ax=ax_hist, kde_kws={'bw':1.5})
 
    # Remove x axis name for boxplot and histogram
    ax_box.set(xlabel='')
    ax_hist.set(xlabel='')
    
    # Title of combined plot
    ax_box.set_title(column, fontsize=15, fontweight='bold')

    f.set_size_inches((5,7))
    return f


# Function to plot boxplot above histogram for two numeric variables side by side 
def plot_2col_boxhist(df, column):
    # Cut the window in 2 parts
    f, ((ax_box1, ax_box2), (ax_hist1, ax_hist2)) = plt.subplots(nrows=2, ncols=2, sharex=True, 
                                                gridspec_kw={"height_ratios": (.15, .85),
                                                             "width_ratios": (.5, .5)})
 
    # RIGHT HAND SIDE PLOTS
    # Add a graph in each part
    sns.boxplot(df[column[0]], ax=ax_box1)
    sns.distplot(df[column[0]], ax=ax_hist1, kde_kws={'bw':1.5})
    
    # Remove x axis name for the boxplot and histogram
    ax_box1.set(xlabel='')
    ax_hist1.set(xlabel='')

    # Title of combined plot
    ax_box1.set_title(column[0], fontsize=15, fontweight='bold')

    # LEFT HAND SIDE PLOTS
    # Add a graph in each part
    sns.boxplot(df[column[1]], ax=ax_box2)
    sns.distplot(df[column[1]], ax=ax_hist2, kde_kws={'bw':1.5})
 
    # Remove x axis name for the boxplot and histogram
    ax_box2.set(xlabel='')
    ax_hist2.set(xlabel='')

    # Title of combined plot
    ax_box2.set_title(column[1], fontsize=15, fontweight='bold')
        
    f.set_size_inches((10,7))
    return f


# Function to plot bar charts for one categorical variables 
def plot_1col_bar(df, column):
    f, ax_bar = plt.subplots(nrows=1, ncols=1, sharex=True, 
                                                #gridspec_kw={"height_ratios": (.15, .85)}
                            )
    # Add graph
    sns.countplot(df[column], ax=ax_bar)
    
    # Remove x axis name for plot
    ax_bar.set(xlabel='')

    # Title of plot
    ax_bar.set_title(column, fontsize=15, fontweight='bold')
        
    f.set_size_inches((5,6))
    return f


# Function to plot bar charts for two categorical variables side by side 
def plot_2col_bars(df, column):
    # Cut the window in 2 parts
    f, ((ax_bar1, ax_bar2)) = plt.subplots(nrows=1, ncols=2, sharex=True, 
                                                gridspec_kw={"width_ratios": (.5, .5)})
 
    # Add a graph in each part
    sns.countplot(df[column[0]], ax=ax_bar1)
    sns.countplot(df[column[1]], ax=ax_bar2)
    
    # Remove x axis name for the plots
    ax_bar1.set(xlabel='')
    ax_bar2.set(xlabel='')

    # Title of each plot
    ax_bar1.set_title(column[0], fontsize=15, fontweight='bold')
    ax_bar2.set_title(column[1], fontsize=15, fontweight='bold')
        
    f.set_size_inches((10,6))
    return f

