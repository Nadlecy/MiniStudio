from easing_functions import *

def lerp(start, end, alpha:float, easing=LinearInOut()):
    return (start + (end - start) * easing.ease(alpha))

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def clamp01(num):
    return clamp(num, 0, 1)