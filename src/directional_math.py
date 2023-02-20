def increment_heading(heading:int) -> int:
    if heading >= 359:
        return 0
    else:
        return heading + 1

def decrement_heading(heading:int) -> int:
    if heading <= 0:
        return 359
    else:
        return heading - 1

def add_heading(base:int, to_add:int) -> int:
    ToReturn = base
    for x in range(0, abs(to_add)):
        if to_add < 0:
            ToReturn = decrement_heading(ToReturn)
        elif to_add > 0:
            ToReturn = increment_heading(ToReturn)
    return ToReturn