import sys
tab = [1, 2, 43, 54, 32]

def search(n: int, tab):
    for i, j in enumerate(tab) :
        if j == n:
            return True, i+1
    return False, i+1

def tracer(frame, event, arg):
    print(event, frame.f_code.co_name, frame.f_lineno, arg)
    return tracer

sys.settrace(tracer)
print(search(43, tab))
sys.settrace(None)




print(sys.settrace(search(43,tab)))
