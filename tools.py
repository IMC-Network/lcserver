def isFloat(value):
    try:
        float(value)

        return True
    except ValueError:
        return False

def isInt(value):
    try:
        int(value)

        return True
    except ValueError:
        return False

def assertAll(truths):
    for truth in truths:
        if not truth:
            return False
    
    return True