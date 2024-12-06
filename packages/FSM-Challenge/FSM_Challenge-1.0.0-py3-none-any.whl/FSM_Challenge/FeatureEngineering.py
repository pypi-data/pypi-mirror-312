from collections import Counter
from itertools import combinations
from .utils import *
import pandas as pd
import numpy as np
import networkx as nx

class FeatureEngineeringProcessor:
    def __init__(self, visits_file, network_file, output_file):
        self.visits_file = visits_file
        self.network_file = network_file
        self.output_file = output_file

    def encode_features(self, df):
        df.rename(columns={'visit_date:': 'visit_date'}, inplace=True)
        df['outcome'] = df['outcome'].map({'SUCCESS': 1, 'FAIL': 0})
        df['original_reported_date'] = pd.to_datetime(df['original_reported_date'], errors='coerce')
        df['visit_date'] = pd.to_datetime(df['visit_date'], errors='coerce')
        df['node_type_numeric'] = df['node_type'].str.extract('(\d+)', expand=False).astype(int)
        df['task_type_numeric'] = df['task_type'].str.extract('(\d+)', expand=False).astype(int)

        dummies = pd.get_dummies(df['node_type_numeric'], prefix="node_type")
        df = pd.concat([df, dummies], axis=1)
        dummies = pd.get_dummies(df['task_type_numeric'], prefix="task_type")
        df = pd.concat([df, dummies], axis=1)

        df['engineer_skill_level_numeric'] = df['engineer_skill_level'].str.extract('(\d+)', expand=False).astype(int)
        df['node_id_numeric'] = df['node_id'].str.extract('(\d+)', expand=False).astype(int)
        dummies = pd.get_dummies(df['node_id_numeric'], prefix="node_id")
        df = pd.concat([df, dummies], axis=1)
        df['task_id_numeric'] = df['task_id'].str.extract('(\d+)', expand=False).astype(int)

        return df

    def compute_network_features(self, G, df_visits):
        features = {
            'degree': dict(G.degree()),
            'degree_centrality': nx.degree_centrality(G),
            'closeness_centrality': nx.closeness_centrality(G),
            'betweenness_centrality': nx.betweenness_centrality(G),
            'eigenvector_centrality': nx.eigenvector_centrality(G, max_iter=1000),
            'clustering_coefficient': nx.clustering(G),
            'pagerank': nx.pagerank(G, alpha=0.85),
        }
        df_network = pd.DataFrame(features)
        df_network['node_id'] = df_network.index

        hubs, authorities = nx.hits(G, max_iter=1000)
        df_network['authority_score'] = df_network['node_id'].map(authorities).fillna(0)
        df_network['hub_score'] = df_network['node_id'].map(hubs).fillna(0)

        df_network['avg_neighbor_degree'] = df_network['node_id'].apply(lambda x: avg_neighbor_degree(x, G))
        df_network['sum_neighbor_pagerank'] = df_network['node_id'].apply(lambda x: sum_neighbor_pagerank(x, df_network, G))
        df_network['avg_shortest_path_length'] = df_network['node_id'].apply(lambda x: compute_avg_shortest_path_length(x, G))

        df_merged = df_visits.merge(df_network, on='node_id', how='left')
        return df_merged

    def add_lag_features(self, df_visits: pd.DataFrame) -> pd.DataFrame:
        """
        Add features based on the previous visits.

        Parameters
        ----------
        df_visits : pd.DataFrame 
            The DataFrame of visits data.

        Returns
        -------
        pd.DataFrame
            The DataFrame with the added features.
        """
        # Add the previous engineer skill level feature
        df_visits['previous_engineer_skill_level_numeric'] = df_visits.groupby(
            ['node_id_numeric', 'task_id_numeric']
        )['engineer_skill_level_numeric'].shift(1)

        # Add the second previous engineer skill level feature
        df_visits['second_previous_engineer_skill_level_numeric'] = df_visits.groupby(
            ['node_id_numeric', 'task_id_numeric']
        )['engineer_skill_level_numeric'].shift(2)

        # Fill missing values in 'previous_engineer_skill_level_numeric' with -1 (indicating no previous visit)
        # Fill missing values in 'second_previous_engineer_skill_level_numeric' with -1 (indicating no previous visit)
        df_visits['previous_engineer_skill_level_numeric'].fillna(-1, inplace=True)
        df_visits['second_previous_engineer_skill_level_numeric'].fillna(-1, inplace=True)
        
        # Make sure the numeric values are integers
        df_visits['previous_engineer_skill_level_numeric'] = df_visits['previous_engineer_skill_level_numeric'].astype(int)
        df_visits['second_previous_engineer_skill_level_numeric'] = df_visits['second_previous_engineer_skill_level_numeric'].astype(int)

        # Add the previous visit date feature
        df_visits['previous_visit_date'] = df_visits.groupby(['node_id_numeric', 'task_id_numeric'])['visit_date'].shift(1)
        
        # Calculate 'time_since_last_visit' in days
        df_visits['time_since_last_visit'] = (df_visits['visit_date'] - df_visits['previous_visit_date']).dt.days

        # Fill missing values in 'time_since_last_visit' with -1 (indicating no previous visit)
        df_visits['time_since_last_visit'].fillna(-1, inplace=True)
        
        # Add external features for time
        df_visits['visit_year'] = df_visits['visit_date'].dt.year
        df_dummies = pd.get_dummies(df_visits['visit_year'], prefix='visit_year')
        df_visits = pd.concat([df_visits, df_dummies], axis=1)
        df_visits['visit_month'] = df_visits['visit_date'].dt.month
        df_visits['visit_day'] = df_visits['visit_date'].dt.day
        df_visits['visit_dayofweek'] = df_visits['visit_date'].dt.dayofweek
        df_visits['visit_weekofyear'] = df_visits['visit_date'].dt.isocalendar().week.astype(int)
        df_visits['visit_quarter'] = df_visits['visit_date'].dt.quarter
        df_visits['visit_is_weekend'] = df_visits['visit_dayofweek'].isin([5, 6]).astype(int)
        df_visits['reported_month'] = df_visits['original_reported_date'].dt.month
        df_visits['reported_day'] = df_visits['original_reported_date'].dt.day
        df_visits['reported_dayofweek'] = df_visits['original_reported_date'].dt.dayofweek
        df_visits['reported_weekofyear'] = df_visits['original_reported_date'].dt.isocalendar().week.astype(int)
        df_visits['reported_quarter'] = df_visits['original_reported_date'].dt.quarter
        df_visits['reported_is_weekend'] = df_visits['reported_dayofweek'].isin([5, 6]).astype(int)

        # Calculate time differences
        df_visits['task_age_days'] = (df_visits['visit_date'] - df_visits['original_reported_date']).dt.days

        # Cyclical encoding
        df_visits['visit_month_sin'] = np.sin(2 * np.pi * df_visits['visit_month'] / 12)
        df_visits['visit_month_cos'] = np.cos(2 * np.pi * df_visits['visit_month'] / 12)
        df_visits['visit_dayofweek_sin'] = np.sin(2 * np.pi * df_visits['visit_dayofweek'] / 7)
        df_visits['visit_dayofweek_cos'] = np.cos(2 * np.pi * df_visits['visit_dayofweek'] / 7)

        df_visits['reported_month_sin'] = np.sin(2 * np.pi * df_visits['reported_month'] / 12)
        df_visits['reported_month_cos'] = np.cos(2 * np.pi * df_visits['reported_month'] / 12)
        df_visits['reported_dayofweek_sin'] = np.sin(2 * np.pi * df_visits['reported_dayofweek'] / 7)
        df_visits['reported_dayofweek_cos'] = np.cos(2 * np.pi * df_visits['reported_dayofweek'] / 7)

        # Ensure that 'time_since_last_visit' and 'previous_engineer_skill_level_numeric' are integers
        df_visits['time_since_last_visit'] = df_visits['time_since_last_visit'].astype(int)  # in days
        return df_visits

    def encode_engineering_notes(self, df_visits: pd.DataFrame) -> pd.DataFrame:
        """
        Encode engineer notes into features.

        Parameters
        ----------
        df_visits : pd.DataFrame
            Visits data with a column named 'engineer_note' containing note text.

        Returns
        -------
        pd.DataFrame
            The input DataFrame with additional columns for each unique token in
            the notes, as well as columns for total tokens, unique tokens, average
            token frequency, maximum token frequency, and co-occurrence score.
        """
        df_visits['engineer_note_tokens'] = df_visits['engineer_note'].str.split()

        # Flatten all tokens to find unique values
        all_tokens = set(token for tokens in df_visits['engineer_note_tokens'] for token in tokens)

        # Create one-hot-encoding columns for each unique token
        for token in all_tokens:
            df_visits[f'token_{token}'] = df_visits['engineer_note_tokens'].apply(lambda x: 1 if token in x else 0)

        df_visits['tokenized_notes'] = df_visits['engineer_note'].apply(lambda x: list(map(int, x.split())))
        token_counts = Counter([token for note in df_visits['tokenized_notes'] for token in note])

        # Calculate Token Co-occurrences
        co_occurrences = Counter(
            combo for note in df_visits['tokenized_notes'] for combo in combinations(note, 2)
        )

        # Total Tokens: Count of tokens in each note
        df_visits['total_tokens'] = df_visits['tokenized_notes'].apply(len)

        # Unique Tokens: Count of unique tokens in each note
        df_visits['unique_tokens'] = df_visits['tokenized_notes'].apply(lambda x: len(set(x)))

        # Average Token Frequency: Average frequency of tokens in each note
        token_freq_dict = dict(token_counts)
        df_visits['avg_token_frequency'] = df_visits['tokenized_notes'].apply(
            lambda x: sum(token_freq_dict[token] for token in x) / len(x) if len(x) > 0 else 0
        )

        # Max Token Frequency: Maximum token frequency in each note
        df_visits['max_token_frequency'] = df_visits['tokenized_notes'].apply(
            lambda x: max(token_freq_dict[token] for token in x) if len(x) > 0 else 0
        )

        # Co-occurrence Score: Sum of co-occurrence frequencies for all token pairs in each note
        co_occurrence_dict = dict(co_occurrences)
        df_visits['co_occurrence_score'] = df_visits['tokenized_notes'].apply(
            lambda x: sum(co_occurrence_dict.get((min(a, b), max(a, b)), 0) for a, b in combinations(x, 2))
        )
        return df_visits


    def drop_auxiliary_features(self, df_visits):
        cols_to_drop = [
            'visit_date', 'original_reported_date', 'node_id', 'task_id', 
            'task_type', 'visit_year', 'node_id_numeric', 
            'node_type_numeric', 'task_type_numeric', 'tokenized_notes', 
            'engineer_skill_level', 'task_id_numeric', 'previous_visit_date', 
            'node_type', 'visit_month', 'visit_dayofweek', 'reported_month', 
            'reported_dayofweek', 'engineer_note', 'engineer_note_tokens'
        ]
        df_visits.drop(columns=cols_to_drop, inplace=True)
        return df_visits

    def process_data(self, add_netork_features=True, add_engineer_note_features=True, add_lag_features=True):
        print("Loading data...")
        df_visits, G = load_data_and_graph(self.visits_file, self.network_file)

        print("Encoding features...")
        df_visits = self.encode_features(df_visits)

        if add_netork_features:
            print("Adding network features...")
            df_visits = self.compute_network_features(G, df_visits)

        if add_engineer_note_features:
            print("Adding engineer note features...")
            df_visits = self.encode_engineering_notes(df_visits)

        if add_lag_features:
            print("Adding lag features...")
            df_visits = self.add_lag_features(df_visits)
            
        print('Total features: ', len(df_visits.columns))
        print("Sorting processed data in time ascending order...")

        df_visits.sort_values(by=['original_reported_date', 'visit_date', 'visit_id'], ascending=True, inplace=True)
        df_visits.reset_index(drop=True, inplace=True)
        df_visits = self.drop_auxiliary_features(df_visits)

        print("Saving processed data ...")
        df_visits.to_csv(self.output_file, index=False)
        print(f"Data processing complete. Processed data saved to {self.output_file}.")
