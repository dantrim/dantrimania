#!/usr/bin/env python


class Region(object) :
    def __init__(self, name = "", displayname = "") :
        self._name = name
        self._displayname = displayname
        self._tcut_str = ""

    @property
    def name(self) :
        return self._name
    @name.setter
    def name(self, val) :
        self._name = val

    @property
    def displayname(self) :
        return self._displayname
    @displayname.setter
    def displayname(self, val) :
        self._displayname = val

    @property
    def tcut(self) :
        """selection string formatted as ROOT TCut"""
        return self._tcut_str
    @tcut.setter
    def tcut(self, val) :
        self._tcut_str = val

    def __str__(self) :
        return "Region    name = %s  displayname = %s  selection = %s" % ( self.name, self.displayname, self.tcut )
