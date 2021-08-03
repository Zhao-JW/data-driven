import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from gaussian_process_util import plot_gp

from skopt.plots import plot_gaussian_process
from skopt import gp_minimize


#the assumed linear material relationship with additive gaussian noise
def f(stress, noise_level = 3, k=20):
    noise = noise_level * np.random.normal()
    strain_law = k*stress[0]
    #strain_law = k*stress**4.1 + 5*stress
    strain_noise = strain_law + noise
    return strain_noise

#the assumed ideal material relationship without noise
def f_wo_noise(stress):
    return f(stress,0)

#initial random samples
x = np.sort(3*np.random.rand(30)).reshape(-1,1)
noise_level = 3
y_sample = [f(stress,noise_level) for stress in x]
y_ideal = [f(stress,0) for stress in x]


#fitting the result to a Gaussian process, not much use in the linear material model but might be useful in the future
kernel = ConstantKernel(1.0) * RBF(length_scale=1.0)
gp = GaussianProcessRegressor(kernel=kernel, alpha=noise_level**2, # if the noise level not know this can be left blank
                              n_restarts_optimizer=10)

gp.fit(x,y_sample)
mu_s,cov_s = gp.predict(x, return_cov=True)

#plot the Gaussian process
fig = plt.figure()
ax = fig.add_subplot(111)
plot_gp(mu_s, cov_s, x,X_train = x, Y_train = y_sample)

#plot the ideal material realtionship and sample points
ax.plot(x, y_ideal,c = 'gray',label = 'ideal material relationship')
ax.set_xlabel('stress')
ax.set_ylabel('strain')

#the ideal constraint set, from strain = F/A on y axis to stress = x0, on x axis， given a Force F at the end and total displacement x0
sigma0 = 50
x0 = 2
x_constraint = np.linspace(0,3,10)
y_constraint = sigma0 - x_constraint*(sigma0/x0)
ax.plot(x_constraint, y_constraint, label = 'constraint set')

ax.set_ylim([0, 60])
ax.set_xlim([0,3])
plt.legend()
plt.show()
