# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:40:19 2023

Script aimed at ensuring security of SRT by safety connexion-deconnexion

"""

from Scripts.SRT_inline import *

SRT.connectAPM(False)
SRT.disconnect()
