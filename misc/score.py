class Score:
    def __init__(self):
        self.__score = 0
        self.fear_mode = False
        self.fear_count = 0

    @property
    def score(self):
        return self.__score

    def __add_to_score(self, amount):
        self.__score += amount

    def eat_seed(self):
        self.__add_to_score(10)

    def eat_energizer(self):
        self.__add_to_score(50)

    def activate_fear_mode(self):
        self.fear_mode = True

    def deactivate_fear_mode(self):
        self.fear_mode = False
        self.fear_count = 0

    def eat_ghost(self):
        self.fear_count += 1
        self.__add_to_score(100 * 2 ** self.fear_count)