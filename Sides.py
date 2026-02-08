class Sides:
    def __init__(self):
        self.Eval = None
        self.pieceVal = 0
        self.AttackVal = 0
        self.DefenseVal = 0
        self.PosVal = 0
        self.PosMoves = []
        self.PosAttack = list()
        self.PosDefence = list()
        self.kingPos = []
        self.king = None
        self.check = False
        self.CastlePositions = []
    def set_eval(self):
        self.Eval = self.pieceVal +self.AttackVal + self.PosVal

    def reset(self):
        self.__init__(self.enemy)


class WhiteSide(Sides):
    def __init__(self, enemy=None):
        self.enemy = enemy
        super().__init__()
        
    _instance = None

    def __new__(cls, *args, **kwargs):  #Singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __str__(self):
        return "white"


class BlackSide(Sides):
    def __init__(self, enemy=None):
        self.enemy = enemy
        super().__init__()

    _instance = None

    def __new__(cls, *args, **kwargs):  #Singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __str__(self):
        return "black"