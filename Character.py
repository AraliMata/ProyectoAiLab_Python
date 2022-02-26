class Character:
    """
    A class used to represent a player
    ...

    Attributes
    ----------
    name : int
    type : Character
    skills : str
    advantage : list
    """
    def __init__(self, name, type, skills, advantage, disadvantage, normal, booster, path):
        self.name = name
        self.type = type
        self.skills = skills
        self.advantage = advantage
        self.disadvantage = disadvantage
        self.normal = normal
        self.booster = booster
        self.path = path