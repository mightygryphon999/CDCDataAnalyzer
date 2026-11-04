
class DeathCount:
    def __init__(
            self,
            Intent,
            Deaths,
            Race
        ):
        self.intent = Intent
        self.deaths = Deaths
        self.race = Race

    def to_dict(self):
        return {
            "intent": self.intent,
            "deaths": self.deaths,
            "race": self.race
        }

class County:
    def __init__(
            self,
            name,
            deaths: list[DeathCount],
            population: int,
            overall_deaths: int,
            metro_size: str,
            death_per_100: float
        ):
        self.name = name
        self.deaths = deaths
        self.metro_size = metro_size
        self.population = population
        self.overall_deaths = overall_deaths
        self.death_per_100 = death_per_100

    def to_dict(self):
        return {
            "name": self.name,
            "deaths": [d.to_dict() for d in self.deaths],
            "metro_size": self.metro_size,
            "population": self.population,
            "overall_deaths": self.overall_deaths,
            "death_per_100": self.death_per_100
        }

class State:
    def __init__(
            self,
            name,
            counties: list[County],
            population: int,
            state_code: int,
            crude_rate: float,
            crude_rate_high: float,
            crude_rate_low: float,
            overall_deaths: int,
            death_per_100: float
        ):
        self.name = name
        self.counties = counties
        self.population = population
        self.state_code = state_code
        self.crude_rate = crude_rate
        self.crude_rate_high = crude_rate_high
        self.crude_rate_low = crude_rate_low
        self.overall_deaths = overall_deaths
        self.death_per_100 = death_per_100

    def to_dict(self):
        return {
            "name": self.name,
            "counties": [c.to_dict() for c in self.counties],
            "population": self.population,
            "state_code": self.state_code,
            "crude_rate": self.crude_rate,
            "crude_rate_high": self.crude_rate_high,
            "crude_rate_low": self.crude_rate_low,
            "overall_deaths": self.overall_deaths,
            "death_per_100": self.death_per_100
        }

