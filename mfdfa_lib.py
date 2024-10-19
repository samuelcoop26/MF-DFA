#This module contains functions useful for performing MF-DFA
import numpy as np 
import scipy as sci

#####################################################################
#This function performs the integration in
#https://academic.oup.com/mnras/article/519/3/3623/6881729?login=false 
#Section 2 "MF-DFA":
#ITS stands for "integrate time series"
def its(time_series,i,mean):
	Y=0
	for k in range(i):
		Y+=(time_series[k]-mean)
	return Y
#####################################################################
#This function creates a list of the integrated values of Y(i):
def int_series(time_series):
#	series=[]
#	average_b=mean=np.mean(time_series)
#	for i in range(0,len(time_series)):
#		series.append(its(time_series,i,average_b))
	tot_series=np.cumsum(time_series)
	avg_B=np.mean(time_series)
	integ_series=[]
	#Append the total integral minus the average of the segment:
	for i in range(len(tot_series)):
		integ_series.append(tot_series[i]-avg_B)
	return integ_series
#Now we need to divide the integrated series into N_s=int(N/s) segments of equal
#length s.
######################################################################
#This function separates integrated time series values into segments:
def int_segments(int_time_series,s):
	segmentlist=[]
	segment=[]
	counter=0
	for i in range(len(int_time_series)):
		if counter!=s:
			segment.append(int_time_series[i])
			counter+=1
		else:
			segmentlist.append(segment)
			counter=0
			segment=[]

	for segment in segmentlist:
		if len(segment)!=s:
			segmentlist.remove(segment)
	
	return segmentlist
#####################################################################
#Now we want to find the local trend of each section:
#For this we can fit a polynomial of degree m to the data:
def poly_fit(segments,m,s):
	i_list=range(s)
	polyList=[]
	for segment in segments:
		poly=np.polyfit(i_list,segment,deg=m)
		polyList.append(poly)		
	return polyList

def polyFunc(coeff,deg,i):
	polySum=0
	degree=deg
	for n in range(deg):
		polySum=polySum+coeff[n]*i**degree
		degree-=1
	return polySum	
######################################################################
#Calculate the variance for a given segment index, v and side length, s:
def variance(s,v,integ_series,poly_list, Ns):
	N=len(integ_series)
	var=0
	for i in range(1,s):
		polyFit=polyFunc(poly_list,3,i)
		var=var + (integseries[N-(v-1)*s+i]-polyFit)^2
	return (1/s)*var

