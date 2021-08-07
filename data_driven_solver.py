import matplotlib.pyplot as plt
import numpy as np


#the assumed linear material relationship with additive gaussian noise
def f(stress, noise_level = 3, k=20):
    noise = noise_level * np.random.normal()
    #strain_law = k*stress[0] #linear
    #strain_law = 50 - 49/(1 + (stress[0]/1.5)** 7) #sigmoid shape
    strain_law = 3 + 36*stress[0] - 6*stress[0]**2 #parabolic shape
    strain_noise = strain_law + noise
    return strain_noise

def nearest(strain, stress, E):
    mindist = 0.5 * C * (E[0][-1] - strain)**2 + 0.5 * (E[1][-1] - stress)**2/C
    index = -1
    for i in range(np.size(y_sample)-1):
        dist = 0.5 * C * (E[0][i] - strain)**2 + 0.5 * (E[1][i] - stress)**2/C
        if dist < mindist :
            index = i
            mindist = dist
    return index


#initial random samples
x = np.sort(3*np.random.rand(30)).reshape(-1,1)
noise_level = 6
y_sample = np.array([f(stress,noise_level) for stress in x])
y_ideal = np.array([f(stress,0) for stress in x])
E = np.stack((x.reshape(-1), y_sample))


#set some constants
L0 = 1
A = 1
C = 1
f = 30
k_spring = 20

#initalize with a randomly selected point from sample dataset
k = 0
inital = np.random.randint(np.size(y_sample),size = (1))
strain0 = E[0][inital]
stress0 = E[1][inital]
stress_k = stress0
strain_k = strain0
stress_k1 = 0
strain_k1 = 0
flag = True

#in the simple bar spring case no iteration is needed at all, the algorithm can find the nearest in one go easily
while (flag and k<5):
    #find corresponding phase point satisfying constraint set through u and eta
    u_k = strain_k * L0 + f/k_spring
    eta_k = 1/C *(f/A - stress_k)

    strain_k_constraint = 1/L0 * (u_k - f/k_spring)
    stress_k_constraint = stress_k + C* 1/L0 * eta_k

    #locate state assignment
    index = nearest(strain_k_constraint,stress_k_constraint,E)
    strain_k1 = E[0][index]
    stress_k1 = E[1][index]

    if ([strain_k,stress_k] != [strain_k1,stress_k1]):
        flag = True
        strain_k = strain_k1
        stress_k = stress_k1
        print('k = ',k,strain_k,stress_k)
        print('k+1: ',strain_k1,stress_k1)
    else:
        flag = False
    k +=1
    

fig = plt.figure()
ax = fig.add_subplot(111)
#plot the ideal material realtionship and sample points
ax.plot(x, y_ideal,c = 'gray',label = 'ideal material relationship')
ax.scatter(x,y_sample,c = 'green',label = 'material sample')
ax.scatter(strain_k1,stress_k1,c = 'red')
ax.set_xlabel('strain')
ax.set_ylabel('stress')

#the ideal constraint set, from stress = k*x0 on y axis to strain = x0, on x axis， given a spring constant k_spring and force f
k_spring = 20

x_constraint = np.linspace(0,3,10)
#y_constraint = k*u0 - x_constraint*k
y_constraint = f/A* np.ones(10)
ax.plot(x_constraint, y_constraint, label = 'constraint set')

ax.set_ylim([0, 60])
ax.set_xlim([0,3.2])
plt.legend()
plt.show()
