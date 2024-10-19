This is a library that performs MF-DFA analysis on solar weather data, as
described in
https://academic.oup.com/mnras/article/519/3/3623/6881729?login=false.


**Prerequisites**
Python 3 or higher must be installed.
The following Python libraries must be installed: numpy, and pyspedas


**How to run with MMS1 FGM data:**
This library currently contains a function to run an MF-DFA analysis
on MMS1 FGM data. This is the main function used to perform the entire
analysis. This can be run as such:

```BASH
python3 main.py
```

**List of functions**
Here is a list of functions that perform the MF-DFA analysis.
These are contained in the file called *mfdfa_lib.py* in the source folder.


***mfdfa_lib.int_series()***

This function returns the integrated time series of an input time series.


***mfdfa_lib.poly_fit()***
This function returns the polynomial fit of an integrated time series segment.
The function returns the coefficients of the polynomial fit.

***mfdfa_lib.polyFunc()***
This function evaluates the value of the polynomial from a set of fit
coefficients.

***mfdfa_lib.variance()***
This function evaluates the variance of a given segment.
