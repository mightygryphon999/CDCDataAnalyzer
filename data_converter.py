
import pandas as pd

from data_structs import County, DeathCount, State


class DataConverter:
    def __init__(
            self,
        ):
        pass

    def load_deaths(
                self,
                data_county_name,
                data_state_name
            ):
        data = pd.read_csv('StateCounty2023UrbanizationRaceInjuryIntentDeaths.csv')

        filtered_result = data[(data['State'] == data_state_name) & (data['County'] == data_county_name)]

        deaths = []

        for index, item in filtered_result.iterrows():

            deaths.append(
                DeathCount(
                    Intent=item["Injury Intent"],
                    Deaths=item["Deaths"],
                    Race=item["Single/Multi Race 31"],
                )
            )

        return deaths

    def load_counties(
                self,
                data_state_name
            ):
        data = pd.read_csv('StateCountyDeathPopulationCrudeRatePer100k.csv')
        data_1 = pd.read_csv('StateCounty2023UrbanizationDeaths.csv')

        filtered_result = data[data['State'] == data_state_name]

        counties = []

        for index, item in filtered_result.iterrows():


            deaths = self.load_deaths(
                data_county_name=item["County"],
                data_state_name=data_state_name
            )

            filtered_result_1 = data_1[(data_1['State'] == data_state_name) & (data_1['County'] == item["County"])]

            counties.append(
                County(
                    name=item["County"],
                    deaths=deaths,
                    population=item["Population"],
                    overall_deaths=item["Deaths"],
                    metro_size=filtered_result_1.iloc[0]["2023 Urbanization"]
                )
            )

        return counties

    def load_states(
            self,
            data: pd.DataFrame
        ):

        states: list[State] = []
        
        for index, item in data.iterrows():

            name = item["State"]

            code = item["State Code"]

            deaths = item["Deaths"]

            population = item["Population"]

            crude_rate = item["Crude Rate"]

            crude_rate_low = item["Crude Rate Lower 95% Confidence Interval"]

            crude_rate_high = item["Crude Rate Upper 95% Confidence Interval"]

            counties = self.load_counties(name)

            states.append(
                State(
                        name=name, 
                        counties=counties, 
                        population=population, 
                        state_code=code, 
                        overall_deaths=deaths, 
                        crude_rate=crude_rate, 
                        crude_rate_low=crude_rate_low, 
                        crude_rate_high=crude_rate_high
                    )
                )

        

        return states

    def load_data(self):
            data = pd.read_csv('StateDeathPopulationCrudeRatePer100k.csv')

            return self.load_states(data=data)