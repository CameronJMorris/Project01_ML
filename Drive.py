from Predicted_Yards import *
from Defense_Scores import *
from Offense_Scores import *
from Play_Call import *

class Drive:
    """
    Creates the offensive, defensive, and overall models. As well as the model that predicts what kind of play
    the play call is
    Args:
        a (dataframe): data the imported football data
        b (String): The two or three letter abbreviation of the offensive team
        c (String): The two or three letter abbreviation of the defensive team
        d (int): The current yard line of the ball
        e (int): The amount of time left in the game
    Returns:
        nothing
    """

    def __init__(self, data, OffenseTeam, DefenseTeam, YardLine, TimeLeft):
        self.OffenseTeam = OffenseTeam
        self.DefenseTeam = DefenseTeam
        self.YardLine = YardLine
        self.TimeLeft = TimeLeft
        data = data.copy()
        self.OTeam = Offense_Model(data, self.OffenseTeam)
        self.DTeam = Defense_Model(data, self.DefenseTeam)
        self.Overall = Predicted_Yards(data)
        self.PlayCall = Play_Call(data)
        self.Get_Full_Name = {
    "ARI": "Cardinals", "ATL": "Falcons", "BAL": "Ravens", "BUF": "Bills",
    "CAR": "Panthers", "CHI": "Bears", "CIN": "Bengals", "CLE": "Browns",
    "DAL": "Cowboys", "DEN": "Broncos", "DET": "Lions", "GB": "Packers",
    "HOU": "Texans", "IND": "Colts", "JAX": "Jaguars", "KC": "Chiefs",
    "LAC": "Chargers", "LA": "Rams", "LV": "Raiders", "MIA": "Dolphins",
    "MIN": "Vikings", "NE": "Patriots", "NO": "Saints", "NYG": "Giants",
    "NYJ": "Jets", "PHI": "Eagles", "PIT": "Steelers", "SF": "49ers",
    "SEA": "Seahawks", "TB": "Buccaneers", "TEN": "Titans", "WAS": "Commanders"}

    """
                intakes the information and the current circumstances and prints the information about what happened
                on the play, and then returns the updated information to call the method again and to continue
                running until there is something that means the drive should end, which is signaled by returning 6 zeros

                Args:
                    a (array): [Down, ToGo, YardLine, TimeLeft, TeamO, TeamD]
                Returns:
                    the array of information passed into the function or all zeros to quit
                """
    def Play(self, Situation):
        if Situation == []:
            Situation = [1, 10, self.YardLine, self.TimeLeft, self.OTeam, self.DTeam]
        #[Down, ToGo, YardLine, TimeLeft, TeamO, TeamD]
        Play = self.PlayCall.Get_Play_Call(Situation[0], Situation[1], Situation[2], Situation[3])
        yards = 0
        r = random.random()
        if Play == 1 or r < .6: #Rush
            P_yards = self.Overall.predict(Situation[0], Situation[1], Situation[2], Situation[3], Play)
            O_yards = self.OTeam.predict(Situation[0], Situation[1], Situation[2], Situation[3], Play)
            D_yards = self.DTeam.predict(Situation[0], Situation[1], Situation[2], Situation[3], Play)
            yards = .6 * P_yards + .2 * O_yards + .2 * D_yards
            time = 30
        else:
            yards = 0
            time = 7
        yards = int(yards + .5)
        if yards >= Situation[1]:
            Situation[0] = 1
            Situation[1] = 10
        else:
            Situation[0] += 1
            Situation[1] -= yards
        if Situation[2] + int(yards + .5) > 100:
            yards = 100 - Situation[2]
        Situation[2] += yards
        Situation[3] -= time
        S_Play = lambda Play: "rush" if Play == 1 else "pass"
        print(self.Get_Full_Name.get(self.OffenseTeam) + " " + S_Play(Play) + " for " + str(yards) + " yards (" + str(Situation[0]) + " down and " + str(Situation[1]) + " yards to go)")
        if Situation[0] == 5:
            work = Situation[4]
            Situation[4] = Situation[5]
            Situation[5] = work
            print("Turnover on downs")
            return [0,0,0,0,0,0]
        if int(Situation[2]) >= 100:
            print("Touchdown!!!!")
            return [0,0,0,0,0,0]
        if int(Situation[0]) == 4:
            if Situation[2] >= 60:
                print(str(100-Situation[2] + 10) + " yard field goal")
            else:
                print("The " + self.Get_Full_Name.get(self.OffenseTeam) + " punted the ball")
            return [0,0,0,0,0,0]
        return Situation