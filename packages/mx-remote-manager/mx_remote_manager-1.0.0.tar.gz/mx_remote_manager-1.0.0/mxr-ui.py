##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

# MX Remote Manager Interface
import sys

if getattr(sys, 'frozen', False):
    import pyi_splash
    
import mx_remote_manager

if getattr(sys, 'frozen', False):
    pyi_splash.close()

mx_remote_manager.mxr_ui()