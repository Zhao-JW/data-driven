import numpy as np
import matplotlib.pyplot as plt
from skopt.plots import plot_gaussian_process
from skopt import gp_minimize


noise_level = 0.1

def f(x, noise_level=0.1): 
    noise = np.random.normal(loc = 0.0, scale = noise_level)  #another way to generate normal noise
    y_noise = np.sin(5 * x[0]) * (1 - np.tanh(x[0] ** 2)) + noise
    return y_noise

def f_wo_noise(x):
    return f(x, noise_level=0)

res = gp_minimize(f,                  # the function to minimize
                  [(-2.0,2.0)],      # the bounds on each dimension of x
                  acq_func="EI",      # the acquisition function
                  n_calls=25,         # the number of evaluations of f
                  n_random_starts=5,  # the number of random initialization points
                  noise=noise_level**2,       # the noise level (optional)
                  xi = 0.001)         #the exploration-exploitation variable, larger values results in more exploration of the function

res2 = gp_minimize(f,                  # the function to minimize
                  [(-2.0,2.0)],      # the bounds on each dimension of x
                  acq_func="EI",      # the acquisition function
                  n_calls=25,         # the number of evaluations of f
                  n_random_starts=5,  # the number of random initialization points
                  noise=noise_level**2,       # the noise level (optional)
                  xi = 0.1)   

res3 = gp_minimize(f,                  # the function to minimize
                  [(-2.0,2.0)],      # the bounds on each dimension of x
                  acq_func="EI",      # the acquisition function
                  n_calls=25,         # the number of evaluations of f
                  n_random_starts=5,  # the number of random initialization points
                  noise=1**2,       # the noise level (optional)
                  xi = 0.1)   


n_iter = 20
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1 = plot_gaussian_process(res, n_calls=5,
                            objective=f_wo_noise,
                            #noise_level=noise_level,
                            show_legend=True, show_title=False,
                            show_next_point=False, show_acq_func=False)
ax1.title.set_text('iteration 5,xi = 0.001,noise level 0.1')
ax2 = fig.add_subplot(222)
ax2 = plot_gaussian_process(res2, n_calls=n_iter,
                            objective=f_wo_noise,
                            #noise_level=noise_level,
                            show_legend=True, show_title=False,
                            show_next_point=False, show_acq_func=False)
ax2.title.set_text('iteration 20,xi = 0.1,noise level 0.1')

ax3 = fig.add_subplot(223)
ax3 = plot_gaussian_process(res, n_calls=n_iter,
                            objective=f_wo_noise,
                            #noise_level=noise_level,
                            show_legend=True, show_title=False,
                            show_next_point=False, show_acq_func=False)
ax3.title.set_text('iteration 20,xi = 0.001,noise level 0.1')

ax4 = fig.add_subplot(224)
ax4 = plot_gaussian_process(res3, n_calls=n_iter,
                            objective=f_wo_noise,
                            #noise_level=noise_level,
                            show_legend=True, show_title=False,
                            show_next_point=False, show_acq_func=False)
ax4.title.set_text('iteration 20,xi = 0.001,noise level 1')

plt.tight_layout()
plt.show()