#/usr/bin/env python
import pylab as pl
import numpy as np
from burgers import Utils, Settings

def main():

	# instantiate class
	utils    = Utils()
	settings = Settings('namelist.json')

	# input settings
	nx   = settings.nx
	mp   = int(nx/2)
	dx   = 2*np.pi/nx
	dt   = settings.dt
	nt   = settings.nt
	visc = settings.visc
	damp = settings.damp
	
	# initialize velocity field
	u = np.zeros(nx)

	# initialize random number generator
	np.random.seed(1)

	# place holder for right hand side
	rhsp = 0
 
	# advance in time
	for t in range(int(nt)):
		
		# compute derivatives
		derivs = utils.derivative(u,dx)
		du2dx  = derivs['du2dx']
		d2udx2 = derivs['d2udx2'] 

		# add fractional Brownian motion (FBM) noise
		f = utils.noise(0.75,nx)

		# compute right hand side
		rhs = visc * d2udx2 - 0.5*du2dx + np.sqrt(2*damp/dt)*f
		
		# advance in time
		if t == 0:
			# Euler
			u_new = u + dt*rhs
		else:
			# Adams-Bashforth 2nd
			u_new = u + dt*(1.5*rhs - 0.5*rhsp)
		
		fu_new     = np.fft.fft(u_new)
		fu_new[mp] = 0
		u_new      = np.real(np.fft.ifft(fu_new))
		u          = u_new
		rhsp       = rhs

		# output to screen every 100 time steps
		if ((t+1)%100==0):
			CFL = np.max(np.abs(u))*dt/dx          
			KE	= 0.5*np.var(u)
			print("%d \t %f \t %f \t %f \t %f \t %f"%(t+1,(t+1)*dt,KE,CFL,np.max(u),np.min(u)))

if __name__ == "__main__":
	main()