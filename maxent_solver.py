import matplotlib.pyplot as plt
import numpy as np


#the assumed linear material relationship with additive gaussian noise
def f(stress, noise_level = 3):
    noise = noise_level * np.random.normal()
    #strain_law = k*stress[0] #linear
    #strain_law = 50 - 49/(1 + (stress[0]/1.5)** 7) #sigmoid shape
    strain_law = 3 + 36*stress[0] - 6*stress[0]**2 #parabolic shape
    strain_noise = strain_law + noise
    return strain_noise

def norm(z):
    [epsilon, sigma] = z
    norm =  (0.5 * C * (epsilon)**2 + 0.5/C * (sigma)**2)**0.5
    return norm

def nearest(epsilon, sigma, E):
    mindist = norm(E[:,-1]-[epsilon, sigma])
    index = -1
    for i in range(np.size(y_sample)-1):
        dist = norm(E[:,i]-[epsilon, sigma])
        if dist < mindist :
            index = i
            mindist = dist
    return index

def maxent_iteration(E,n,beta_k,z_k,):
    #calculate p_k
    c_k1 = np.array([ np.exp(-beta_k*norm(z_k-E[:,i])**2) for i in range(n)]) #shape: length n array
    Z_k1 = np.sum(c_k1) #a scalar
    p_k1 = np.array([ c_k1[i]/Z_k1 for i in range(n)])    #shape: length n array

    #break if Z_k is nan
    if (p_k1!=p_k1).any():
        p_k1 = p_k_previous
        return 0

    z_k1_bar = np.sum(np.array([p_k1[i]*E[:,i] for i in range(n)]),axis = 0)   # a vector

    #calculate u_k1, eta_k1, beta_k1
    u_k1 = L0 * z_k1_bar[0] + f/k_spring
    eta_k1 = 1/C *(f/A - z_k1_bar[1])
    beta_k1_tilda = ( np.sum( np.array([ p_k1[i]*norm(E[:,i]-z_k1_bar)**2 for i in range(n)]) ) )**(-1)
    beta_k1 = beta_k1_tilda * anneal_rate + (1-anneal_rate) * beta_k

    epsilon_k1 = 1/L0 * (u_k1 - f/k_spring)
    sigma_k1 = z_k1_bar[1] + eta_k1 * C/L0
    z_k1 = np.array([epsilon_k1,sigma_k1])

    return [z_k1,z_k1_bar,beta_k1,p_k1]

def  result_plot(ax,ax2,ax3):
    #plot the ideal material realtionship and sample points
    ax.plot(x, y_ideal,c = 'gray',label = 'ideal material relationship')
    ax.scatter(x,y_sample,c = 'green',label = 'material sample')
    ax.scatter(z_result[0],z_result[1],c = 'red')
    ax.set_xlabel('strain')
    ax.set_ylabel('stress')

    #the ideal constraint set, from stress = k*x0 on y axis to strain = x0, on x axis， given a spring constant k_spring and force f
    k_spring = 20

    x_constraint = np.linspace(0,3,10)
    y_constraint = f/A* np.ones(10)
    ax.plot(x_constraint, y_constraint, label = 'constraint set')

    ax.set_ylim([-5, 65])
    ax.set_xlim([-0.2,3.2])
    ax.legend()

    legend2 = 'step taken: '+str(len(beta))
    ax2.plot(np.linspace(1,len(beta),len(beta)),beta,label = legend2)
    ax2.set_xlim([0,len(beta)])
    #ax2.set_ylim([0,5])
    ax2.set_xlabel('step')
    ax2.set_ylabel('beta')
    ax2.legend()

    ax3.plot(np.linspace(1,len(zbar),len(zbar)),zbar)
    ax3.set_xlim([0,len(zbar)])
    ax3.set_xlabel('step')
    ax3.set_ylabel('zbar')
    plt.tight_layout()
    return fig


def plot_evolution(E,y_ideal,p_log,zbar_log):
    fig = plt.figure()
    m = np.shape(p_log)[0]
    step = [1,5,10,100,500,1000,2000,5000]
    step = step[:m-1]+[len(beta)]
    for i in range(m):
        
        ax1 = fig.add_subplot((m+1)//2, 2, i+1)

        p_yellow = probabilitycheck(p_log[i],0.01) #return the value of desired data points
        p_orange = probabilitycheck(p_log[i], 0.1)
        ax1.plot(E[0,:], y_ideal,c = 'gray',label = 'ideal material relationship')
        ax1.scatter(E[0,:], E[1,:],c = 'green',label = 'material sample')
        ax1.scatter(p_yellow[:,0],p_yellow[:,1],c = 'yellow')
        ax1.scatter(p_orange[:,0],p_orange[:,1],c = 'orange')
        ax1.scatter(zbar_log[i,0],zbar_log[i,1],c = 'red')
        ax1.title.set_text('step = '+str(step[i]))
        ax1.plot(np.linspace(0,3,10), f/A* np.ones(10), label = 'constraint set')
    plt.tight_layout()
    return 0

def probabilitycheck(p_log,threshold):
    Plarge = np.empty([0,2])
    for i in range(n):
        if p_log[i]>threshold:
            Plarge = np.append(Plarge,np.array([E[:,i]]),axis = 0)
    return Plarge


#initialize random samples
n = 50
x = np.sort(3*np.random.rand(n)).reshape(-1,1)
noise_level = 3
y_sample = np.array([f(stress,noise_level) for stress in x])
y_ideal = np.array([f(stress,0) for stress in x])
E = np.stack((x.reshape(-1), y_sample))

#set some constants
L0 = 1
A = 1
C = 1
f = 30
k_spring = 30
anneal_rate = 0.1

# (I): simulated annealing
#initialize z, z_bar, beta
z_k_bar = 1/n * np.sum(E,axis = 1)
z_k = z_k_bar
z_k1 = z_k
beta_k1 = 1/(1/n * sum([norm(E[:,i]-z_k_bar)**2 for i in range(n)]))

#iteration step
k = 0
flag = True
beta = np.array([])
zbar = np.array([])
p_k_previous = np.array([])
p_log = np.empty([0,n])
zbar_log = np.empty([0,2])

while (flag and k<5000):
    
    k1result = maxent_iteration(E,n,beta_k1,z_k1)
    if k1result != 0:
        [z_k1,z_k1_bar,beta_k1,p_k1] = k1result
    else:
        break

    beta = np.append(beta,beta_k1)
    zbar = np.append(zbar,z_k1_bar[1])

    #test for convergence
    if (z_k==z_k1).all():
        flag = False
    else:
        z_k = z_k1
        k += 1
    if ( np.array([k]*8) ==np.array([1,5,10,100,500,1000,2000,5000])).any():
        p_log = np.append(p_log,[p_k1],axis=0)
        zbar_log = np.append(zbar_log,[z_k1_bar],axis = 0)

p_log = np.append(p_log,[p_k1],axis=0)
zbar_log = np.append(zbar_log,[z_k1_bar],axis = 0)
z_result = E[:,nearest(z_k1[0],z_k1[1],E)]

# (III): result demonstration
fig = plt.figure()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)
fig = result_plot(ax,ax2,ax3)
plt.show()

plot_evolution(E,y_ideal,p_log,zbar_log)
plt.show()
