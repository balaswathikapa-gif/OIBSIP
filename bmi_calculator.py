import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = {
    "Hours": [1, 2, 3, 4, 5, 6],
    "Marks": [35, 40, 50, 65, 75, 85]
}

df = pd.DataFrame(data)

X = df[["Hours"]]
y = df["Marks"]

model = LinearRegression()
model.fit(X, y)

predicted_marks = model.predict([[7]])

print("Predicted Marks for 7 hours:", predicted_marks[0])

plt.scatter(df["Hours"], df["Marks"])
plt.plot(df["Hours"], model.predict(X))
plt.title("Hours vs Marks Prediction")
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.show()
