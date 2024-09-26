from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

class Defense_Model:
    """
                        receives a defensive team and then limits the data to only the plays contains their defense
                        then create a scaler linear regression model for different scenarios

                        Args:
                            a (dataframe): data the imported football data
                            b (String): The two or three letter abbreviation of the team
                        Returns:
                            nothing
                        """
    def __init__(self, data, team):
        self.data = data[data["DefenseTeam"] == team].copy()
        self.model = LinearRegression()
        self.X = self.data[["Down", "ToGo", "YardLine", "TimeLeft", "PlayCalled"]]
        self.y = self.data["Yards"]
        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(self.X)
        self.model.fit(self.X, self.y)

    """
                intakes all of the information and uses the model created in the innit based on the 
                imported defense to get an average play distance for the team from the certain situation
                using a linear regression model

                Args:
                    a (int): the down
                    b (int): how many yards until first down
                    c (int): what the current yard line is
                    d (int): how much time is left in the game
                    e (int): whether a run or pass was called
                Returns:
                    the defensive predicted yardage
                """
    def predict(self, Down, ToGo, YardLine, TimeLeft, PlayCalled):
        df = [[Down, ToGo, YardLine, TimeLeft, PlayCalled]]
        df = self.scaler.transform(df)
        return self.model.predict(df)