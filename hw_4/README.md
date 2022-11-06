#### Homework 4. numpy

**Describing**
Script realises some function for matrix and vector operation. Additionaly, if you run program directly you will see the creation of three arrays. 

**Preparation**
For convenient utilizing this script I advise user to create virtual environment.

First of all, you should create virtual environment in acceptable directory (*numpy_venv* is a name for example).
```
python3 -m venv numpy_venv
```
Also you need activate this venv
```
source numpy_venv/bin/activate
```
The second step is the installation of the numpy module. This can be done in the following ways:
1. Install package numpy inside venv directly:
```
pip install numpy==1.23.4
```
2. Through copy requiremets.txt from this repository (branch homework_4)
```
git clone https://github.com/Evgen01011/Python_BI_2022
pip install -r ../Python_BI_2022/hw_4/requiremets.txt
```
Inside venv you can run numpy_challenge.py or use its functions in own programs
```
python3 /path/to/script/numpy_challenge.py
```

**Features**
The script contain next function:  
- `matrix_multiplication` - the function accepts 2 matrices, multiplies them according to matrix rules and outputs the resulting matrix
    ```
    matrix_multiplication(array1, array2)
    ```
- `multiplication_check` - the function accepts a matrices list  
    If they can be multiplied by each other in the order in which they are in the list it returns *True*. If they cann't be multiplied it returns *False*
    ```
    multiplication_check(*arrays)
    ```
- `multiply_matrices` - the function accepts a matrices list
    It outputs the result of multiplication of n-dimensional array without broadcasting if it can be possible, or returns None if they cann't be multiplied
    ```
    multiply_matrices(*arrays)
    ```
- `effective_multiply_2d_matrices` - the function is similar to         `multiply_matrices` but it more effective for 2D arrays
    ```
    effective_multiply_2d_matrices(*2D_arrays)
    ```
- `compute_2d_distance` - the function takes 2 one-dimensional arrays (vectors) with a pair of values and calculates the distance between them
    ```
    compute_2d_distance(vector1, vector2)
    ```
- `compute_multidimensional_distance` - the function takes 2 one-dimensional arrays with any equal number of values and calculates the distance between them
    ```
    compute_multidimensional_distance(vector1, vector2)
    ```
- `compute_pair_distances` - the function takes a 2d array (each row is an observation, each column is a feature)
    The function calculates a matrix of pairwise distances and gives it to user.
    ```
    compute_pair_distances(array)
    ```



