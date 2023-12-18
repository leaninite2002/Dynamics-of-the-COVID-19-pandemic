# Code based on https://matplotlib.org/stable/gallery/widgets/slider_demo.html

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp

N = 100 
gamma = 0.1
t = np.linspace(0, 200, 500)
t_max=200

def dSdt(S, I, beta):
    return -beta * S * I / N

def dIdt(S, I, beta):
    return beta * S * I / N - gamma * I

def dRdt(I):
    return gamma * I

def computeVariables(t, beta, I0, S0):
    sol=solve_ivp(fun=lambda t,x: [dSdt(x[0],x[1],beta),dIdt(x[0],x[1],beta),dRdt(x[1])],t_span=(0, t_max),y0=[S0,I0,N-S0-I0], t_eval=t, method='RK45')
    S,I,R=sol.y
    return S,I,R

init_beta = 0.25
init_I0 = 10
init_S0 = 90

fig, ax = plt.subplots(figsize=(12, 7))
line1, = ax.plot(t, computeVariables(t, init_beta, init_I0, init_S0)[0], lw=2, label='Susceptible')
line2, = ax.plot(t, computeVariables(t, init_beta, init_I0, init_S0)[1], lw=2, label='Infected')
line3, = ax.plot(t, computeVariables(t, init_beta, init_I0, init_S0)[2], lw=2, label='Recovered (or removed)')
ax.set_xlabel('Time [day]')
ax.set_ylabel('Percentage of the population')
ax.legend()
fig.suptitle("Dynamics of the SIR model",fontsize=15)
fig.subplots_adjust(left=0.25, bottom=0.25)

ax.set_ylim(0, 100)  

axBeta = fig.add_axes([0.25, 0.1, 0.65, 0.03])
beta_slider = Slider(
    ax=axBeta,
    label='Transmission rate $\\beta$',
    valmin=0,
    valmax=1,
    valinit=0.25,
)

axI0 = fig.add_axes([0.25, 0.05, 0.65, 0.03])
I0_slider = Slider(
    ax=axI0,
    label='Initial percentage of infected people',
    valmin=0,
    valmax=100,
    valinit=10,
)

axS0 = fig.add_axes([0.25, 0, 0.65, 0.03])
S0_slider = Slider(
    ax=axS0,
    label='Initial percentage of susceptible people',
    valmin=0,
    valmax=100,
    valinit=90,
)

def update(val):
    beta_val = beta_slider.val
    I0_val = I0_slider.val
    S0_val = S0_slider.val
    
    # Check if I0 + S0 exceeds 100
    if I0_val + S0_val > 100:
        total = I0_val + S0_val
        excess = total - 100
        if I0_val >= excess:
            I0_slider.set_val(I0_val - excess)
        else:
            I0_slider.set_val(0)
            S0_slider.set_val(S0_val - excess + I0_val)

    line1.set_ydata(computeVariables(t, beta_val, I0_slider.val, S0_slider.val)[0])
    line2.set_ydata(computeVariables(t, beta_val, I0_slider.val, S0_slider.val)[1])
    line3.set_ydata(computeVariables(t, beta_val, I0_slider.val, S0_slider.val)[2])

beta_slider.on_changed(update)
I0_slider.on_changed(update)
S0_slider.on_changed(update)
plt.show()
