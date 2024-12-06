# End to End TimeSeries Model Evaluation and Feature Engineering Library

## Overview


This project was developed as part of a **Data Science Challenge**

The objectives include:
1. Building a binary classifier to predict whether a visit to repair or maintain a node will succeed or fail.
2. Providing intuitive explanations for the classifier's predictions to ensure interpretability.

This library offers tools for preprocessing data, engineering features, evaluating models tailored to the requirements of the challenge and interpreting predictions.


The library includes:

- **FeatureEngineeringProcessor**: Comprehensive feature engineering for complex datasets.
- **TimeSeriesModelEvaluator**: Evaluate machine learning models using time series split validation.
- **Utility Functions**: Essential utilities for data manipulation, visualization, and model analysis.


## Features

### FeatureEngineeringProcessor
A comprehensive, end-to-end class designed to process the visits.txt dataset and transform it into a feature-rich, model-ready format for predictive analysis.

- **Encoding**: Converts categorical variables into numerical features using encoding techniques.
- **Lag Features**: Generates lag-based features to uncover sequential patterns and relationships in the data
- **Network Features**: Derives insights from the network structure by calculating features like degree, closeness centrality, pagerank, and more
- **Text Analysis**: Encodes engineering notes with co-occurrence metrics, token frequency analysis etc.


### TimeSeriesModelEvaluator

- **Time-Series-Cross-Validation**: Supports time-series cross-validation with custom splits, test sizes, and gaps.
- **Model Evaluation**: Built-in support for evaluating Logistic Regression and SVM with configurable hyperparameters.
- **Feature Selection**: Supports chi-squared feature selection for optimal model inputs.
- **Metrics Reporting**: Automatic computation of AUC, F1-score, recall, and ROC curves of the best configuration.

### Utility Functions
- **SHAP Analysis**: Provides SHAP explanations with waterfall and summary plots.
- **Visualization**: ROC curves, feature importance plots, and more.

## Installation

```bash 
pip install FSM-Challenge
```

## Complete Usage Example

Below is a complete example of using the library to preprocess data, evaluate models, and interpret predictions.

### Step 1: Import Necessary Modules

```python
from TimeSeriesModelEvaluator import TimeSeriesModelEvaluator
from utils import *
from FeatureEngineering import *
```

### Step 2: Define File Paths

```
VISITS_FILE = 'visits.txt'
NETWORK_FILE = 'network.adjlist'
OUTPUT_FILE = 'preprocessed_data.csv'
```

### Step 3: Data Preprocessing
Use the `FeatureEngineeringProcessor` to preprocess the data and generate features:
```
if __name__ == "__main__":
    data_processor = FeatureEngineeringProcessor(VISITS_FILE, NETWORK_FILE, OUTPUT_FILE)
    data_processor.process_data(add_netork_features=True, add_engineer_note_features=True, add_lag_features=True)
```
### Step 4: Initialize and Evaluate Models
Set up the `TimeSeriesModelEvaluator` for cross-validation and evaluate configurations:

```
evaluator = TimeSeriesModelEvaluator(data_path=OUTPUT_FILE, n_splits=5, test_size=1000, gap=0)
evaluator.build_configurations(model_types=['LogisticRegression'], K=[50, 100, 150, 200, 300])
evaluator.run_evaluation()
```

### Step 5: Find and Save the Best Model Configuration
Determine the best-performing configuration and save it:

```
best_configuration = find_best_configuration(evaluator.configurations, evaluator.n_splits)
print_results_metrics(best_configuration)
save_best_config(best_configuration)
```

### Step 6: Evaluate a Trivial Classifier for Baseline Comparison
Compare the best model with a trivial majority classifier:

```
trivial_results = evaluate_majority_classifier(evaluator.X, evaluator.y, evaluator.tscv)
plot_configuration_results(best_configuration, trivial_classifier_results=trivial_results)
```

### Step 7: Analyze Individual Predictions with SHAP
Retrieve specific instances and generate SHAP explanations:
```
instance_idx_1 = 1  # Start counting from 1
instance_idx_2 = 2

sample1 = get_instance(instance_idx_1, evaluator.X, evaluator.y)
sample2 = get_instance(instance_idx_2, evaluator.X, evaluator.y)

save_shap_summary(best_configuration, evaluator.X, evaluator.y)
shap_explainer(configuration=best_configuration, dataX=evaluator.X, dataY=evaluator.y, sample=sample1, name='Instance1')
shap_explainer(configuration=best_configuration, dataX=evaluator.X, dataY=evaluator.y, sample=sample2, name='Instance2')
```

### Step 8: Visualize Model Insights
Generate a visualization of the most important features:

```
plot_logistic_regression_top_weights(best_configuration, top_n=15)
```
