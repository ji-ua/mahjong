#!/usr/bin/env python3

def ron_point(han):
    if han <= 1:
            return 1500, 1000
    elif han <= 2:
            return 3000, 2000
    elif han <= 3:
            return 5800, 3900
    elif han <= 5:
            return 12000, 8000
    elif han <= 7:
            return 18000, 12000
    elif han <= 10:
            return 24000, 16000
    elif han <= 12:
            return 36000, 24000
    elif han >= 13:
            return 48000, 36000
    
def tsumo_point(han):
    if han <= 1:
            return 500, 300
    elif han <= 2:
            return 1000, 500
    elif han <= 3:
            return 2000, 1000
    elif han <= 5:
            return 4000, 2000
    elif han <= 7:
            return 6000, 3000
    elif han <= 10:
            return 8000, 4000
    elif han <= 12:
            return 12000, 6000
    elif han >= 13:
            return 16000, 8000
    
def no_ten_point(num):
        if num == 1:
                return 3000
        if num == 2:
                return 1500
        if num == 3:
                return 1000
        
def ten_pai_point(num):
        if num == 1:
                return 3000
        if num == 2:
                return 1500
        if num == 3:
                return 1000