from MFDFA import MFDFA
import pyspedas
import matplotlib.pyplot as plt
import numpy as np
from pyspedas import tplot


def main():
	#Gather data and plot it:
	pyspedas.mms.fgm(time_clip=True,probe=1,trange=["2024-03-10","2024-03-11"])
		#t_plot=tplot(['mms1_fgm_b_gse_srvy_l2_btot', 'mms1_fgm_b_gse_srvy_l2_bvec'])

	#Get data to be put in array format:
	magdata=pyspedas.get_data("mms1_fgm_b_gse_srvy_l2_btot")
	#extract time and B-field magnitudes:
	times=magdata.times
	bmag=magdata.y
	print("loaded data!")

	

	# Select a band of lags, which usually ranges from
	# very small segments of data, to very long ones, as
	lag = np.unique(np.logspace(0.5, 3, 100, dtype=int))
	#DO THIS INSTEAD: np.power(2,range(10),dtype=int) 
	#[2**i for i in range(10)]

	# Notice these must be ints, since these will segment
	# the data into chucks of lag size

	# Select the power q
	q = 2


	# The order of the polynomial fitting
	#PLay around with this: see how much it will change the data
	order = 3

	# Obtain the (MF)DFA as
	lag, dfa = MFDFA(bmag, lag = lag, q = q, order = order)

# And now we need to fit the line to find the slope
	# in a double logaritmic scales, i.e., you need to
	# fit the logs of the results
	H_hat = np.polyfit(np.log(lag)[4:20],np.log(dfa[4:20]),1)[0]

	#Plots the fluctuation function:	
	fluctuation_func(bmag,lag,q,order)
	print('Estimated H = '+'{:.3f}'.format(H_hat[0]))
	# Now what you should obtain is: slope = H + 1

	qlist=np.arange(-20,20,3).tolist()
	print(qlist)
	renyi_exponents(bmag, lag, qlist, order)	
	
#Now we generate the Renyi exponents:
def renyi_exponents(bmag,lag,qlist,order):

	#hlist=np.zeros([len(qlist),2])
	#For qidx, q in enumerate(qlist)
	#hlist[qidx,:] = q,H_hat

	#This is the list where the Hurst exponents will live:
	hlist=[]
	#Perform MFDFA for each value of q, find h(q), append to hlist:	
	
	#combine loops:
	for q in qlist:
		lag,dfa=MFDFA(bmag,lag=lag,q=q,order=order)
		H_hat = np.polyfit(np.log(lag)[4:20],np.log(dfa[4:20]),1)[0]
		hlist.append([q,H_hat])#take q out of here
		print(q)

	#This is the list where the Renyi exponents will live:
	renyilist=[]
	
	#For each h(q), find the Renyi exponent, append to renyilist:
	for h in hlist:
		#This is the relation of the Renyi exponent to the Hurst exponent:
		tau=h[0]*h[1]-1
		renyilist.append(tau)

	#plt.plot(*hlist)

	plt.plot(qlist,renyilist)
	plt.xlabel('$q$')
	plt.ylabel(r'$\tau(q)$')
	plt.xlim(-20,20)
	plt.ylim(-40,40)
	plt.show()
	
	

def fluctuation_func(bmag,lag,q,order):

	lag,dfa = MFDFA(bmag,lag=lag,q=q,order=order)
	# To uncover the Hurst index, lets get some log-log plots
	plt.loglog(lag, dfa, 'o', label='fOU: MFDFA q=2')
	plt.xlabel('s')
	plt.ylabel(r'F_q(s)')
	plt.title('q-th Order Fluctuation Function for MMS data')
	plt.show()
	
	return lag,dfa[1]


main()
			
