from Character import Character


class Player():
    """
    A class used to represent a player
    ...

    Attributes
    ----------
    hp : int
    character : Character
    enemyType : str
    booster : list
    """

    def __init__(self):
        self.hp = 25
        self.character = Character("Aquarder", "Agua", skills={"Aqua-jet":[3,5,2,5,7,4], "Cola ferrea": [2], "Cabezazo": [2]},
                        advantage=["Roca", "Fuego"], disadvantage=["Electrico", "Planta"], normal=["Agua", "Escarabajo"],
                        booster="Lluvia", path="Personajes/aquarder.png")
        self.enemyType = "Roca"
        self.booster = [False, 0]
        self.level = 0


    def attack(self, chosenAttack):
        if chosenAttack != self.character.booster:
            points = self.character.skills[chosenAttack]
            if len(points) > 1:
                if self.__inAdvantage():
                    return points[1] + self.__boosterPoints()
                elif self.__inDisadvantage():
                    return points[2] + self.__boosterPoints()
                else:
                    return points[0] + self.__boosterPoints()
            else:
                return points[0] + self.__boosterPoints()
            
        
        self.booster[0] = True 

        return 0

    def receiveAttack(self, points):
        self.hp -= points

    def __boosterPoints(self):
        using = self.booster[0]
        time = self.booster[1]

        if using and time < 3:
            self.booster[1] += 1

            if time == 3:
                return 0
            return 2   
        else:
            self.booster[0] = False
            self.booster[1] = 0
        
        return 0

    def boosterAvailable(self):
        return not self.booster[0] 
        
    def __inAdvantage(self):
        if self.enemyType in self.character.advantage:
            return True
        return False

    def __inDisadvantage(self):
        if self.enemyType in self.character.disadvantage:
            return True
        return False
