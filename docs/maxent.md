# Max entropy data driven solver:

**code: maxent_solver.py**

This code implements the max entropy data driven solver proposed in the paper. It starts by considering a cluster of data points then gradually narrow down the target through iteration. The code gives a demonstration of how the weight of data points evolve over the time. (Yellow for p>0.01, orange for p>0.1, red for the current weighed average)

![alt text](maxent_demo.png)

_(fig1,2: learning rate = 0.01, fig 3,4: learning rate = 0.1)_

The pusedocode describing the logic of the the program is as followed:

## Pseudocode of the algorithm

**1.Initialize**

Initialize values as:

![alt text](https://latex.codecogs.com/gif.latex?%5Cbar%7Bz%7D%5E0%20%3D%20%5Cfrac%7B1%7D%7Bn%7D%5Csum_i%20z_i)

![alt text](https://latex.codecogs.com/gif.latex?z_0%5E%7B%280%29%7D%20%3D%20%5Cbar%7Bz%7D%5E0)

![alt text](https://latex.codecogs.com/gif.latex?%5Cfrac%7B1%7D%7B%5Cbeta%5E0%7D%20%3D%20%5Cfrac%7B1%7D%7Bn%7D%20%5Csum_i%20%7C%5Cbar%7Bz%7D%5E0%20-%20z_i%7C%5E2)

k=0, set annealing rate ![](https://latex.codecogs.com/gif.latex?%5Clambda), note that here ![](https://latex.codecogs.com/gif.latex?%7C%5Cbar%7Bz%7D%20-%20z_i%7C%5E2%20%3D%20%5Cfrac%7B1%7D%7B2%7DC%28%5Cbar%7B%5Cepsilon%7D-%5Cepsilon_i%29%5E2%20&plus;%20%5Cfrac%7B1%7D%7B2C%7D%28%5Cbar%7B%5Csigma%7D-%5Csigma_i%29%5E2), where C is a constant.

**2.weighed average value of z**

![alt text](https://latex.codecogs.com/gif.latex?c%5Ek_i%20%3D%20e%5E%7B-%5Cfrac%7B%5Cbeta%7D%7B2%7D%7Cz%5Ek-z_i%7C%5E%202%7D)

![alt text](https://latex.codecogs.com/gif.latex?Z%28z%5Ek%2C%5Cbeta%5Ek%29%20%3D%20%5Csum_i%20c_i%5Ek)

![alt text](https://latex.codecogs.com/gif.latex?P_i%28z%5Ek%2C%5Cbeta%5Ek%29%20%3D%20%5Cfrac%7Bc_i%5Ek%7D%7BZ%28z_k%2C%5Cbeta_k%29%7D)

![alt text](https://latex.codecogs.com/gif.latex?%5Cbar%7Bz%7D%5Ek%20%3D%20P_i%28z%5Ek%2C%5Cbeta%5Ek%29z_i%20%3D%20%28%5Cbar%7B%5Cepsilon%7D%5Ek%2C%5Cbar%7B%5Csigma%7D%5Ek%29)

**3.solve for the pysical relationship**
Here the simple spring bar example is used.

![alt text](https://latex.codecogs.com/gif.latex?u%5E%7Bk&plus;1%7D%20%3D%20L_0%5Cbar%7B%5Cepsilon%7D%5Ek%20&plus;%20%5Cfrac%7Bf%7D%7Bk%7D)

![alt text](https://latex.codecogs.com/gif.latex?%5Ceta%5E%7Bk&plus;1%7D%20%3D%20%5Cfrac%7B1%7D%7BC%7D%28%5Cfrac%7Bf%7D%7BA%7D-%5Cbar%7B%5Csigma%7D%5Ek%29)

**4.Progress schedule**
![alt text](https://latex.codecogs.com/gif.latex?%5Ctilde%7B%5Cbeta%7D%5E%7Bk&plus;1%7D%20%3D%20%28%5Csum_i%20p_i%28z%5Ek%2C%5Cbeta%5Ek%29%7Cz_i-%5Cbar%7Bz%7D%5Ek%7C%5E2%29%5E%7B-1%7D)

![alt text](https://latex.codecogs.com/gif.latex?%5Cbeta%5E%7Bk&plus;1%7D%20%3D%20%281-%5Clambda%29%20%5Cbeta%5Ek%20&plus;%20%5Clambda%5Ctilde%7B%5Cbeta%7D%5E%7Bk&plus;1%7D)

**5.Compute local state**

![alt text](https://latex.codecogs.com/gif.latex?%5Cepsilon%5E%7Bk&plus;1%7D%20%3D%20%5Cfrac%7B1%7D%7BL_0%7D%28u%5E%7Bk&plus;1%7D-%5Cfrac%7Bf%7D%7Bk%7D%29)

![alt text](https://latex.codecogs.com/gif.latex?%5Csigma%5E%7Bk&plus;1%7D%20%3D%20%5Cbar%7B%5Csigma%7D%5E%7Bk&plus;1%7D&plus;%20%5Ceta%5E%7Bk&plus;1%7D%5Cfrac%7BC%7D%7BL_0%7D)

![alt text](https://latex.codecogs.com/gif.latex?z%5E%7Bk&plus;1%7D%20%3D%20%28%5Cepsilon%5E%7Bk&plus;1%7D%2C%5Csigma%5E%7Bk&plus;1%7D%29)

**6.test for ending conditions**

If ![](https://latex.codecogs.com/gif.latex?%5Cbar%7Bz%7D%5E%7Bk&plus;1%7D%20%3D%20%5Cbar%7Bz%7D%5Ek), or ![](https://latex.codecogs.com/gif.latex?%5Cbeta%5E%7Bk&plus;1%7D) reaches Ifinity or NAN, or maximum iteration step is reached, ternimate the algorithm.

Else, k = k+1, continue from step 2.






