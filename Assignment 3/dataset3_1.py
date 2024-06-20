import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Open the data file and read the data lines
fPointer = open(sys.argv[1], "r")
data = fPointer.readlines()
fPointer.close()

# Create empty lists to store the frequency and radiance data points
frequencies = []
radiances = []

# Iterate over the data lines and split them into frequency and radiance values
for line in data:
    line = line.split()
    frequencies.append(float(line[0]))
    radiances.append(float(line[1]))

# Define the constants used in the blackbody radiation formula
h = 6.626e-34
c = 299792458
kB = 1.380649e-23

# Define the function to calculate the blackbody radiance at a given frequency and temperature
def planck(f, T):
    b = (2*h*(f**3)/(c**2))/(np.exp((h*f)/(kB*T)) - 1)
    return b

# Generate a list of starting points for the curve fitting algorithm
starting_points = np.linspace(1000, 10000, 10)

# Initialize the best fit parameters
best_fit = None

# Iterate over the starting points and find the best fit parameters
for T in starting_points:
    try:
        # Perform the curve fitting
        popt, pcov = curve_fit(planck, frequencies, radiances, p0=[T])

        # If the current fit is better than the best fit so far, update the best fit parameters
        if best_fit is None or pcov[0][0] < best_fit[1][0][0]:
            best_fit = (popt, pcov)

    except RuntimeError:
        pass

# Print the estimated temperature
print(f'The Temperature estimated is {popt[0]}K')

# Calculate the predicted radiance at each frequency using the best fit parameters
zy = [planck(frequency, popt[0]) for frequency in frequencies]

# Plot the actual and predicted radiance data
plt.plot(frequencies, radiances, 'b', label = "Noisy Data")
plt.plot(frequencies, zy, 'r', label = "Estimated")
plt.legend()
# Set the plot labels
plt.xlabel("Frequencies")
plt.ylabel("Radiance")

# Save the plot to a file
plt.savefig("Dataset 3_1 Plot.png")