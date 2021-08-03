import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from gaussian_process_util import plot_gp

from skopt.plots import plot_gaussian_process
from skopt import gp_minimize


def f(stress, noise_level = 3, k=20):
    noise = noise_level * np.random.normal()
    strain_law = k*stress[0]
    #strain_law = k*stress**4.1 + 5*stress
    strain_noise = strain_law + noise
    return strain_noise

def f_wo_noise(stress):
    return f(stress,0)

#initial samples
x = np.sort(3*np.random.rand(30)).reshape(-1,1)

noise_level = 3
y_sample = [f(stress,noise_level) for stress in x]
y_ideal = [f(stress,0) for stress in x]

'''
kernel = ConstantKernel(1.0) * RBF(length_scale=1.0)
gp = GaussianProcessRegressor(kernel=kernel, alpha=noise**2,
                              n_restarts_optimizer=10)

gp.fit(x,y_noise)
mu_s,cov_s = gp.predict(x, return_cov=True)

fig = plt.figure()
plot_gp(mu_s, cov_s, x,X_train = x, Y_train = y_noise)
plt.xlabel('stress')
plt.ylabel('strain')
'''

#x0, y0 input needs to be a list of lists
x = [[stress[0]] for stress in x]

res = gp_minimize(f,                  # the function to minimize
                  [(0,3.0)],      # the bounds on each dimension of x
                  acq_func="EI",      # the acquisition function
                  n_calls=0,         # the number of evaluations of f
                  n_random_starts=0,  # the number of random initialization points
                  noise=noise_level**2,       # the noise level (optional)
                  x0 = x,
                  y0 = y_sample,
                  xi = 100)


fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(x, y_ideal,c = 'gray',label = 'ideal material relationship')
ax.scatter(x, y_sample, c = 'r', label = 'sample datapoint ')
ax.set_xlabel('stress')
ax.set_ylabel('strain')

#the constraint set, from strain = F/A on y axis to stress = x0, on x axis， given a Force F at the end and total displacement x0
sigma0 = 50
x0 = 2
x_constraint = np.linspace(0,3,10)
y_constraint = sigma0 - x_constraint*(sigma0/x0)
ax.plot(x_constraint, y_constraint, label = 'constraint set')

'''
#plot the gaussian expectation, not very well in the linear case
ax = plot_gaussian_process(res, n_calls=0,
                            objective=f_wo_noise,
                            #noise_level=noise_level,
                            show_legend=False, show_title=False,
                            show_next_point=False, show_acq_func=False,show_mu = False)
'''

ax.set_ylim([0, 60])
ax.set_xlim([0,3])
plt.legend()
plt.show()

#plt.show()