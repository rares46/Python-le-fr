"""import for csv"""
from typing import Dict
import pandas as pd

class DataIngestor:
    """class for csv processing"""
    def __init__(self, csv_path: str):
        """initiate processing"""
        self.csv_path = csv_path
        self.dataset = pd.read_csv(self.csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]


    def _filter_by_question(self, q: str) -> pd.DataFrame:
        """filter dataset to include specified rows"""
        return self.dataset[self.dataset['Question'] == q]


    def states_mean(self, q: str) -> Dict[str, float]:
        """mean values for all states"""
        #get dataset for q
        filtered_data = self._filter_by_question(q)
        #calculate mean
        state_averages = filtered_data.groupby('LocationDesc')['Data_Value'].mean()
        #sort and return dictionar
        return state_averages.sort_values().to_dict()


    def state_mean(self, q: str, state: str) -> Dict[str, float]:
        """mean value for specific state"""
        filtered_data = self._filter_by_question(q)
        #select the state
        state_data = filtered_data[filtered_data['LocationDesc'] == state]
        return {state: state_data['Data_Value'].mean()}


    def best5(self, q: str, count: int = 5) -> Dict[str, float]:
        """top five states / top values"""
        state_averages = self.states_mean(q)
        # for q where lower is better, keep ascending order
        # for q where higher is better, reverse to descending order
        if q in self.questions_best_is_max:
            sorted_states = dict(sorted(state_averages.items(), key=lambda x: x[1], reverse=True))
        else:
            sorted_states = dict(sorted(state_averages.items(), key=lambda x: x[1]))

        return dict(list(sorted_states.items())[:count])


    def worst5(self, q: str, count: int = 5) -> Dict[str, float]:
        """worst five states / worst values"""
        state_averages = self.states_mean(q)
        #for metrics where higher is better, keep ascending order for bottom performers
        #for metrics where lower is better, reverse to descending order for bottom performers
        if q in self.questions_best_is_min:
            sorted_states = dict(sorted(state_averages.items(), key=lambda x: x[1], reverse=True))
        else:
            sorted_states = dict(sorted(state_averages.items(), key=lambda x: x[1]))

        return dict(list(sorted_states.items())[:count])


    def global_mean(self, q: str) -> Dict[str, float]:
        """global mean for all"""
        filtered_data = self._filter_by_question(q)
        return {'global_mean': filtered_data['Data_Value'].mean()}


    def diff_from_mean(self, q: str) -> Dict[str, float]:
        """difference for all states mean - global mean"""
        #global mean
        national_avg = self.global_mean(q)['global_mean']
        #specific mean
        state_averages = self.states_mean(q)

        deviations = {}
        for state, value in state_averages.items():
            deviations[state] = national_avg - value

        return deviations


    def state_diff_from_mean(self, q: str, state: str) -> Dict[str, float]:
        """difference of a specific state - global mean"""
        #global
        national_avg = self.global_mean(q)['global_mean']
        #specific
        state_avg = self.state_mean(q, state)[state]

        return {state: national_avg - state_avg}


    def mean_by_category(self, q: str) -> Dict[str, float]:
        """mean for each category + stratification"""
        filtered_data = self._filter_by_question(q)

        #group by location and demographic information
        grouped_data = filtered_data.groupby([
            'LocationDesc', 
            'StratificationCategory1',
            'Stratification1'
        ])['Data_Value'].mean()

        #convert multiindex keys to string format
        result = {}
        for indices, value in grouped_data.items():
            key = str(indices)
            result[key] = value

        return result


    def state_mean_by_category(self, q: str, state: str) -> Dict[str, Dict[str, float]]:
        """mean for each category + stratification for a specific state"""
        filtered_data = self._filter_by_question(q)
        state_data = filtered_data[filtered_data['LocationDesc'] == state]

        #group by demographic information for the specified state
        grouped_data = state_data.groupby([
            'StratificationCategory1',
            'Stratification1'
        ])['Data_Value'].mean()

        #convert multiindex keys to string format
        result = {}
        for indices, value in grouped_data.items():
            key = str(indices)
            result[key] = value

        return {state: result}
