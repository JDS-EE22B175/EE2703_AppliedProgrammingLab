import numpy as np
import matplotlib.pyplot as plt
import sys

# Open the data file, read the data lines and close the file
fPointer = open(sys.argv[1], "r")
data = fPointer.readlines()
fPointer.close()
# Create empty lists to store the x and y data points
xp = []
yp = []

# Iterate over the data lines and split them into x and y values
for line in data:
    line = line.split()
    xp.append(float(line[0]))
    yp.append(float(line[1]))

# Create a matrix of the x data points with a column of ones appended
M = np.column_stack([xp, np.ones(len(xp))])

# Perform least squares fitting to find the slope and intercept of the line
(m, c), _, _, _ = np.linalg.lstsq(M, yp, rcond=None)

# Print the estimated equation of the line
print(f"The estimated equation is {m} t + {c}")

# Calculate the predicted y values for each x data point
y = [m * xp[i] + c for i in range(len(xp))]

# Calculate the residuals (i.e., the difference between the actual and predicted y values)
n = [yp[i] - y[i] for i in range(len(yp))]

# Plot the data points with error bars
plt.errorbar(xp[::25], yp[::25], np.std(n), fmt='ro')

# Plot the actual and predicted data lines
plt.plot(xp, yp)
plt.plot(xp, y, 'g')
plt.xlabel("X (Independent)")
plt.ylabel("Y (Dependent)")
# Save the plot to a file
plt.savefig("Dataset 1 Plot.png")

