import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the function to calculate the blackbody radiance at a given frequency and temperature using the estimated values of the constants
def planck(f, hEst, cEst, kBEst, TEst):
  return (2*hEst*(f**3))/((cEst**2)*(np.exp((hEst*f)/(kBEst*TEst)) - 1))


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


# Define the starting values for the curve fitting algorithm
startingTemp = 4930
startingH = 6.62e-34
startingkB = 1.4e-23
startingC = 2.99e8
startingPoints = [startingH, startingC, startingkB, startingTemp]

# Perform the curve fitting
(hEstimate, cEstimate, kBEstimate, TEstimate), pcov = curve_fit(planck, frequencies, radiances, startingPoints)

# Print the estimated values
print(f'The estimated values are h = {hEstimate}, c = {cEstimate}, kB = {kBEstimate}, T = {TEstimate}')

# Calculate the estimated radiances using the best fit parameters
estimatedradiances = [planck(frequency, hEstimate, cEstimate, kBEstimate, TEstimate) for frequency in frequencies]

# Plot the actual and estimated radiance data
plt.plot(frequencies, radiances, 'b', label = "Noisy Data")
plt.plot(frequencies, estimatedradiances, 'r', label = "Estimated")
plt.legend()
# Set the plot labels
plt.xlabel("Frequencies")
plt.ylabel("Radiance")

# Save the plot to a file
plt.savefig("Dataset 3_2 Plot.png")