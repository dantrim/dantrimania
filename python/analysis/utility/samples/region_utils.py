#!/usr/bin/env python

def regions_unique(region_list) :
    """ count the number of times a given region occurs in the region list,
        if the count is greater > 1 for any then return False. The metric used
        is the 'name' property of the region object."""

    name_list = [ r.name for r in region_list ]
    for region in region_list :
        if name_list.count(region.name) > 1 :
            return False
    return True

def region_counts(region_list) :
    """ return a dictionary of the count/occurences of the regions. The metric
        used is the 'name' property of the region object."""
    name_dict = {}
    name_list = [ r.name for r in region_list ]
    for region in region_list :
        name_dict[region.name] = name_list.count(region.name)
    return name_dict

def has_region(region_list = [], region_to_look_for = None) :
    """ provided a list of region objects, check if list contains the
        region object 'region_to_look_for' """
    found_region = False
    for region in region_list :
        if region.name == region_to_look_for :
            found_region = True
            break
    return found_region
