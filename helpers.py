from easing_functions import *

def lerp(start, end, alpha:float, easing=LinearInOut()):
    return (start + (end - start) * easing.ease(alpha))