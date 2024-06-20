# Travelling Salesman Problem - Assignment 6
# Written by EE22B175
# Dattatreya Sastry Jonnalagadda

import numpy as np
import matplotlib.pyplot as plt
import math
import sys

def pointDist(pointA, pointB):
  """Calculates the distance between two points.

  Args:
    pointA: A tuple of two floats, representing the coordinates of the first point.
    pointB: A tuple of two floats, representing the coordinates of the second point.

  Returns:
    A float representing the distance between the two points.
  """

  # Calculate the difference in the x and y coordinates of the two points.
  xDiff = pointA[0] - pointB[0]
  yDiff = pointA[1] - pointB[1]

  # Square the differences and add them together.
  squaredDist = xDiff**2 + yDiff**2

  # Take the square root of the squared distance to get the actual distance.
  dist = math.sqrt(squaredDist)

  # Return the distance.
  return dist

def distance(cities, cityorder):
  """Calculates the total distance between a list of cities in the order specified.

  Args:
    cities: A list of tuples of two floats, representing the coordinates of the cities.
    cityorder: A list of integers, representing the order in which to visit the cities.

  Returns:
    A float representing the total distance between the cities in the order specified.
  """

  # Initialize the total distance.
  totalDistance = 0
  # Iterate over the cities in the order specified.
  for i in range(len(cityorder) - 1):
    # Add the distance between the current city and the next city to the total distance.
    totalDistance += pointDist(cities[i], cities[i+1])

  # Add the distance between the last city and the first city to the total distance
  totalDistance += pointDist(cities[-1], cities[0])

  return totalDistance

def nearestneighbourSearch(cities):
  """
  Finds the nearest neighbor tour of a list of cities.

  Args:
    cities: A list of 2D coordinates, where each coordinate represents a city.

  Returns:
    A list of integers representing the order in which to visit the cities in the
    nearest neighbor tour.
  """

  # Choose a random starting city.
  startingCity = np.random.randint(0, len(cities))

  # Initialize the city order and the list of cities left to visit.
  cityOrder = [startingCity]
  citiesLeft = [n for n in (range(len(cities)))]
  citiesLeft.remove(startingCity)

  # Iterate until all cities have been visited.
  i = startingCity
  while(len(citiesLeft) != 0):

    # Find the nearest neighbor to the current city.
    nearestNeighbour = citiesLeft[0]
    nNDistance = pointDist(cities[i], cities[nearestNeighbour])
    for j in citiesLeft:
      # If a city is closer to the current city than the current nearest
      # neighbor, update the nearest neighbor.
      if(pointDist(cities[i], cities[j]) < nNDistance):
        nearestNeighbour = j
        nNDistance = pointDist(cities[i], cities[nearestNeighbour])

    # Add the nearest neighbor to the city order and remove it from the list of
    # cities left to visit.
    cityOrder.append(nearestNeighbour)
    citiesLeft.remove(nearestNeighbour)

    # Set the current city to the nearest neighbor.
    i = nearestNeighbour

  # Return the city order.
  return cityOrder

def tsp(cities):
  """Solves the traveling salesman problem using simulated annealing.

  Args:
    cities: A list of tuples of two floats, representing the coordinates of the cities.

  Returns:
    A list of integers, representing the order in which to visit the cities to minimize the total distance traveled.
  """

  # Initialize the city order.
  cityOrder = [n for n in range(len(cities))]

  # Initialize the temperature.
  temperature = 0.5

  # Initialize a counter that keeps track of the number of times city orders with the same distance have appeared consecutively
  # The total distance is the "Fitness" of the order, the lesser the distance the better Fitness
  sameFitnessCounter = 0

  currentDistance = 0 
  # While we do not encounter orders of the same fitness 2000 times in a row
  while (sameFitnessCounter <= 2000):
    previousDistance = currentDistance
    # Get the current cities and distance.
    currentCities = [cities[k] for k in cityOrder]
    currentDistance = distance(currentCities, cityOrder)

    swappedOrder = cityOrder[:]
    swap = np.random.default_rng()

    # Swap two random cities in the order.
    swappedCityOrder = swap.choice(40, 2, replace=False)
    temp = swappedOrder[swappedCityOrder[0]]
    swappedOrder[swappedCityOrder[0]] = swappedOrder[swappedCityOrder[1]]
    swappedOrder[swappedCityOrder[1]] = temp

    # Get the swapped cities and distance.
    swappedCities = [cities[k] for k in swappedOrder]
    randomDistance = distance(swappedCities, swappedOrder)

    # If the random distance is less than or equal to the current distance,
    # then accept the random city order.
    if randomDistance <= currentDistance:
      cityOrder = swappedOrder

    if previousDistance == currentDistance:
      sameFitnessCounter += 1

    else:
      sameFitnessCounter = 0
      # If the temperature is not 0
      # accept the random city order with a probability that depends
      # exponentially on the difference in total distances between the current and the previous order (Difference in Fitness)
      # divided by the temperature 
      if(temperature >= 3e-200):
        probability = np.exp(-(randomDistance - currentDistance) / temperature)
        rng = np.random.rand()
        if rng <= probability:
          cityOrder = swappedOrder
      # Otherwise return the previous city order
      else:
        continue

    # Decrease the temperature exponentially
    temperature /= 1.1

  # Return the city order.
  return cityOrder

# Get the filename from the command line arguments.
filename = sys.argv[1]

# Open the file for reading.
fPointer = open(filename, "r")

# Read all of the lines from the file.
lines = fPointer.readlines()

# Get the number of cities from the first line of the file.
numberOfCities = int(lines[0])

# Create empty lists to store the x and y coordinates of the cities.
x_cities = []
y_cities = []

# Iterate over the remaining lines in the file and parse the city coordinates.
for i in range(1, numberOfCities + 1):
    line = lines[i].split()
    x_cities.append(float(line[0]))
    y_cities.append(float(line[1]))

# Close the file.
fPointer.close()

# Convert the x and y coordinates to numpy arrays.
x_cities = np.array(x_cities)
y_cities = np.array(y_cities)

# Create a list of cities, where each city is represented as a list of coordinates.
cities = list(zip(x_cities, y_cities))

# Generating a random order of cities and finding the distance to be travelled along that random path
randomCityOrder = [n for n in (range(len(cities)))]
np.random.shuffle(randomCityOrder)
randomOrderDistance = distance(cities, randomCityOrder)

# Find the nearest neighbor search of the cities.
finalOrder = nearestneighbourSearch(cities)

# Reorder the x and y coordinates to match the nearest neighbor search order.
x_cities = x_cities[finalOrder]
y_cities = y_cities[finalOrder]

# Update the list of cities with the reordered coordinates.
cities = list(zip(x_cities, y_cities))

# Solve the traveling salesman problem using the nearest neighbour search order as its jumping off point
finalorder = tsp(cities)


# Rearrange the city coordinates for plotting.
xplot = x_cities[finalorder]
yplot = y_cities[finalorder]
cityCoords = list(zip(xplot, yplot))

# Print the final city order and distance traveled.
distanceTravelled = distance(cityCoords, finalorder)
print(f"The Order for the Salesman to travel is {finalorder}.")
print(f"The Distance to Travel is {distanceTravelled}.")

# Calculate the percentage improvement in the path.
improvementPercentage = (randomOrderDistance - distanceTravelled) * 100/(randomOrderDistance)
# Print the percentage improvement.
print(f"The percentage improvement in the path that is seen starting from a random initial point to the best possible solution found is {improvementPercentage}%.")

# Append the first city coordinates to the end of the list for plotting.
xplot = np.append(xplot, xplot[0])
yplot = np.append(yplot, yplot[0])

# Plot the city coordinates.
plt.plot(xplot, yplot, 'o-')
plt.show()