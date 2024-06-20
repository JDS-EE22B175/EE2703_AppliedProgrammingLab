The python modules `matplotlib.pyplot, numpy, scipy, math and sys` must be available on the device to run these 4 programs.

# **To run the script:**

1. Open a terminal window and navigate to the directory where the script is saved.
2. Run the script using the following command:

```
python <python_file> <data_file>
```
where,
`<data_file>` is the path to the data file,
`<python_file>` is the name of the python script to be run.

# `dataset_1.py`

This Python script performs least squares fitting to a linear model. The script reads the data from a file, performs the least squares fitting, and plots the data points with error bars and the actual and predicted data lines.

**Restrictions on the Data File**

The data file must contain two columns of values, the first representing the values of the independent variable and the second the dependent variable. The relation between the two must be linear, only then will the code give desired outputs.

# `dataset_2.py`

This Python script performs least squares fitting to a sinusoidal model. The script reads the data from a file, performs the least squares fitting, and plots the actual and predicted data lines.

**Restrictions on the Data File**

The data file must contain two columns of values, the first representing the values of the independent variable and the second the dependent variable. The independent variable must be the argument of given to 3 sinusoids of frequencies f, 3f and 5f and the dependent variable must be a linear combination of the three sinusoids only then will the code give desired outputs.

# `dataset_3_1.py and dataset_3_2.py`

This Python script performs least squares fitting to planck's blackbody radiation equation. The script reads the data from a file, performs the least squares fitting, and plots the actual and predicted data lines.

**Restrictions on the Data File**

The data file must contain two columns of values, the first representing the values of the frequencies $f$ and the second the blackbody radiances $B$ . The relation between the two must be based on planck's blackbody radiation equation, which is 
$$B(f, T) = \frac{2hf^3}{c^2} \frac{1}{e^{\frac{hf}{k_BT}} - 1}$$.