import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, roc_auc_score, classification_report, accuracy_score
import matplotlib.pyplot as plt
from .utils import *
import warnings
warnings.filterwarnings('ignore')


class TimeSeriesModelEvaluator:
    def __init__(self, data_path: str, n_splits: int = 5, test_size: int = 1000, gap: int = 0) -> None:
        """
        Initialize TimeSeriesModelEvaluator.

        Parameters:
            data_path (str): Path to the dataframe to load.
            n_splits (int): Number of splits for TimeSeriesSplit. Default=5.
            test_size (int): Size of each test set for TimeSeriesSplit. Default=1000.
            gap (int): Gap between train and test sets for TimeSeriesSplit. Default=0.
        """
        # Path to the dataframe
        self.data_path = data_path

        # Parameters for TimeSeriesSplit
        self.n_splits = n_splits           # Number of splits
        self.test_size = test_size         # Size of each test set
        self.gap = gap                     # Gap between train and test sets

        # Load dataframe
        self.X, self.y = load_dataframe(self.data_path)

        # Initialize TimeSeriesSplit
        self.tscv = TimeSeriesSplit(n_splits=self.n_splits, test_size=self.test_size, gap=self.gap)

    def build_configurations(self, model_types: list[str], K: list[int]) -> list[dict]:
        """Build and store configurations for desired model types.

        Parameters:
            model_types (list[str]): List of model types to build configurations for.

        Returns:
            list[dict]: List of configuration dictionaries.
        """
        # Initialize empty list to store configurations
        self.configurations: list[dict] = []

        # Iterate over each model type
        for model_type in model_types:
            if model_type == 'LogisticRegression':
                # Build Logistic Regression configurations
                self.LR_configurations: list[dict] = build_LR_configurations(K)
                self.configurations += self.LR_configurations
            elif model_type == 'SVM':
                # Build SVM configurations
                self.SVM_configurations: list[dict] = build_SVM_configurations()
                self.configurations += self.SVM_configurations

        # Output total configurations
        print('Total configurations built: ', len(self.configurations))
        
        return self.configurations


    def run_evaluation(self) -> dict:
        """
        Run the evaluation for all configurations across folds.

        This method will evaluate each configuration for each fold and store the results.
        After all configurations have been evaluated, it will find the best configuration
        and return it.

        Returns:
            dict: The best configuration found after evaluation.
        """

        # Iterate over each fold
        for fold, (train_index, test_index) in enumerate(self.tscv.split(self.X), 1):
            print(f"\nRunning All Configurations for Fold {fold}:")
            # Iterate over each configuration
            for configuration in self.configurations:
                # Evaluate the configuration for the current fold
                self._evaluate_configuration(fold, train_index, test_index, configuration)
            print(f"Fold {fold} ended")

        # Find the best configuration amongst all based on average AUC
        return self._find_best_configuration()


    def _find_best_configuration(self) -> dict:
        """
        Determine and return the best configuration based on average AUC.

        Returns:
            dict: The best configuration found.
        """
        return find_best_configuration(self.configurations, self.n_splits)


    def _evaluate_configuration(
        self, fold: int, train_index: np.ndarray, test_index: np.ndarray, configuration: dict
    ) -> None:
        """Evaluate a single configuration by training and testing the model.

        Parameters:
            fold (int): The current fold number.
            train_index (np.ndarray): The indices of the training data.
            test_index (np.ndarray): The indices of the test data.
            configuration (dict): The configuration to evaluate.

        Returns:
            None
        """
        # Split data into training and test sets
        X_train, X_test = self.X.iloc[train_index].copy(), self.X.iloc[test_index].copy()
        y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]

        # Add external features to the training and test data
        X_train = add_external_features(X_train, y_train)
        X_test = add_external_features(X_test, y_test)

        # Perform feature selection using the specified method and number of features
        model, k = configuration['model'], configuration['K']
        selected_features = perform_feature_selection(X_train, y_train, method='chi2', k=k)

        # Subset the data to only include the selected features
        X_train = X_train[selected_features]
        X_test = X_test[selected_features]

        # Scale the training and test data
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train the model using the scaled training data
        model.fit(X_train_scaled, y_train)

        # Predict probabilities for ROC curve calculation
        y_prob = self._predict_probabilities(model, X_test_scaled)

        # Evaluate the model and store metrics
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        f1 = f1_score(y_test, y_pred, average="binary")
        recall = recall_score(y_test, y_pred)

        # Output the AUC for the current configuration
        print(f'AUC (k={k}): ', auc)
        save_configuration_results(configuration, model, auc, selected_features, fpr, tpr, f1, recall)  


    @staticmethod
    def _predict_probabilities(
        model: Any, X_test_scaled: np.ndarray
    ) -> np.ndarray:
        """Predict probabilities using the given model.

        Parameters:
            model (Any): The model to use for prediction.
            X_test_scaled (np.ndarray): The scaled test data to predict probabilities for.

        Returns:
            np.ndarray: The predicted probabilities, either from the model's predict_proba method
                or from the decision function.
        """
    @staticmethod
    def _predict_probabilities(
        model: Any, X_test_scaled: np.ndarray
    ) -> np.ndarray:
        """Predict probabilities using the given model.

        Parameters:
            model (Any): The model to use for prediction.
            X_test_scaled (np.ndarray): The scaled test data to predict probabilities for.

        Returns:
            np.ndarray: The predicted probabilities, either from the model's predict_proba method
                or from the decision function (normalized to [0,1]).
        """
        if hasattr(model, "predict_proba"):
            return model.predict_proba(X_test_scaled)[:, 1]
        else:
            # Use decision function for models without predict_proba (e.g., SVM with probability=False)
            y_prob = model.decision_function(X_test_scaled)
            return (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min())  # Normalize scores to [0,1]
