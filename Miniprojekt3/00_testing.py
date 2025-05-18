import kernel_function as kf
import svm
import data_split as ds

""" linear_kernel_func = kf.KernelFunction(kernelType='linear')
polynomial_kernel_func = kf.KernelFunction(kernelType='polynomial', degree=2, gamma=0.5, coeff0=0)
rbf_kernel_func = kf.KernelFunction(kernelType='rbf', gamma=0.1)

vector1 = [1, 2, 3]
vector2 = [4, 5, 6]

print(f"Linear Kernel: {linear_kernel_func(vector1, vector2)}")
print(f"Polynomial Kernel: {polynomial_kernel_func(vector1, vector2)}")
print(f"RBF Kernel: {rbf_kernel_func(vector1, vector2)}") """

a,b,c = ds.GetDataSplit()

svm.GetDecisiveFunction(a, kf.KernelFunction('linear'), 0)