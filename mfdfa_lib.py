#This module contains functions useful for performing MF-DFA analysis on 
#solar weather data as described in: https://academic.oup.com/mnras/article/519/3/3623/6881729?login=false
import numpy as np 

#####################################################################

#This function integrates the time series and creates the Y(i) function:
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

def variance(segSeries,polyCoeff,s,m,Ns,N):

	#This function calculates the variance as shown in 2.iii of the Gomes paper
	#
	# Here I am taking the 2Ns length from the paper and defining it as Ns
	varianceList=[]
	varianceElement=0
	Ns=len(segSeries)
	for v in range(Ns):
		varianceElement=0
		if v<= Ns:
			for i in range(s):
				segIndex=(v-1)*s+i
				print(segIndex)
				#varianceElement=(segSeries[(v-1)*s+i-1]-polyFunc(polyCoeff[v],m,i))**2
		v+=s
			#varianceList.append(varianceElement) 

	#return varianceList
"""
		elif v> Ns:
			for i in range(s):
				varianceElement=(segSeries[N-(v-Ns)*s+i]-polyFunc(polyCoeff[v],m,i))**2+varianceElement
			varianceList.append(varianceElement)
"""
