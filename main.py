#This script loads data from MMS1_FGM using pyspedas
import pyspedas
import numpy as np
import mfdfa_lib as mfdfa 
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
	print(times)

	print("Calculating the cumulative sum...")	
	#Obtain a list of integrated time series values and save to csv:
	#Also obtain the reverse list to segment the list backwards for 2N entries
	int_series=mfdfa.int_series(bmag)
	reverse_int_series = list(reversed(int_series))

#	np.savetxt('data/Yfunc_values.csv',(np.array(int_series)),delimiter=',')
	print("Done integrating...")
		
	print("Segmenting...")
	#Segment the integrated series:
	s=4
	seg_series=mfdfa.int_segments(int_series,s)

	#Now reverse the series to include points that are left out of the last
	#paritition of the integrated time series:
	#This gives us 2N_s total points to apply a polynomial fit.
	reverse_seg_series=mfdfa.int_segments(reverse_int_series,s)

	#Concatenate the entire list of both the reversed segments and the
	#non-reversed segments:
	segment_list = seg_series + reverse_seg_series
	print("Constructing polynomial fits...")
	#fit the series to a n degree plynomial:
	n=3
	#this function returns the coefficients of the polynomial:
	fitList=mfdfa.poly_fit(segment_list,n,s)
	print(f"Polynomial fits: {fitList}")
	#Now we construct the polynomial values for a given value i	
	#WIP
	print("Finished!")

main()
