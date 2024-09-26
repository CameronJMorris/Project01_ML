import pandas as pd
from Drive import *
import warnings
warnings.filterwarnings("ignore")

class Simulate:

    def __init__(self):
        df = pd.read_csv("pbp-2023.csv")
        df = df[["Quarter", "Minute", "Second", "Down", "ToGo", "YardLine", "IsRush", "IsPass", "PlayType", "Yards",
                 "DefenseTeam", "OffenseTeam"]]
        filtered_df = df[df['PlayType'].isin(['PASS', 'RUSH', 'SACK'])].copy()
        filtered_df = filtered_df[filtered_df['Yards'] >= -20]
        filtered_df["TimeLeft"] = filtered_df.apply(self.Time_Left_In_Half, axis=1)
        filtered_df["PlayCalled"] = filtered_df["PlayType"].apply(lambda x: 1 if x == "RUSH" else 0)
        self.data = filtered_df

    """
            Uses simple arithmatic to calculate the time in seconds left in the game

            Args:
                a (dataframe): a singular row of the dataframe
            Returns:
                the total seconds remaining in the game
            """
    def Time_Left_In_Half(self, row):
        times = 0
        times += (4 - int(row["Quarter"])) * 15 * 60 + 60 * int(row["Minute"]) + int(row["Second"])
        return times

"""
        creates a simulate object and a drive object that represents the drive and then uses the loop  that
        simulates a drive by using the situation returned and received by the play function and only stopping
        when it is returned six zeros, which represent a touchdown, or field goal , or punt or turnover

        Args:
            none
        Returns:
            nothing
        """
if __name__ == "__main__":
    s = Simulate()
    d = Drive(s.data, "BUF", "CIN", 25, 1000)
    play = []
    while play != [0,0,0,0,0,0]:
        play = d.Play(play)
