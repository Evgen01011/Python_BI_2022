import numpy as np

# Matrix creation
if __name__ == "__main__":
    # first array through list
    first_array = np.array([int(n) for n in range(16)], dtype='f2').reshape(8, -1)
    # second array through arange and sum
    second_array = np.arange(3, 21, 2).reshape(3, 3) + np.eye(3)
    # third array through random
    np.random.seed(123)
    third_array = np.random.randint(10, size=(3, 4, 2))


# Matrix multiplication
def matrix_multiplication(a, b):
    result = np.matmul(a, b)
    return result


# Strict multiplication check for n-dimensional array without broadcasting
def multiplication_check(*args):
    check = np.shape(args[0])[-2]                   # start position of rows
    d3_check = np.shape(args[0])[:-2]               # constant for high dimensions
    for matrix in args:
        # check rows and columns of two adjacent matrices and unchangeable other dimensions
        if np.shape(matrix)[-2] == check and np.shape(matrix)[:-2] == d3_check:
            check = np.shape(matrix)[-1]            # change row amount
        else:
            return False
    return True


# Matrix multiplication for n-dimensional array without broadcasting
def multiply_matrices(*args):
    if multiplication_check(*args):
        answer = matrix_multiplication(args[0], args[1])
        for matrix in args[2:]:
            answer = matrix_multiplication(answer, matrix)
        return answer
    else:
        return None


# Effective matrix multiplication for two-dimensional array without broadcasting
def effective_multiply_2d_matrices(*args):
    if multiplication_check(*args):
        return np.linalg.multi_dot(args)
    else:
        return None


# Calculation 2D vector length
def compute_2d_distance(a, b):
    dist = np.linalg.norm(a-b)
    return dist


# Calculation multidimensional vector length
def compute_multidimensional_distance(a, b):
    dist = np.linalg.norm(a-b)
    return dist


# Function calculating matrix of pairwise distances
def compute_pair_distances(a):
    main_factor = a.shape[0]                          # very often variable so create
    repeat_all_point = np.tile(a, (main_factor, 1))   # create some original matrix copies in one array
    repeat_one_point = np.repeat(a, main_factor, 0)   # create consistent repeat every observation
    # Find pairwise distances through difference previous arrays
    result = np.apply_along_axis(np.linalg.norm, 1, repeat_all_point - repeat_one_point).reshape(main_factor, -1)
    return result



