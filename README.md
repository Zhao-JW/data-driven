# data-driven

This is a documentation for the works done in summer 2021 on data driven computing by Jiingwen Zhao.

### Contents:
- [A short summary on data driven computing](README.md)
- [A knonwledge catchup for two possible directions](docs/BO_multifid.md)
- Code implementation
    + [Simple spring bar example](docs/SpringBar.md)
    + [Bayesian optimization example](docs/BO.md)
    + [Iterative minimum distance solver](docs/mindist.md)
    + [Maximum entropy based solver](docs/maxent.md)
  
## A short summary on data driven computing

**1. Data driven computing paradigm**

The data-driven computing is a method designed to tackle large amounts of data. The key difference between the data-driven computing and traditional method is that the data-driven paradigm is independent of any empirical material modelling, therefore bypassing the potential errors and uncertainty in modelling. Meanwhile, the data-driven computing still ensures the result follows the fundamental compatibility and conservation laws, in contrast to techniques such as machine learning. 

Depending on the specific problem studied, the conservation law and compatibility law can be written in various forms. In the simplest case of potential field, denoted as scalar u, the field describes the global state of the system. Here the localization law extracts from u the local state at a given material point is
![](https://latex.codecogs.com/gif.latex?%5Cepsilon%20%3D%20%5Cnabla%20u), along with appropriate boundary conditions. 
The flux ![](https://latex.codecogs.com/gif.latex?%5Csigma) follows the conservation law 
![](https://latex.codecogs.com/gif.latex?%5Cnabla%20%5Ccdot%20%5Csigma%20%3D%20%5Crho) where ![](https://latex.codecogs.com/gif.latex?%5Crho) is is the source density.
The pair ![](https://latex.codecogs.com/gif.latex?z%20%3D%20%28%5Cepsilon%2C%5Csigma%29) hence describes the local state of a system at a given material point. The collection of these state functions z defines the global phase space Z and from it the constraint set ![](https://latex.codecogs.com/gif.latex?E%20%5Csubset%20Z).

In the case of a simple linear elastic problem, the scalar field u now represents the displacement field. The strain tensor field is extracted as
![](https://latex.codecogs.com/gif.latex?%5Cepsilon%20%28x%29%20%3D%20%5Cfrac%7B1%7D%7B2%7D%28%5Cnabla%20u%28x%29&plus;%5Cnabla%20u%5ET%28x%29%29) by compatibility.
The stress tensor filed ![](https://latex.codecogs.com/gif.latex?%5Csigma) is extracted from the body force f as
![](https://latex.codecogs.com/gif.latex?%5Cnabla%20%5Ccdot%20%5Csigma%28x%29%20&plus;f%28x%29%20%3D%200) by equilibrium.
Along with the boundary conditions ![](https://latex.codecogs.com/gif.latex?u%28x%29%20%3D%20g%28x%29) and
![](https://latex.codecogs.com/gif.latex?%5Csigma%28x%29%5Cnu%28x%29%20%3D%20h%28x%29) where g is the boundary displacements, ![](https://latex.codecogs.com/gif.latex?%5Cnu) outer normal and h applied tractions. The above four equations form the constraint set in this problem setup.

In the case of a truss, the simplified material behaviour can be characterized by the uniaxial strain ![](https://latex.codecogs.com/gif.latex?%5Cepsilon_e) and uniaxial stress ![](https://latex.codecogs.com/gif.latex?%5Csigma_e) in the bar. 
Same as above, the state ![](https://latex.codecogs.com/gif.latex?z%20%3D%20%28%5Cepsilon%2C%5Csigma%29)is subjected to the compatibility and equilibrium constraints.  
The compatibility law ![](https://latex.codecogs.com/gif.latex?%5Csigma_e%20%3D%20B_eu), where where u is the array of nodal displacements and ![](https://latex.codecogs.com/gif.latex?B_e) he matrix describing the geometry and connectivity of the truss. The equilibrium law is described as
![](https://latex.codecogs.com/gif.latex?%5Csum%5Em_%7Be%3D1%7D%20B_e%5ET%20w_e%20%5Csigma_e%20%3D%20f) where f is the array of applied nodal forces. The constraint set is thus constructed.

**2. Solving the data-driven problem**

Two sets are set up and ready to be solved. Firstly, the constraint set C, which contains all the local points which satisfies the equilibrium and compatibility law, along its boundary conditions. This set is universal and material independent. Secondly, the material set E, which imperfectly characterises the material law by a set of local states. 

It can be proved that an ideal noise-free material data set which satisfies the following conditions gives solutions that converges to the classical solution.  A limiting material law is represented by a graph E in phase space, and that a sequence ![](https://latex.codecogs.com/gif.latex?E_k) of material data set satisfies: (i) there is a sequence ![](https://latex.codecogs.com/gif.latex?%5Crho_k%20%5Cdownarrow%200) such that ![](https://latex.codecogs.com/gif.latex?dist%28z%2CE_k%29%20%5Cleq%20%5Crho_k) for all ![](https://latex.codecogs.com/gif.latex?z%20%5Cin%20E), and (ii) there is a sequence ![](https://latex.codecogs.com/gif.latex?t_k%20%5Cdownarrow%200) such that
![](https://latex.codecogs.com/gif.latex?dist%28z_k%2CE%29%20%5Cleq%20t_k), for all ![](https://latex.codecogs.com/gif.latex?z_k%5Cin%20E_k). This is a good sanity check which helps proving the validity of the algorithm, however not overly useful in solving engineering problems.

While trying to solve the problem, generally, it is nearly impossible to directly find the intersect of the constraint set and material data set, various relaxation is therefore needed. One of the simplest ways to do it is finding the closest point z_i in the material dataset that is closest to the constraint set, through a properly defined distance d. However, this is prone to be affected by outliers caused by noise. The solver can be further updated to be probability driven, minimizing the weighed distance to a cluster of nearby material data points. The problem is then converted to minimizing the equivalent free energy
![](https://latex.codecogs.com/gif.latex?F%28z%2C%5Cbeta%29%20%3D%20-%5Cfrac%7B1%7D%7B%5Cbeta%7DlogZ%28z%2C%5Cbeta%29) over the constraint set, where
![](https://latex.codecogs.com/gif.latex?Z%28z%2C%5Cbeta%29%20%3D%20%5Csum_%7Bn%7D%5E%7Bi%3D1%7D%20%5Cexp%5E%7B-%28%5Cbeta/2%29d%5E2%28z%2Cz_i%29%7D) and 
![](https://latex.codecogs.com/gif.latex?p_i%28z%2C%5Cbeta%29%20%3D%20%5Cfrac%7B1%7D%7BZ%28z%29%7D%20%5Cexp%5E%7B-%28%5Cbeta/2%29d%5E2%28z%2Cz_i%29%7D) is given by the Boltzmann solution and ![](https://latex.codecogs.com/gif.latex?%5Cbeta%20%5Cin%20%280%2C&plus;%5Cinfty%29) a Pareto weight. This equation maximizes the Shannon’s information entropy while placing a lower weight for points distant from z.

A simulated annealing procedure is proposed to tackle the minimization as the free energy ![](https://latex.codecogs.com/gif.latex?F%28%5Ccdot%2C%5Cbeta%29) is strongly non-convex. However, at sufficiently small ![](https://latex.codecogs.com/gif.latex?%5Cbeta), F is convex. The initial condition can be
![](https://latex.codecogs.com/gif.latex?%5Cfrac%7B1%7D%7B%5Cbeta_0%7D%20%3D%20%5Cfrac%7B1%7D%7Bn%7D%5Csum_%7Bn%7D%5E%7Bi-1%7D%7C%5Cbar%7Bz%7D%5E%7B0%7D-z_i%7C%5E2), with 
![](https://latex.codecogs.com/gif.latex?%5Cbar%7Bz%7D%5E%7B0%7D%20%3D%20%5Cfrac%7B1%7D%7Bn%7D%5Csum%5E%7Bn%7D_%7Bi-1%7Dz_i)
Then the value ![](https://latex.codecogs.com/gif.latex?%5Cbeta) can be iteratively increased according to 
![](https://latex.codecogs.com/gif.latex?z%5E%28k&plus;1%29%3DP_C%20%28%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20p_i%20%28z%5E%7Bk%7D%2C%5Cbeta%5E%7Bk%7D%29z_i%29) and 
![](https://latex.codecogs.com/gif.latex?%5Cfrac%7B1%7D%7B%5Cbeta%5E%7Bk&plus;1%7D%7D%20%3D%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20p_i%20%28z%5E%7Bk%2C%5Cbeta%5Ek%7D%20%29%7Cz_i-%5Cbar%7Bz%7D%5Ek%7C%5E2). Here Pc is the closest-point projection to C. Furthermore, a control value on the annealing rate can be set as 
![](https://latex.codecogs.com/gif.latex?%5Cbeta%5E%7Bk&plus;1%7D%20%3D%20%5Clambda%20%5Ctilde%7B%5Cbeta%7D%5E%7Bk&plus;1%7D%20&plus;%20%281-%5Clambda%29%20%5Cbeta%5Ek)
, where ![](https://latex.codecogs.com/gif.latex?%5Ctilde%7B%5Cbeta%7D%5E%7Bk&plus;1%7D) is the result of the above iteration value. The solver operates in this manner until the values for ![](https://latex.codecogs.com/gif.latex?%5Cbeta) is large. Then it proceeds by distance minimization until convergence is reached. 
As discussed in the last chapter, this algorithm can be further improved. The width of the distribution is of order
![](https://latex.codecogs.com/gif.latex?%5Cbeta%20%5E%7B-1/2%7D)
, therefore it roughly only looks at data points within this range. In the early stage of the annealing, the algorithm looks at almost all the data points so it can be speed up by appropriate subsampling or summarizing. In the late stage of the algorithm only the data near the current point matters so the dataset can be truncated to reduce calculation as well.
