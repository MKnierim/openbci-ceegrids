import pandas as pd
import numpy as np
import preprocessing as prpr
from scipy import stats
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import AdaBoostClassifier
import pickle

"""
This code shows the process of training a classifier to predict bruxism (jaw clenching) events.
The events are either short (~3s) or long (~10s) and were recorded in three separate sessions, 
on three separate days, with the same participant.

The first two recordings were combined to create a more diverse training dataset. 
The third recording was held out as a test data set.

The final model is used for an online prediction task (liveBruxismPrediction.py)
"""

# SET GLOBAL PARAMETERS
np.random.seed(42) # Ensure reproducible classification results
time_interval = "1S" # Epoch duration (here 1 second)

# Recording file paths
training_path = "training_data_cut.csv"
validation_path = "validation_data_cut.csv"
test_path = "test_data_cut.csv"

# HELPER FUNCTIONS FOR DATA PREPARATION
def data_loading(path):
    """Load and prepare labels for the experiment recordings."""

    # Load the data from file
    df = pd.read_csv("data/" + path, header=0, low_memory=False)

    # Re-label
    # Convert experiment phases (to numeric IDs)
    df["LABEL"] = 0
    df.EVENT=df.EVENT.astype(int)
    classes = np.unique(df.PHASEID)
    for i in range(1, len(classes)):
        df.loc[(df['PHASEID'].isin([classes[i]]))&(df["EVENT"] == 1), "LABEL"] = i

    # Epoch the data and set epoch to contain a particular event when >50% of the epoch contain a 1 as label
    df.index=pd.to_datetime(df['TimestampMilliPOSX'])
    y = df['LABEL'].resample(time_interval).agg(prpr.majority_labeling)
    df.drop(["TimestampMilliPOSX",'PHASEID',"EVENT"],axis=1, inplace = True)

    # Separate predictors from labels
    X = df.iloc[:, :-1]

    # Return predictors and labels
    return X, y

def binarize_test_data_labels(data):
    """Binarize test data set - identify if bruxing (then = 1) or not (then = 0)"""
    data[~data.isin([14,15])] = 0
    data[data != 0] = 1
    return data

def remove_outliers(X,y):
    """ Remove severe outliers (in predictors and labels)"""
    bool = (np.abs(stats.zscore(X)) < 10).all(axis=1)
    X = X[bool]
    y = y[bool]
    return X,y

def main():
    # LOADING THE DATA
    print("\n--- Load the data ---")
    X_train_raw, y_train_prep = data_loading(training_path)
    X_val_raw, y_val_prep = data_loading(validation_path)
    X_test_raw, y_test_prep = data_loading(test_path)

    ### EXTRACT FEATURES
    print("\n--- Calculate the features ---")
    X_train_prep = prpr.process_and_extract_bruxism_features(X_train_raw, time_interval)
    X_val_prep = prpr.process_and_extract_bruxism_features(X_val_raw, time_interval)
    X_test_prep = prpr.process_and_extract_bruxism_features(X_test_raw, time_interval)

    ### FURTHER PRE-PROCESSING
    # Remove missing entries
    X_train_prep.fillna(0,inplace=True)
    y_train_prep.fillna(0,inplace=True)
    X_val_prep.fillna(0,inplace=True)
    y_val_prep.fillna(0,inplace=True)
    X_test_prep.fillna(0,inplace=True)
    y_test_prep.fillna(0,inplace=True)

    # Join the two initial recordings (training and validation set)
    X = [X_train_prep, X_val_prep]
    y = [y_train_prep,y_val_prep]
    X = pd.concat(X)
    y = pd.concat(y)

    # Prepare binary prediction labels for test data set (clenching or not)
    y_test_prep = binarize_test_data_labels(y_test_prep)

    ### MODEL DEVELOPMENT
    # Set up the classifier & evaluation approach (5-fold CV)
    clf = AdaBoostClassifier()
    cv = StratifiedKFold(n_splits=5)

    # Store evaluation metrics for each fold
    f1_list = []
    scores_rec = []
    scores_prec = []
    scores_cm = []

    # Run the cross validation
    for train_fold_index, val_fold_index in cv.split(X, y):
        # Separate training and validation set
        X_train_fold, y_train_fold = X.iloc[train_fold_index], y.iloc[train_fold_index]
        X_val_fold, y_val_fold = X.iloc[val_fold_index], y.iloc[val_fold_index]

        # Re-create binary labels
        y_train_fold = binarize_test_data_labels(y_train_fold)
        y_val_fold= binarize_test_data_labels(y_val_fold)

        # Use oversampling to balance class distributions
        oversample = SMOTE(random_state=42)
        X_train_upsample, y_train_upsample = oversample.fit_resample(X_train_fold, y_train_fold)

        # Scale the features (z-Standardization)
        scaler = StandardScaler()
        X_train_upsample_t = scaler.fit_transform(X_train_upsample)
        X_val_t = scaler.transform(X_val_fold)

        # Fit the classifier model
        model = clf.fit(X_train_upsample_t,y_train_upsample)
        # Predict the labels of the validation set
        y_pred_fold = model.predict(X_val_t)

        # Collect various performance metrics
        f1_list.append(f1_score(y_val_fold, y_pred_fold))
        scores_rec.append(recall_score(y_val_fold, y_pred_fold))
        scores_prec.append(precision_score(y_val_fold, y_pred_fold))
        scores_cm.append(confusion_matrix(y_val_fold, y_pred_fold))

    # REPORT TRAINING PERFORMANCE
    print("\n--- Averaged CV Results ---")
    print(np.mean(f1_list))
    print(np.mean(scores_rec))
    print(np.mean(scores_prec))
    print(np.mean(scores_cm,axis = 0))

    # FINAL MODEL EVALUATION
    print("\n--- Prediction on Test Data ---")

    # Repeat the previous stages, but now for the so far unseen test data set.
    # Oversampling
    oversample = SMOTE(random_state=42)
    X, y = oversample.fit_resample(X, y)
    y = binarize_test_data_labels(y)

    # Feature scaling
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    X_test_t = scaler.transform(X_test_prep)

    # Model fitting
    model = clf.fit(X, y)
    y_pred_test = model.predict(X_test_t)

    # Report final performance metrics
    print(confusion_matrix(y_test_prep, y_pred_test))
    print(f1_score(y_test_prep, y_pred_test))
    print(recall_score(y_test_prep,y_pred_test))
    print(precision_score(y_test_prep,y_pred_test))

    # Export the final objects that are needed for an online prediction application
    print("\n--- Save final scaler & model ---")

    filename = 'classification_model.sav'
    pickle.dump(clf, open(filename, 'wb'))

    filename = 'feature_scaler.sav'
    pickle.dump(scaler, open(filename, 'wb'))

    print("\n--- Classifier development finished ---")

if __name__ == '__main__':
    main()