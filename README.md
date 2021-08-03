# data-driven
#codes written in summer 2021 for data driven computing method

simple spring bar example:
A simple example used to demonstrate the data driven method is a spring bar setup as follows. The material dataset is used to describe the behavior of the bar and the constraint set reflects the fact that the bar and spring is connected in series thus undergoing the same axial force. As a result at a given spring constant and total displacement there is only a set of points in the phase space that satisfies the relationship. 

![alt text](docs/springbarsetup.png)

The material is assumed to follow a linear relationship with an Gaussian additive nosie during sampling. It is then fit to a Gaussian process and the resulting predction plotted. Altough fitting a GP process to a linear relationship is not of much significance but same code can be used for more complicated material relationship.
The spring is assume to follow Hook's law.

![alt text](docs/springbar.png)
