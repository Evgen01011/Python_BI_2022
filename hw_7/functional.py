import sys                                   # for 7 task


# I task - sequential map
def sequential_map(*args):
    if len(args[-1]) == 0:                   # check of list attendance
        return None
    temp = map(args[0], args[-1])            # execution of first function
    for function in args[1:-1]:
        temp = map(function, temp)           # execution of every function
    return list(temp)


# II task - consensus filter
def consensus_filter(*args):
    if len(args[-1]) == 0:                   # check of list attendance
        return None
    temp = filter(args[0], args[-1])         # execution of first filter
    for function in args[1:-1]:
        temp = filter(function, temp)        # execution of every filter
    return list(temp)


# III task - conditional reduce
def conditional_reduce(function1, function2, container):
    if len(container) == 0:                                # check of list attendance
        return None
    temp = list(filter(function1, container))              # execution of filter
    if len(temp) < 2:                                      # check possibility of error
        return None
    answer = function2(temp[0], temp[1])                   # combine first and second elements
    for i in temp[2:]:
        answer = function2(answer, i)                      # combine every function
    return answer


# IV task - functional chain
def func_chain(*args):
    def execute(*value):
        temp = map(args[0], value)                         # execution of first function
        for function in args[1:]:                          # subsequent execution
            temp = map(function, temp)
        return tuple(temp)
    return execute


# V task (integrated)
def sequential_map_improved(*args):
    unit = func_chain(*args[:-1])
    return unit(*args[-1])


# VI task - multiple partial
def multiple_partial(*args, **keywords):
    answer = []

    def modify(func, **keywords):                                   # apply parameters for every function
        def alter(*new_args, **new_keywords):                       # function for kwargs application/changing
            newkeywords = {**keywords, **new_keywords}
            return func(*new_args, **newkeywords)
        return alter

    for function in args:                                           # queue of function
        changed_function = modify(function, **keywords)
        answer.append(changed_function)
    return answer


# VII task - bicycled print
def bicycled_print(*args, sep=' ', end='\n', file=sys.stdout):
    gap = list(map(str, args))                                      # check of user activity
    result = sep.join(gap)                                          # insert gap
    result = ''.join([result, end])                                 # append end

    if file != sys.stdout:                                          # direct record
        with open(f'{file}', 'w') as output:
            output.write(result)
    else:
        sys.stdout.write(result)
