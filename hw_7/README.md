## Homework 7. Functional programming

### Describing
Script realises some functions for work with other functions and containers. 

### Preparation
For convenient utilizing this script I advise user to create virtual environment.

First of all, you should create virtual environment in acceptable directory (*func_venv* is a name for example).
```
python3 -m venv func_venv
```
Also you need activate this venv
```
source func_venv/bin/activate
```
The second step is the installation of the numpy module. This can be done in the following ways:
1. Install package numpy inside venv directly:
```
pip install sys==3.11.1
```
2. Through copy requiremets.txt from this repository (branch homework_7)
```
git clone https://github.com/Evgen01011/Python_BI_2022/homework_7
pip install -r ../Python_BI_2022/hw_7/requirements.txt
```


### Features
The script contain next function:  
- `sequential_map` - the function accepts any number of functions and the container with some values. The function returns a list of the results of sequential application of the passed functions to the values in the container.
    ```
    sequential_map(*args)
    ```
> Example: 
> Q: sequential_map(np.square, np.sqrt, lambda x: x**3, [1, 2, 3, 4, 5])
> R: [1, 8, 27, 64, 125]

- `consensus_filter` - the function accepts any number of functions that return True or False, as well as a container with some values. The function returns a list of values that, when passed to all functions, give True.
    ```
    consensus_filter(*args)
    ```
> Example: 
> 
> Q: consensus_filter(lambda x: x > 0, lambda x: x > 5, lambda x: x < 10, [-2, 0, 4, 6, 11])
> 
> R: [6]

- `conditional_reduce` - the function accepts 2 functions and the container with values. The first function should take 1 argument and return True or False, the second also takes 2 arguments and returns a value - the result of reduce, skipping the values with which the first function returned False.
    ```
    conditional_reduce(function1, function2, container)
    ```
> Example: 
> Q: conditional_reduce(lambda x: x < 5, lambda x, y: x + y, [1, 3, 5, 10])
> R: 4
 
 - `func_chain` - the function accepts as arguments any number of functions. The function returns a function combining all passed by sequential execution.
    ```
    func_chain(*args)
    ```
> Example: 
> Q: my_chain = func_chain(lambda x: x + 2, lambda x: (x/4, x//4))
> Q: my_chain(37)
> R: (9.75, 9)

- `sequential_map_improved` - the analog of the `sequential_map` function, but with the use of `func_chain`.
    ```
    sequential_map_improved(*args)
    ```

 - `multiple_partial` - an analogue of the `partial` function, but which takes an unlimited number of functions as arguments and returns a list of the same number of "partial functions" with added kwargs.
    ```
    multiple_partial(*args, **keywords)
    ```
> Example: 
> ax1_mean, ax1_max, ax1_sum = multiple_partial(np.mean, np.max, np.sum, axis=1)

- ` bicycled_print` - an analogue of the `print` function.
Parameters:
- args: elements of output
- sep: arguments separator (by default - sep=' ')
- end: determinant of string finish (by default - end='\n')
- file: label of output - standard or in file (by default - file=sys.stdout)
    ```
    bicycled_print(*args, sep=' ', end='\n', file=sys.stdout)
    ```
> Example: 
> Q: bicycled_print('Why', 'am', 'I', 'doing', 'print', sep=' ', end='?')
> R: Why am I doing print?


