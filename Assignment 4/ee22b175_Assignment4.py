import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = np.loadtxt("Admission_Predict_Ver1.1.csv", delimiter=',', skiprows=1)

# Extract the features and target variable and normalizing them to draw meaningful inferences
greScore = data[:,1]/340
toeflScore = data[:,2]/120
uniRating = data[:,3]/5
sopRating = data[:,4]/5
lorRating = data[:,5]/5
cgpa = data[:,6]/10
researchRating = data[:,7]
chanceOfAdmit = data[:,8]

# Calculating the Pearson Correlation coefficient matrix
correlationMatrix = np.corrcoef([greScore, toeflScore, uniRating, sopRating, lorRating, cgpa, researchRating,chanceOfAdmit], rowvar=True)

# Create the feature matrix
M = np.column_stack([greScore, toeflScore, uniRating, sopRating, lorRating, cgpa, researchRating, np.ones(len(chanceOfAdmit))])

# Calculate the least squares coefficients
(a, b, c, d, e, f, g, h), _, _, _ = np.linalg.lstsq(M, chanceOfAdmit, rcond=None)
"""
    a: The coefficient for the GRE score term.
    b: The coefficient for the TOEFL score term.
    c: The coefficient for the university rating term.
    d: The coefficient for the SOP rating term.
    e: The coefficient for the LOR rating term.
    f: The coefficient for the CGPA term.
    g: The coefficient for the research rating term.
    h: The constant correction term.
"""

# Print the linear regression equation
print(f"Chances of Admit = {round(a, 5)} * GRE Score + {round(b, 5)} * TOEFL Score + {round(c, 5)} * University Rating + {round(d, 5)} * SOP Rating + {round(e, 5)} * LOR Rating + {round(f, 5)} * CGPA + {round(g, 5)} * Research - {abs(round(h, 5))}")

# Define a function to calculate the predicted chance of admit
def AdmitCalc(gre, toefl, uniR, sop, lor, cgpa, research):
    """Calculates the predicted chance of admit.

  Args:
    gre: The GRE score.
    toefl: The TOEFL score.
    uniR: The university rating.
    sop: The Statement of Purpose rating.
    lor: The Letter of Recommendation rating.
    cgpa: The CGPA.
    research: The research rating.

  Returns:
    A float equal the predicted chance of admit.
  """
    return a * gre + b * toefl + c * uniR + d * sop + e * lor + f * cgpa + g * research + h

# Calculate the predicted chances of admit
predictedChances = np.array(AdmitCalc(greScore, toeflScore, uniRating, sopRating, lorRating, cgpa, researchRating))

# Calculate the error
error = predictedChances - chanceOfAdmit

# Calculate the absolute error
absError = np.absolute(error)

# Define a function to calculate the mean squared error
def meanSquaredError(ActualY, PredictedY):
    """
    Calculate Mean Squared Error (MSE) between true and predicted values.

    Parameters:
        ActualY (list or array): True values of the dependent variable.
        PredictedY (list or array): Predicted values of the dependent variable.

    Returns:
        float: Mean Squared Error.
    """
    size = len(ActualY)
    meanSqError = np.sum((ActualY - PredictedY)**2) / size
    return meanSqError

# Calculating the mean squared error of the predicted chances of admission
meanSqErr = meanSquaredError(chanceOfAdmit, predictedChances)
print(f"Mean Squared Error of the Preicted Chances is {meanSqErr}")

# Plot the predicted chances and absolute error vs actual chances of admit
plt.scatter(chanceOfAdmit, predictedChances, label = "Predicted Chances of Admission")
plt.scatter(chanceOfAdmit, absError, label = "Absolute Error")
plt.xlabel("Actual Chances of Admit")
plt.yticks(np.arange(0.0, 1.0, 0.1))
plt.legend()
plt.show()