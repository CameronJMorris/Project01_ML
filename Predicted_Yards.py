from sklearn.linear_model import QuantileRegressor
from sklearn.preprocessing import StandardScaler
from scipy.stats import skewnorm

class Predicted_Yards:
    """
        Creates the models which will be later used in the predict method and uses a quantile regressor by using
        different benchmark percentiles

        Args:
            a (dataframe): this is all of the football data
        Returns:
            nothing
        """
    def __init__(self, data):
        self.data = data.copy()

        X = self.data[['Down', 'ToGo', "YardLine", "TimeLeft", "PlayCalled"]]  # Sets the X values
        y = self.data['Yards'] # sets the criteria or Y values
        self.scalar = StandardScaler()
        X = self.scalar.fit_transform(X) # makes the model and values for the X values scalar

        self.model_10 = QuantileRegressor(quantile=.2, alpha=.01) # 10th percentile yardage
        self.model_10.fit(X, y)
        self.model_50 = QuantileRegressor(quantile=.5, alpha=.01) # 50th percentile yardage
        self.model_50.fit(X, y)
        self.model_90 = QuantileRegressor(quantile=.8, alpha=.01) # 90th percentile yardage
        self.model_90.fit(X, y)

    """
            intakes all of the information and uses the models created in the innit with a skewed graph and then
            picks a weighted random number along that graph to output as the predicted yards gained

            Args:
                a (int): the down
                b (int): how many yards until first down
                c (int): what the current yard line is
                d (int): how much time is left in the game
                e (int): whether a run or pass was called
            Returns:
                the predicted yardage
            """
    def predict(self, Down, ToGo, YardLine, TimeLeft, PlayCalled):
        yards_10 = self.model_10.predict(self.scalar.transform([[Down, ToGo, YardLine, TimeLeft, PlayCalled]]))
        yards_50 = self.model_50.predict(self.scalar.transform([[Down, ToGo, YardLine, TimeLeft, PlayCalled]]))
        yards_90 = self.model_90.predict(self.scalar.transform([[Down, ToGo, YardLine, TimeLeft, PlayCalled]]))
        StandardDeviation = (yards_90[0] - yards_10[0]) / 1.68
        skew = (yards_90[0] - yards_50[0]) / (yards_50[0] - yards_10[0])
        y_pred = skewnorm.rvs(a=skew, loc=yards_50, scale=StandardDeviation)
        return y_pred