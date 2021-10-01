# data-driven

This is a documentation for the works done in summer 2021 on data driven computing by Jiingwen Zhao.

###Contents:
- [A short summary on data driven computing](README.md)
- [A knonwledge catchup for two possible directions](BO_multifid.md)
- Code implementation
    + [Simple spring bar example](SpringBar.md)
    + [Bayesian optimization example](BO.md)
    + [Iterative minimum distance solver](mindist.md)
    + [Maximum entropy based solver](maxent.md)
  
## A short summary on data driven computing

**1. Data driven computing paradigm**

The data-driven computing is a method designed to tackle large amounts of data. The key difference between the data-driven computing and traditional method is that the data-driven paradigm is independent of any empirical material modelling, therefore bypassing the potential errors and uncertainty in modelling. Meanwhile, the data-driven computing still ensures the result follows the fundamental compatibility and conservation laws, in contrast to techniques such as machine learning. 

Depending on the specific problem studied, the conservation law and compatibility law can be written in various forms. In the simplest case of potential field, denoted as scalar u, the field describes the global state of the system. Here the localization law extracts from u the local state at a given material point is
![](https://latex.codecogs.com/gif.latex?%5Cepsilon%20%3D%20%5Cnabla%20u), along with appropriate boundary conditions. 
The flux ![](https://latex.codecogs.com/gif.latex?%5Csigma) follows the conservation law 
![](https://latex.codecogs.com/gif.latex?%5Cnabla%20%5Ccdot%20%5Csigma%20%3D%20%5Crho) where ![](https://latex.codecogs.com/gif.latex?%5Crho) is is the source density.
The pair ![](https://latex.codecogs.com/gif.latex?z%20%3D%20%28%5Cepsilon%2C%5Csigma%29) hence describes the local state of a system at a given material point. The collection of these state functions z defines the global phase space Z and from it the constraint set ![](https://latex.codecogs.com/gif.latex?E%20%5Cin%20Z).

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
