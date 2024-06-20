# The following imports are assumed for the rest of the problems
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from matplotlib.animation import PillowWriter

def gradDescent(startingX, learningRate, func, xDerivative, xLims, stepCount, problemName, leeway = 3, startingY = None, yDerivative = None, yLims = None, numberOfPoints = 300, azimuth = -80):
    """
    Perform gradient descent to find the local minimum of a function.

    Args:
        startingX (float): Initial X value.
        learningRate (float): Learning rate for gradient descent.
        func (function): The function to minimize.
        xDerivative (function): The derivative of the function with respect to X.
        xLims (list): A list containing the lower and upper limits for X.
        stepCount (int): Number of gradient descent steps.
        problemName (str): Name of the problem, used for saving the animation.
        leeway (int): Adjust the plotting limits by this amount.
        startingY (float, optional): Initial Y value for 2D problems.
        yDerivative (function, optional): Derivative of the function with respect to Y for 2D problems.
        yLims (list, optional): A list containing the lower and upper limits for Y for 2D problems.
        numberOfPoints (int): Number of points for plotting.
        azimuth (float): Azimuth angle for 3D plots.

    Returns:
        tuple: The local minimum coordinates, either (X, Y) for 2D or (X, Y, Z) for 3D problems.
    """

    # Define metadata for the animation
    metadata = dict(title='Assignment5 GIFs', artist='EE22B175')
    # Assign the 'problemName' to 'problem' (Note: The initial assignment of 'problemName' is not needed)
    problem = problemName
    # Create a PillowWriter object for saving the animation
    # Set the frames per second (fps) and metadata for the animation
    problem = PillowWriter(fps=2, metadata=metadata)

    # For One Independent Variable Problems
    if(startingY == None):
        # Generate a linear space of X values with some leeway
        xbase = np.linspace(xLims[0] - leeway, xLims[1] + leeway, numberOfPoints)
        # Evaluate the function at the X values to obtain Y values
        ybase = func(xbase)

        # Create a new figure and axis for plotting
        fig, ax = plt.subplots()
        # Plot the function curve using X and Y values
        ax.plot(xbase, ybase)

        # Set labels for the X and Y axes
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")

        # Initialize variables to track the best solution
        bestX = startingX
        bestY = func(bestX)
        # Create lists to store the trajectory of X and Y during optimization
        xplot = [bestX]
        yplot = [bestY]

        # Print the starting point
        print(f"The starting point is ({round(bestX, 3)}, {round(bestY, 3)})")

        # Initialize markers for visualizing the optimization process
        lnall,  = ax.plot([], [], 'ro')  # All points
        lngood, = ax.plot([], [], 'go', markersize=10)  # Good (best) point

        # Start recording frames for the animation
        with problem.saving(fig, problemName + ".GIF", 300):
            for i in range(stepCount):
                # Constraining X to lie in the specified range
                adderX = 0
                if (bestX < 0):
                    adderX = xLims[0]
                bestX = bestX%xLims[1] + adderX

                # Update the current bestX by moving it in the opposite direction of the gradient
                bestX -= xDerivative(bestX) * learningRate
                # Compute the corresponding Y value for the new bestX
                bestY = func(bestX)
                # Append the new values to the trajectory lists
                xplot.append(bestX)
                yplot.append(bestY)

                # Set the 'good' point marker to the current bestX and bestY
                lngood.set_data([bestX], [bestY])
                # Set the 'all' points marker to the trajectory so far
                lnall.set_data(xplot, yplot)

                # Grab a frame for the animation
                problem.grab_frame()

        # Print and display the local minimum found
        print(f"The local minima found is ({round(bestX, 3)}, {round(bestY, 3)})")
        plt.show()
        # Return the coordinates of the local minimum
        return (bestX, bestY)

    # For Two Independent Variables Problems
    else:
        # Create a linear space for X and Y within certain limits with leeway
        xbase = np.linspace(xLims[0] - leeway, xLims[1] + leeway, numberOfPoints)
        ybase = np.linspace(yLims[0] - leeway, yLims[1] + leeway, numberOfPoints)

        # Create a grid of X and Y values using meshgrid
        X, Y = np.meshgrid(xbase, ybase)
        # Evaluate the function over the grid to obtain Z values
        zbase = func(X, Y)
        # Create a new figure with 3D projection
        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
        # Set the view angle for the 3D plot
        ax.view_init(elev=0, azim=azimuth)
        # Plot the surface of the function in 3D
        ax.plot_surface(X, Y, zbase, cmap=cm.magma_r)
        # Plot the X and Y base values
        ax.plot(xbase, ybase)

        # Set labels for the X and Y axes
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")

        # Initialize variables to track the best solution
        bestX = startingX
        bestY = startingY
        bestZ = func(bestX, bestY)
        # Create lists to store the trajectory of X, Y, and Z during optimization
        xplot = [bestX]
        yplot = [bestY]
        zplot = [bestZ]

        # Print the starting point
        print(f"The starting point is ({round(bestX, 3)}, {round(bestY, 3)}, {round(bestZ, 3)})")

        # Start recording frames for the animation
        with problem.saving(fig, problemName + ".GIF", 300):
            for i in range(stepCount):
                adderX = 0
                adderY = 0
                # Handle boundary conditions
                if (bestX < 0):
                    adderX = xlim3[0]
                if (bestY < 0):
                    adderY = ylim3[0]

                # Apply boundary conditions and calculate the new bestX and bestY
                bestX = bestX % xlim3[1] + adderX
                bestY = bestY % ylim3[1] + adderY

                # Calculate the gradient components for X and Y
                diffX = xDerivative(bestX, bestY) * learningRate
                diffY = yDerivative(bestX, bestY) * learningRate

                # Update bestX and bestY based on the gradient descent step
                bestX = bestX - diffX
                bestY = bestY - diffY
                adderX = 0
                adderY = 0
                # Handle boundary conditions
                if (bestX < 0):
                    adderX = xlim3[0]
                if (bestY < 0):
                    adderY = ylim3[0]

                # Apply boundary conditions and calculate the new bestX and bestY
                bestX = bestX % xlim3[1] + adderX
                bestY = bestY % ylim3[1] + adderY

                # Calculate the corresponding Z value for the new bestX and bestY
                bestZ = func(bestX, bestY)

                # Append the new values to their respective trajectory lists
                xplot.append(bestX)
                yplot.append(bestY)
                zplot.append(bestZ)

                # Scatter plot the trajectory points
                ax.scatter(xplot, yplot, zplot, color='black', marker='.')
                
                # Grab a frame for the animation
                problem.grab_frame()

            # Scatter plot the final bestX, bestY, and bestZ
            ax.scatter(bestX, bestY, bestZ, color='green', marker='o', s=80)
            problem.grab_frame()

        # Print and display the local minimum found
        print(f"The local minima found is ({round(bestX, 3)}, {round(bestY, 3)}, {round(bestZ, 3)})")
        plt.show()

        # Return the coordinates of the local minimum (X, Y, Z)
        return (bestX, bestY, bestZ)


# Problem 1 - 1-D simple polynomial

# The gradient is not specified.  You can write the function for gradient on your own.  
# The range within which to search for minimum is [-5, 5].

print("\nProblem 1")

def f1(x):
    return x ** 2 + 3 * x + 8
def gradientf1(x):
    return 2 * x + 3

gradDescent((0.5 - np.random.random()) * 10, 0.1, f1, gradientf1, [-5, 5], 20, "Problem 1")

 
# ## Problem 2 - 2-D polynomial
# Functions for derivatives, as well as the range of values within which to search for the minimum, are given.

print("\nProblem 2")

xlim3 =  [-10, 10]
ylim3 =  [-10, 10]
def f3(x, y):
    return x**4 - 16*x**3 + 96*x**2 - 256*x + y**2 - 4*y + 262

def df3_dx(x, y):
    return 4*x**3 - 48*x**2 + 192*x - 256

def df3_dy(x, y):
    return 2*y - 4

gradDescent((0.5 - np.random.random()) * xlim3[1], 0.05, f3, df3_dx, xlim3, 20, "Problem 2", 10, (0.5 - np.random.random()) * ylim3[1], df3_dy, ylim3)

# ## Problem 3 - 2-D function 
# 
# Derivatives and limits given. 

print("\nProblem 3\n")

xlim4 = [-np.pi, np.pi]
def f4(x,y):
    return np.exp(-(x - y)**2) * np.sin(y)

def df4_dx(x, y):
    return -2 * np.exp(-(x - y)**2) * np.sin(y) * (x - y)

def df4_dy(x, y):
    return np.exp(-(x - y)**2) * np.cos(y) + 2 * np.exp(-(x - y)**2) * np.sin(y)*(x - y)


gradDescent((0.5 - np.random.random()) * xlim4[1], 0.5, f4, df4_dx, xlim4, 50, "Problem 3", 10, (0.5 - np.random.random()) * xlim4[0], df4_dy, xlim4, numberOfPoints=500, azimuth=-70)
# ## Problem 4 - 1-D trigonometric
# 
# Derivative not given.  Optimization range [0, 2*pi]

print("\nProblem 4\n")
def f5(x):
    return np.cos(x)**4 - np.sin(x)**3 - 4*np.sin(x)**2 + np.cos(x) + 1

def gradientf5(x):
    return -4 * np.sin(x) * np.cos(x)**3 - 3 * np.cos(x) * np.sin(x)**2 - 8 * np.sin(2*x) -np.sin(x)

(bestX, bestY) = gradDescent(np.random.rand() * 2 * math.pi, 0.1, f5, gradientf5, [0, 2 * math.pi], 20, "Problem 4", numberOfPoints=300)