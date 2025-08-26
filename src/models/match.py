class Match():
    def __init__(self, _id, team_h, team_a, date, location, stadium_condition, weather_condition, referee, match_importance):
        self.id = _id
        self.team_h = team_h
        self.team_a = team_a
        self.date = date
        self.location = location
        self.stadium_condition = stadium_condition # ex: seco, molhado, pesado
        self.weather_condition = weather_condition # ex: ensolarado, nevando, chuvoso, nublado, quente, frio
        self.referee = referee
        self.match_importance = match_importance # ex: amistoso, copa, campeonato, final