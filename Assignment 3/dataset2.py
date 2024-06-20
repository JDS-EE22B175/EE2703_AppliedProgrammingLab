import numpy as np
import matplotlib.pyplot as plt
import math
import sys
from scipy.optimize import curve_fit

# Open the data file and read the data lines
fPointer = open(sys.argv[1], "r")
data = fPointer.readlines()
fPointer.close()

# Create empty lists to store the X and Y data points
X = []
Y = []

# Iterate over the data lines and split them into X and Y values
for line in data:
    line = line.split()
    X.append(float(line[0]))
    Y.append(float(line[1]))

# Calculate the period of the data
period = 0
spacing = X[1] - X[0]
difference = 1
for i in range(0, len(Y)):
    for j in range(i + 1, len(Y)):
        if (math.fabs(Y[i] - Y[j]) < difference and (j - i) > 100):
            difference = math.fabs(Y[i] - Y[j])
            period = j - i
period = period * spacing

# Calculate the angular frequency of the data
omega = 2 * math.pi / period

# Print the angular frequency
print(omega)

# Create a list of sine values for the first three harmonics of the data
sineValuesNew = []
for i in (1, 3, 5):
    omegai = omega * i
    sineValuesNew.append([math.sin(omegai * x) for x in X])

# Create a matrix of the sine values for the first three harmonics of the data
M = np.column_stack([sineValue for sineValue in sineValuesNew])

# Calculate the least squares coefficients for the first three harmonics of the data
(a, b, c), _, _, _ = np.linalg.lstsq(M, Y, rcond=None)
# Print the estimated equation
print(f"The estimated equation using least squares is {a} Sin{omega}x + {b} Sin{omega * 3}x + {c} Sin{omega * 5}x")

# Define a function to calculate the least squares fit of the data
def equation(x):
    return (a * math.sin(omega * x) + b * math.sin(omega * 3 * x) + c * math.sin(omega * 5 * x))

# Calculate the predicted Y values using the least squares fit
yPredNew = [equation(x) for x in X]

# Plot the actual and predicted Y values
plt.plot(X, Y, 'b')
plt.plot(X, yPredNew, 'r')
plt.savefig("Dataset 2 Least Square plot.png")

# Define a function to calculate the curve fit of the data
def equationUnkown(x, a, b, c):
    return (a * np.sin(2.3884711270442605 * x)) + (b * np.sin(2.3884711270442605 * 3 * x)) + (c * np.sin(2.3884711270442605 * 5 * x))

# Perform the curve fit
(aEst, bEst, cEst), pcov = curve_fit(equationUnkown, X, Y)

# Print the estimated equation
print(f"The estimated equation using curve_fit is {a} Sin{omega}x + {b} Sin{omega * 3}x + {c} Sin{omega * 5}x")

# Calculate the predicted Y values using the curve fit
yPredNew = [equationUnkown(x, aEst, bEst, cEst) for x in X]

# Plot the actual and predicted Y values
plt.plot(X, Y, 'b')
plt.plot(X, yPredNew, 'r')
plt.savefig("Dataset 2 Curve Fit Plot.png")