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
		#Construct the Y(i) function
		Y+=(time_series[k]-mean)
	return Y

#####################################################################

#This function creates a list of the integrated values of Y(i):
def int_series(time_series):
#	series=[]
#	average_b=mean=np.mean(time_series)
#	for i in range(0,len(time_series)):
#		series.append(its(time_series,i,average_b))

	#Evaluate the cumulative sum:
	tot_series=np.cumsum(time_series)
	#Find the average B field value at this point:
	avg_B=np.mean(time_series)
	#Initialize the integrated list:
	integ_series=[]
	#Append the total integral minus the average of the segment:
	for i in range(len(tot_series)):
		integ_series.append(tot_series[i]-avg_B)
	return integ_series
#Now we need to divide the integrated series into N_s=int(N/s) segments of equal
#length s.

######################################################################

#This function separates integrated time series values into segments:
#Each segment is size s
def int_segments(int_time_series,s):
	#initialize the lists of segments:
	segmentlist=[]
	segment=[]
	counter=0
	#Run through the integrated time list and append each portion of size
	#s to a large list of segments
	for i in range(len(int_time_series)):
		#If the counter is not the size of the full segment, continue
		#If the counter reaches s, then add that segment to the list 
		#of segments
		if counter!=s:
			segment.append(int_time_series[i])
			counter+=1
		else:
			segmentlist.append(segment)
			counter=0
			segment=[]
	#Remove any segments that are smaller than s (this occurs at the end of
	#the list since the list is not necessarily divisible by s.
	#The full segment list size becomes N_s=int(N/s) where N is the size 
	#of the integrated list.
	for segment in segmentlist:
		if len(segment)!=s:
			segmentlist.remove(segment)
	
	return segmentlist

#####################################################################

#Now we want to find the local trend of each section:
#For this we can fit a polynomial of degree m to the data:
def poly_fit(segments,m,s):
	#Here, for each segment we fit a polynomial to the data
	#The i values represent time as an index of data points
	i_list=range(s)
	polyList=[]
	for segment in segments:
		#use the numpy polyfit function to fit with a polynomial
		#The numpy polyfit function returns a set of coefficients
		#in the form a_m x^m + a_{m-1} x^{m - 1} +..+ a_1 x+ a_0.
		poly=np.polyfit(i_list,segment,deg=m)
		polyList.append(poly)		
	return polyList

#This function evaluates the output of the polynomial function for the 
#given set of coefficients:
def polyFunc(coeff,deg,i):
	polySum=0
	degree=deg
	#Run through each degree and sum up the polynomial terms:
	for n in range(deg):
		polySum=polySum+coeff[n]*i**degree
		degree-=1
	#Return the sum of the polynomial terms:
	return polySum	

######################################################################

#Calculate the variance for a given segment index, v and side length, s:

def variance(s,v,integ_series,poly_list, Ns):
	N=len(integ_series)
	var=0
	#For each element in the segment, find the polynomial fit,
	#then calculate the variance from the Gomes article, in the MF-DFA
	#section, part 3.
	for i in range(1,s):
		#Extract the value of the polynomial
		polyFit=polyFunc(poly_list,3,i)
		#Calculate the variance:
		var=var + (integseries[N-(v-1)*s+i]-polyFit)^2
	return (1/s)*var

