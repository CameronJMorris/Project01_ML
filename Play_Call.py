import random
from sklearn.linear_model import LogisticRegression

class Play_Call:
    """
            creates a logistic model that predicts the percentage of run or passed based on the circumstances

            Args:
                a (dataframe): this is all of the football data
            Returns:
                nothing
            """
    def __init__(self, data):
        self.data = data
        model = LogisticRegression()
        X = self.data[["Down", "ToGo", "YardLine", "TimeLeft"]]
        y = self.data[["PlayCalled"]]
        model.fit(X, y)
        self.model = model

    """
            Uses the model created above to predict the percentage of run or passed based on the circumstances and then
            uses the probability along with a random float generator to choose on or the other in accordance to the 
            odds

            Args:
                Args:
                a (int): the down
                b (int): how many yards until first down
                c (int): what the current yard line is
                d (int): how much time is left in the game
            Returns:
                whether the play is a run or a pass
            """
    def Get_Play_Call(self, Down, ToGo, YardLine, TimeLeft):
        arr = self.model.predict([[Down, ToGo, YardLine, TimeLeft]])
        i = random.random()
        if i < arr[0]:
            return 0
        else:
            return 1