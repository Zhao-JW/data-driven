# Iterative minimum distance data driven solver:

**code: data_driven_solver.py**

This is a simple implmentation of the iterative data driven solver proposed  in the 2015 paper. The algorithm finds the minimum distance to a implicit constraint set based on noisless assumption. Iterative codes have been implemented but in the bar spring case no iteration is needed. The suedocode of the program is as below:

__Require: local data set E (pairs of know material data in the format (ϵ,σ)), applied force F (a scalar value)__

1.  Set k = 0, initial local data assignment:

	Choose <img src="https://render.githubusercontent.com/render/math?math=(\epsilon^{*},\sigma^{*})">
  randomly from E
  
2.  Solve for u and η by:
  <p align="center">
  <img src="https://render.githubusercontent.com/render/math?math=u^{k} = \epsilon^{*k}L_0 + \frac f k">
  </p>
  <p align="center">
  <img src="https://render.githubusercontent.com/render/math?math=\eta^k = \frac 1 C (\frac{f}{A}-\sigma^{*k})">
  </p> 
  
3.  Compute local states:
  <p align="center">
  <img src="https://render.githubusercontent.com/render/math?math=\epsilon^k=\frac 1 L_0 *(u^k-\frac{f}{k})">
  </p>
  <p align="center">
  <img src="https://render.githubusercontent.com/render/math?math=\sigma^k=\sigma^(*k)+\frac{C\eta^k}{L_0}">
  </p>
  
4.  Locate state assignment:

	Choose <img src="https://render.githubusercontent.com/render/math?math=(\epsilon^{*(k%2B 1)},\sigma^{*(k%2B 1)})">
  closest to <img src="https://render.githubusercontent.com/render/math?math=(\epsilon^{*},\sigma^{*})"> in E.
  
5.  Test for convergence:

	__If__ <img src="https://render.githubusercontent.com/render/math?math=(\epsilon^{*(k%2B 1)},\sigma^{*(k%2B 1)})=(\epsilon^{*},\sigma^{*})">
  , then:
  <p align="center">
  <img src="https://render.githubusercontent.com/render/math?math=u = u^k , (\epsilon,\sigma) = (\epsilon^{*},\sigma^{*})">
  </p>
  
  __Exit__
  
  __Else__
  k←k+1, goto (ii)

  __End if__
	
The distance is defined by the norm <img src="https://render.githubusercontent.com/render/math?math=(\frac{1}{2}C(\epsilon-\epsilon^*)^2%2B\frac{1}{2C}(\sigma-\sigma^*)^2 )^{\frac{1}{2}}">

In the spring bar case, the constraint set is a horizontal line as shown. However this method is prone to be misled by outliers. One example of such is shown below:

![alt text](parasolver_outlier.png)
