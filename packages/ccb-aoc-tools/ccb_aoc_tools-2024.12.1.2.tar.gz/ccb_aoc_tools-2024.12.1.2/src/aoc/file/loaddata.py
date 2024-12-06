# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 00:45:56 2024

@author: elija
"""

def loadData(filename):
    try:
        with open(filename) as file:
            return file.readlines()
    except Exception as ex:
        raise ex