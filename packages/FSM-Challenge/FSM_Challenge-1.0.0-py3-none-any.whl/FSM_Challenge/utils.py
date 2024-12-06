import pandas as pd
import networkx as nx
import numpy as np
import shap
from sklearn.svm import SVC
from itertools import product
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, recall_score, roc_curve, auc
from sklearn.model_selection import permutation_test_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import KBinsDiscretizer
from typing import Any
import json


def load_data_and_graph(visits_file: str, network_file: str) -> (pd.DataFrame, nx.Graph):
    """
    Load the visits data and network graph.

    Parameters
    ----------
    visits_file : str
        The file containing the visits data.
    network_file : str
        The file containing the network graph.

    Returns
    -------
    df_visits : pd.DataFrame
        The visits data.
    G : nx.Graph
        The network graph.
    """
    df_visits = pd.read_json(visits_file, lines=True)
    G = nx.read_adjlist(network_file)
    return df_visits, G

def load_dataframe(name: str) -> (pd.DataFrame, pd.Series):
    """
    Load a CSV file into a DataFrame and split it into feature set X and target variable y.

    Parameters
    ----------
    name : str
        The name of the CSV file to load.

    Returns
    -------
    X : pd.DataFrame
        The feature set.
    y : pd.Series
        The target variable.
    """
    df = pd.read_csv(name)

    # Split the DataFrame into feature set X and target variable y
    X = df.drop("outcome", axis=1)  # Feature set
    y = df["outcome"]

    return X, y

def compute_avg_shortest_path_length(node: int, G: nx.Graph) -> float:
    """
    Calculate the average shortest path length for all nodes from a given node.

    Parameters
    ----------
    node : int
        The node to calculate the average shortest path length from.
    G : nx.Graph
        The graph.

    Returns
    -------
    mean_distance : float
        The average shortest path length.
    """
    lengths = nx.single_source_shortest_path_length(G, node)
    return np.mean(list(lengths.values()))

def avg_neighbor_degree(node: int, G: nx.Graph) -> float:
    """
    Calculate the average degree of all neighbors of a node.

    Parameters
    ----------
    node : int
        The node to calculate the average degree for.
    G : nx.Graph
        The graph.

    Returns
    -------
    mean_degree : float
        The average degree of the neighbors.
    """
    neighbors = list(G.neighbors(node))
    if not neighbors:
        return 0
    return np.mean([G.degree(n) for n in neighbors])

def sum_neighbor_pagerank(node: int, df_network: pd.DataFrame, G: nx.Graph) -> float:
    """
    Calculate the sum of pagerank for all neighbors of a node.

    Parameters
    ----------
    node : int
        The node for which to calculate the sum of pagerank of its neighbors.
    df_network : pd.DataFrame
        DataFrame containing network features, including 'pagerank'.
    G : nx.Graph
        The graph containing the node and its neighbors.

    Returns
    -------
    float
        The sum of pagerank for all neighbors of the node.
    """
    neighbors = list(G.neighbors(node))
    return np.sum([df_network.loc[df_network['node_id'] == n, 'pagerank'].values[0] for n in neighbors if n in df_network['node_id'].values])


def compute_previous_success_count(engineer_lvls: np.ndarray, outcomes_arr: np.ndarray) -> np.ndarray:
    """
    Computes the previous_success_count for each sample.
    
    Parameters:
    - engineer_lvls (np.ndarray): Array of engineer_skill_level_numeric.
    - outcomes_arr (np.ndarray): Array of outcomes (1 for success, 0 otherwise).
    
    Returns:
    - np.ndarray: Array of previous_success_count.
    """
    previous_success_count = np.zeros_like(outcomes_arr, dtype=int)
    cumulative_success = {}

    for i in range(len(engineer_lvls)):

        lvl = engineer_lvls[i]
        current_count = cumulative_success.get(lvl, 0)
        previous_success_count[i] = current_count

        if outcomes_arr[i] == 1:
            cumulative_success[lvl] = current_count + 1
            
    return previous_success_count

def compute_previous_total_visits(engineer_lvls: np.ndarray) -> np.ndarray:
    """
    Computes the previous_total_visits for each sample.
    
    Parameters:
    - engineer_lvls (np.ndarray): Array of engineer_skill_level_numeric.
    
    Returns:
    - np.ndarray: Array of previous_total_visits.
    """
    previous_total_visits = np.zeros_like(engineer_lvls, dtype=int)
    cumulative_visits = {}
    
    for i in range(len(engineer_lvls)):
        lvl = engineer_lvls[i]
        current_visit = cumulative_visits.get(lvl, 0)
        previous_total_visits[i] = current_visit
        cumulative_visits[lvl] = current_visit + 1
        
    return previous_total_visits

def compute_success_rate(previous_success_count: np.ndarray, previous_total_visits: np.ndarray) -> np.ndarray:
    """
    Computes the success_rate for each sample.
    
    Parameters:
    - previous_success_count (np.ndarray): Array of previous_success_count.
    - previous_total_visits (np.ndarray): Array of previous_total_visits.
    
    Returns:
    - np.ndarray: Array of success_rate.
    """
    success_rate = np.zeros_like(previous_success_count, dtype=float)
    non_zero_mask = previous_total_visits > 0
    success_rate[non_zero_mask] = previous_success_count[non_zero_mask] / previous_total_visits[non_zero_mask]
    return success_rate


def add_external_features(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """
    Add external feature 'success_rate' to the DataFrame X based on the outcomes in y.

    Parameters
    ----------
    X : pd.DataFrame
        DataFrame containing the feature data, including 'engineer_skill_level_numeric'.
    y : pd.Series
        Series containing the outcome data.

    Returns
    -------
    pd.DataFrame
        The input DataFrame X with additional external features.
    """
    engineer_lvls = X['engineer_skill_level_numeric'].values
    outcomes = y.values

    previous_success_count = compute_previous_success_count(engineer_lvls, outcomes)
    previous_total_visits = compute_previous_total_visits(engineer_lvls)
    success_rate = compute_success_rate(previous_success_count, previous_total_visits)
    X['success_rate'] = success_rate

    return X

def build_LR_configurations(k_for_FS: list[int] = [50, 100, 200, 250]) -> list[dict]:
    """
    Build Logistic Regression configurations.

    Parameters
    ----------
    k_for_FS : list[int]
        List of K values for feature selection.

    Returns
    -------
    list[dict]
        List of configuration dictionaries.
    """
    configurations = []
    Balanced = [True]
    penalties = ['l1', 'l2']
    c_values = [0.01, 0.1, 1]
    solvers = ['lbfgs']
    Feature_Selection_algos = ['chi2'] #, 'mutual_info_classif']
    models = []
    count_configs = 0

    # Generate all combinations of hyperparameters
    for balanced, penalty, c, solver, k in product(Balanced, penalties, c_values, solvers, k_for_FS):
        # Skip invalid penalty-solver combinations
        if solver == 'lbfgs' and penalty in ['l1', 'elasticnet']:
            continue

        configurations.append({
            'balanced': balanced,
            'penalty': penalty,
            'use_penalty': True,  # Assuming use_penalty is always True when penalties are considered
            'c': c,
            'solver': solver,
            'chi2': True,
            'K': k
        })

    for config in configurations:
        # print(f"Building model with configuration: {config}")

        # Create the Logistic Regression model
        model = LogisticRegression(
            penalty=config['penalty'],
            C=config['c'],
            solver=config['solver'],
            class_weight='balanced' if config['balanced'] else None,
            max_iter=1000  # Increase iterations for convergence
        )

        # Store the model and configuration
        models.append({
            'model': model,
            'K': config['K'],
            'AUC_scores': [],
            'f1_scores': [],
            'recall_scores': [],
            'Coefficients': [],
            "chiFeatures": [],
            'roc_curves': [],
        })
        count_configs += 1

    return models

def build_SVM_configurations(k_for_FS: list[int] = [50, 100, 200, 250]) -> list[dict]:
    """
    Generate all combinations of hyperparameters for the SVM model.

    Parameters:
        k_for_FS (list[int]): List of values for k, the number of features to select using chi2.

    Returns:
        list[dict]: A list of dictionaries where each dictionary contains the hyperparameters
            for an SVM model, including the kernel type, regularization parameter, kernel
            coefficient, and k for feature selection.
    """
    configurations = []
    kernels = ['linear']  # Supported kernel types
    c_values = [0.01]        # Regularization parameters
    gammas = ['auto']           # Kernel coefficients
    Feature_Selection_algos = ['chi2']  # Currently only chi2 is supported

    # Generate all combinations of hyperparameters
    for kernel, c, gamma, k in product(kernels, c_values, gammas, k_for_FS):
        # Skip invalid combinations (e.g., 'degree' is only relevant for 'poly' kernel)

        configurations.append({
            'kernel': kernel,
            'c': c,
            'gamma': gamma,
            'K': k,
        })

    models = []
    count_configs = 0

    for config in configurations:
        # Print for debugging or verification if needed
        # print(f"Building model with configuration: {config}")

        # Create the SVM model
        model = SVC(
            kernel=config['kernel'],
            C=config['C'],
            gamma=config['gamma'],
            class_weight='balanced',  # Assuming all models use balanced classes
            probability=True,  # Enable probability estimates for ROC calculations
        )

        # Store the model and configuration
        models.append({
            'model': model,
            'K': config['K'],
            'AUC_scores': [],
            'f1_scores': [],
            'recall_scores': [],
            'Coefficients': [],
            "chiFeatures": [],
            'roc_curves': [],
        })
        count_configs += 1

    return models


def find_best_configuration(LR_configurations: list[dict], n_splits: int) -> dict:
    """
    Identify the best configuration based on average AUC.

    Parameters:
        LR_configurations (list[dict]): List of Logistic Regression configurations with results from CV.
        n_splits (int): Number of splits used in Time Series Cross-Validation.

    Returns:
        dict: The best configuration identified.
    """
    best_auc = 0.5
    best_config = None

    # Identify the best configuration based on average AUC
    for configuration in LR_configurations:
        current_auc = sum(configuration['AUC_scores']) / n_splits
        if current_auc > best_auc:
            best_auc = current_auc
            best_config = configuration

    return best_config

def plot_configuration_results(best_config: dict, trivial_classifier_results: dict = None) -> None:
    """
    Plot the ROC curve for the best configuration and the trivial classifier, and print feature importance.

    Parameters:
        best_config (dict): The best configuration identified, containing 'roc_curves' (list of tuples of fpr and tpr) 
                            and 'Coefficients' (list of arrays).
        trivial_classifier_results (dict, optional): Results from the trivial classifier, containing 'roc_curve' 
                                                     (tuple of fpr and tpr) and 'auc' values.

    Returns:
        None
    """
    if best_config is None:
        print("No best configuration to plot.")
        return

    # Create a figure with a single subplot
    plt.figure(figsize=(8, 6))

    # Calculate mean false positive rate for interpolation
    mean_fpr = np.linspace(0, 1, 100)

    # Initialize lists to store true positive rates and AUC values
    tprs = []
    aucs = []

    # Iterate over each fold's ROC curve
    for i, (fpr, tpr) in enumerate(best_config['roc_curves']):
        # Calculate AUC value for the current fold
        auc_value = auc(fpr, tpr)
        # Store AUC value in the list
        aucs.append(auc_value)

        # Plot the ROC curve for the current fold
        plt.plot(fpr, tpr, alpha=0.6, label=f'AUC (fold {i + 1}) = {auc_value:.2f}')

        # Interpolate true positive rate at the mean false positive rate
        interp_tpr = np.interp(mean_fpr, fpr, tpr)
        # Set the first point to (0, 0)
        interp_tpr[0] = 0.0
        # Store the interpolated true positive rate in the list
        tprs.append(interp_tpr)

    # Calculate mean true positive rate and AUC
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0  # Ensure the curve ends at (1, 1)
    mean_auc = np.mean(aucs)
    std_auc = np.std(aucs)

    # Plot the mean ROC curve
    plt.plot(mean_fpr, mean_tpr, color='b', linestyle='--',
             label=f'Average AUC = {mean_auc:.2f} (±{std_auc:.2f})')

    # Plot the trivial classifier's ROC curve if provided
    if trivial_classifier_results:
        fpr, tpr = trivial_classifier_results['roc_curve']
        trivial_auc = trivial_classifier_results['auc']
        trivial_auc_std = trivial_classifier_results.get('auc_std', 0.0)  # Use 0.0 if not provided
        plt.plot(fpr, tpr, linestyle='--', color='k', 
                 label=f'Majority Classifier AUC = {trivial_auc:.2f} ({trivial_auc_std:.2f})')

    # Set up the plot
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid(True)
    plt.title('ROC Curve of best configuration VS Majority trivial classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')
    plt.show()


def evaluate_majority_classifier(
    X: pd.DataFrame,  # Feature data
    y: pd.Series,  # Target data
    tscv: TimeSeriesSplit  # Time series split object
) -> dict:
    """
    Evaluate a trivial majority classifier using time series splits.

    Parameters:
        X (pd.DataFrame): Feature data.
        y (pd.Series): Target data.
        tscv (TimeSeriesSplit): Time series split object.

    Returns:
        dict: Dictionary containing average accuracy, AUC, and the overall ROC curve.
    """
    print("\nEvaluating Trivial Majority Classifier")
    dummy_accuracies = []
    dummy_aucs = []
    all_fpr = []
    all_tpr = []

    for fold, (train_index, test_index) in enumerate(tscv.split(X), 1):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # Majority Classifier
        dummy_clf = DummyClassifier(strategy="most_frequent")
        dummy_clf.fit(X_train, y_train)

        # Predict and Evaluate
        y_pred = dummy_clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Handle single-class scenario in AUC
        if len(y_test.unique()) > 1:
            auc_score = roc_auc_score(y_test, [1] * len(y_test) if y_test.mode()[0] == 1 else [0] * len(y_test))
            fpr, tpr, _ = roc_curve(y_test, [1] * len(y_test) if y_test.mode()[0] == 1 else [0] * len(y_test))
        else:
            auc_score = 0.5  # Default to 0.5 for no discrimination
            fpr, tpr = [0, 1], [0, 1]

        dummy_accuracies.append(accuracy)
        dummy_aucs.append(auc_score)
        all_fpr = fpr
        all_tpr = tpr

        print(f"Fold {fold} - Majority Classifier Accuracy: {accuracy}, AUC: {auc_score}")

    avg_accuracy = np.mean(dummy_accuracies)
    avg_auc = np.mean(dummy_aucs)

    print(f"\nTrivial Majority Classifier Average Accuracy: {avg_accuracy}, Average AUC: {avg_auc}")

    return {
        'average_accuracy': avg_accuracy,
        'average_auc': avg_auc,
        'roc_curve': (all_fpr, all_tpr),
        'auc': avg_auc
    }


def print_results_metrics(best_config: dict) -> None:
    """
    Prints the results metrics (AUC, F1-score, Recall) for each fold and their averages with standard deviations.

    Parameters:
        best_config (dict): Dictionary containing model results and metrics.
    """
    # Check if best_config is not empty
    if not best_config:
        print("No best configuration found.")
        return

    # Extract metrics from the best_config
    auc_scores = best_config.get('AUC_scores', [])
    f1_scores = best_config.get('f1_scores', [])
    recall_scores = best_config.get('recall_scores', [])

    # Check if metrics are present
    if not auc_scores or not f1_scores or not recall_scores:
        print("Metrics are missing in the best configuration.")
        return

    # Print fold-by-fold metrics
    print("Metrics for each fold for the best configuration:")
    for i, (auc, f1, recall) in enumerate(zip(auc_scores, f1_scores, recall_scores)):
        print(f"  Fold {i + 1}:")
        print(f"    AUC: {auc:.4f}")
        print(f"    F1-Score: {f1:.4f}")
        print(f"    Recall: {recall:.4f}")

    # Calculate and print mean and standard deviation
    mean_auc, std_auc = np.mean(auc_scores), np.std(auc_scores)
    mean_f1, std_f1 = np.mean(f1_scores), np.std(f1_scores)
    mean_recall, std_recall = np.mean(recall_scores), np.std(recall_scores)

    print("\nAverage Metrics Across Folds:")
    print(f"  Average AUC: {mean_auc:.4f} (±{std_auc:.4f})")
    print(f"  Average F1-Score: {mean_f1:.4f} (±{std_f1:.4f})")
    print(f"  Average Recall: {mean_recall:.4f} (±{std_recall:.4f})")

    # Additional information (if needed)
    print("\nModel Information:")
    print(f"  Model: {best_config.get('model')}")
    print(f"  Number of Features Selected (K): {best_config.get('K')}")

    # Extract metrics from the best_config
    auc_scores = best_config.get('AUC_scores', [])
    f1_scores = best_config.get('f1_scores', [])
    recall_scores = best_config.get('recall_scores', [])
    
    if not auc_scores or not f1_scores or not recall_scores:
        print("Metrics are missing in the best configuration.")
        return

    # Print fold-by-fold metrics
    print("Metrics for each fold for the best configuration:")
    for i, (auc, f1, recall) in enumerate(zip(auc_scores, f1_scores, recall_scores)):
        print(f"  Fold {i + 1}:")
        print(f"    AUC: {auc:.4f}")
        print(f"    F1-Score: {f1:.4f}")
        print(f"    Recall: {recall:.4f}")

    # Calculate and print mean and standard deviation
    mean_auc, std_auc = np.mean(auc_scores), np.std(auc_scores)
    mean_f1, std_f1 = np.mean(f1_scores), np.std(f1_scores)
    mean_recall, std_recall = np.mean(recall_scores), np.std(recall_scores)

    print("\nAverage Metrics Across Folds:")
    print(f"  Average AUC: {mean_auc:.4f} (±{std_auc:.4f})")
    print(f"  Average F1-Score: {mean_f1:.4f} (±{std_f1:.4f})")
    print(f"  Average Recall: {mean_recall:.4f} (±{std_recall:.4f})")

    # Additional information (if needed)
    print("\nModel Information:")
    print(f"  Model: {best_config.get('model')}")
    print(f"  Number of Features Selected (K): {best_config.get('K')}")
    # print(f"  Features Used: {best_config.get('chiFeatures')}")

def save_best_config(best_config: dict) -> None:
    """
    Save the best configuration to a json file.

    Parameters:
        best_config (dict): The best configuration dictionary to save.
        trivial_classifier_results (dict, optional): Results from the trivial classifier, containing 'roc_curve' 
                                                     (tuple of fpr and tpr) and 'auc' values.

    Returns:
        None
    """
    if best_config is None:
        return

    weights = best_config['model'].coef_.tolist()
    auc_scores = best_config.get('AUC_scores', [])
    f1_scores = best_config.get('f1_scores', [])
    recall_scores = best_config.get('recall_scores', [])

    config_to_save = {
        "K": best_config.get('K', "N/A"),
        "weights": weights,
        "AUC_scores": auc_scores,
        "F1_scores": f1_scores,
        "Recall_scores": recall_scores,
    }

    with open('best_config.json', "w") as file:
        json.dump(config_to_save, file, indent=4)


def save_configuration_results(
    configuration: dict, 
    model: Any, 
    auc: float, 
    selected_features: list, 
    fpr: np.ndarray, 
    tpr: np.ndarray, 
    f1: float, 
    recall: float
) -> None:
    """
    Save the results of a single fold evaluation.

    Parameters:
        configuration (dict): The configuration dictionary to store results in.
        model (Any): The model object.
        auc (float): The AUC score for this fold.
        selected_features (list): The list of selected features for this fold.
        fpr (np.ndarray): The false positive rates for the ROC curve.
        tpr (np.ndarray): The true positive rates for the ROC curve.
        f1 (float): The F1 score for this fold.
        recall (float): The recall score for this fold.

    Returns:
        None
    """
    configuration['AUC_scores'].append(auc)
    configuration['Coefficients'].append(model.coef_)
    configuration['chiFeatures'].append(selected_features)
    configuration['roc_curves'].append((fpr, tpr))  # Store the ROC data for this fold
    configuration['f1_scores'].append(f1)
    configuration['recall_scores'].append(recall)


def add_success_rate_in_SHAP_data(dataX: pd.DataFrame, dataY: pd.Series, selected_features: list) -> pd.DataFrame:
    """
    Add 'success_rate' feature to the DataFrame dataX for SHAP analysis based on the selected features.

    Parameters
    ----------
    dataX : pd.DataFrame
        DataFrame containing the feature data.
    dataY : pd.Series
        Series containing the outcome data.
    selected_features : list
        List of features selected for SHAP analysis.

    Returns
    -------
    pd.DataFrame
        The modified DataFrame with additional features for SHAP analysis.
    """
    engineer_lvls = dataX['engineer_skill_level_numeric'].values
    outcomes = dataY.values

    previous_success_count = compute_previous_success_count(engineer_lvls, outcomes)
    previous_total_visits = compute_previous_total_visits(engineer_lvls)

    if 'success_rate' in selected_features:
        success_rate = compute_success_rate(previous_success_count, previous_total_visits)
        dataX['success_rate'] = success_rate

    return dataX

def add_success_rate_to_instance(
    instance: pd.DataFrame, 
    outcome: str
) -> pd.DataFrame:
    """
    Add the 'success_rate' feature to the instance DataFrame.

    Parameters:
        instance (pd.DataFrame): DataFrame containing the feature data of a single data point.
        outcome (str): The outcome of the data point (success or failure).

    Returns:
        pd.DataFrame: The modified DataFrame with the additional 'success_rate' feature.
    """
    engineer_lvls = instance['engineer_skill_level_numeric'].values
    outcomes = [int(outcome)]
    previous_success_count = compute_previous_success_count(engineer_lvls, outcomes)
    previous_total_visits = compute_previous_total_visits(engineer_lvls)
    success_rate = compute_success_rate(previous_success_count, previous_total_visits)
    instance['success_rate'] = success_rate
    return instance


def save_shap_summary(
    configuration: dict, 
    dataX: pd.DataFrame, 
    dataY: pd.Series
) -> None:
    """
    Generate SHAP summary plots for the given configuration and dataset.

    Parameters:
        configuration (dict): Best configuration containing the model and selected features.
        dataX (pd.DataFrame): DataFrame containing the feature data.
        dataY (pd.Series): Series containing the outcome data.

    Returns:
        None
    """
    model = configuration['model']
    selected_features = configuration['chiFeatures'][0]  # Extract selected features from configuration
    data = add_success_rate_in_SHAP_data(dataX, dataY, selected_features)

    data_filtered = data[selected_features]
    explainer = shap.Explainer(model, data_filtered)

    # Compute SHAP values for the filtered dataset and instance
    shap_values_data = explainer(data_filtered)
    shap_values_data.values = np.array(shap_values_data.values, dtype=np.float64)

    plt.figure()  # Create a new figure for the summary plot
    shap.summary_plot(shap_values_data, data_filtered, show=False, max_display=10)
    plt.savefig('SHAP_summary.jpg', dpi=300, bbox_inches='tight')
    print("SHAP summary plot saved.")


def shap_explainer(
    configuration: dict, 
    dataX: pd.DataFrame, 
    dataY: pd.Series, 
    sample: tuple, 
    name: str = 'sample'
) -> shap.Explanation:
    """
    Generate SHAP explanations for a given instance and save both the waterfall and summary plots.

    Parameters:
        configuration (dict): Best configuration containing the model and selected features.
        dataX (pd.DataFrame): Dataset used for training or evaluation.
        dataY (pd.Series): Series containing the outcome data.
        sample (tuple): A tuple containing a single data point (pd.DataFrame) and its outcome (any).
        name (str): Name identifier for the instance (default is 'sample').

    Returns:
        shap.Explanation: SHAP values for the instance.
    """
    instance, outcome = sample

    # Extract the model and selected features
    model = configuration['model']
    selected_features = configuration['chiFeatures'][0]  # Extract selected features from configuration
    data = add_success_rate_in_SHAP_data(dataX, dataY, selected_features)

    if 'success_rate' in selected_features:
        instance = add_success_rate_to_instance(instance, outcome)

    data_filtered = data[selected_features]
    instance_filtered = instance[selected_features]

    # Initialize the SHAP explainer
    explainer = shap.Explainer(model, data_filtered)
    
    # Compute SHAP values for the filtered dataset and instance
    shap_values_data = explainer(data_filtered)
    shap_values_instance = explainer(instance_filtered)

    # Plot and optionally save the waterfall plot for the instance
    plt.figure()  # Create a new figure for the waterfall plot
    shap.plots.waterfall(shap_values_instance[0], show=False)  # Disable automatic display
    plt.savefig('SHAP_'+ name + '_waterfall.jpg', dpi=300, bbox_inches='tight')
    print("SHAP Waterfall plot saved.")

    return shap_values_instance

def plot_logistic_regression_top_weights(
    configuration: dict,  # Best configuration containing the model and selected features.
    top_n: int = 15  # Number of top features to plot (default is 15).
) -> None:
    """
    Plots the top N features' importance based on the absolute values of Logistic Regression weights.

    Parameters:
        configuration (dict): Best configuration containing the model and selected features.
        top_n (int): Number of top features to plot (default is 15).
    """
    # Extract the model and selected features
    model = configuration['model']
    selected_features = configuration['chiFeatures'][0]  # List of selected feature names

    # Ensure the model is a Logistic Regression with coefficients
    if not hasattr(model, 'coef_'):
        raise ValueError("The provided model does not have coefficients. Ensure it is a Logistic Regression model.")

    # Get the coefficients and compute absolute importance
    coefficients = model.coef_.flatten()  # Flatten if there's only one target
    feature_importance = np.abs(coefficients)

    # Create a DataFrame for easy sorting
    importance_df = pd.DataFrame({
        'Feature': selected_features,
        'Importance': feature_importance
    })

    # Sort by importance and select the top N features
    importance_df = importance_df.sort_values(by='Importance', ascending=False).head(top_n)

    # Plot the feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
    plt.gca().invert_yaxis()  # Reverse the order to display the highest importance at the top
    plt.title(f"Top {top_n} Features Based on Logistic Regression Weights")
    plt.xlabel("Absolute Coefficient Value (Importance)")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig('Logistic_Regression_Top_Features.jpg', dpi=300)
    # plt.show()

def perform_feature_selection(X: pd.DataFrame, y: pd.Series, method: str, k: int) -> list:
    """
    Perform feature selection on the provided dataset.

    This function takes in the input feature data (X), the target variable (y), the
    feature selection method to use (e.g., 'chi2'), and the number of top features
    to select (k). It then applies the specified feature selection method to the
    input data and returns the list of selected feature names.

    Parameters:
        X (pd.DataFrame): The input feature data.
        y (pd.Series): The target variable.
        method (str): The feature selection method to use (e.g., 'chi2').
        k (int): The number of top features to select.

    Returns:
        list: The list of selected feature names.
    """
    if method == 'chi2':
        # Discretize the input data before applying Chi-Squared feature selection
        discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='uniform')
        X_discretized = discretizer.fit_transform(X)

        # Apply Chi-Squared feature selection
        chi2_selector = SelectKBest(score_func=chi2, k=k)
        X_new = chi2_selector.fit_transform(X_discretized, y)

        # Get the list of selected feature names
        selected_features = X.columns[chi2_selector.get_support()].tolist()

    return selected_features


def get_instance(instance_idx: int, X: pd.DataFrame, y: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
    """
    Get a single instance from the input data.

    Parameters:
        instance_idx (int): The index of the instance to retrieve. Note that indexing starts at 1.
        X (pd.DataFrame): The input feature data.
        y (pd.Series): The target variable.

    Returns:
        tuple[pd.DataFrame, pd.Series]: A tuple containing the instance data (pd.DataFrame) and the corresponding target value (pd.Series).
    """
    return X.iloc[instance_idx-1:instance_idx], y.iloc[instance_idx-1:instance_idx]