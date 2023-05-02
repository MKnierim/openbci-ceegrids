import numpy as np
import pandas as pd
from mne.filter import filter_data, notch_filter

"""
This code contains the EEG signal processing and feature extraction functions.
These are used identically for the classifier development and the live prediction demo.

"""

# GLOBAL PARAMTERS FOR PRE-PROCESSING
# Determine the minimum length of an epoch before processing it.
minimum_length_epoch = 1


# LABELING FUNCTIONS (DEPENDENT VARIABLES)
def majority_labeling(X, threshold = 0.5):
    """Takes a series or one-dimensional numpy array and returns a single label depending on the distribution of 0s and 1s in the series."""
    if not X.empty and len(X) > minimum_length_epoch:
        weight = np.sum(X)/(len(X)*np.max(X))
        return np.max(X) if weight >= threshold else 0


# SIGNAL PROCESSING FUNCTIONS (SINGLE CHANNEL)
def mean_center(X):
    """Takes a series or one-dimensional numpy array, subtracts its mean and returns the series."""
    X -= np.mean(X)
    return X

def abs_sum(X):
    """Takes a series or one-dimensional numpy array and returns the absolute sum of it."""
    if not X.empty and len(X) > minimum_length_epoch:
        return np.sum(np.abs(X))
    else:
        return np.NaN

def abs_max(X):
    """Takes a series or one-dimensional numpy array and returns the absolute maximum value in it."""
    if not X.empty and len(X) > minimum_length_epoch:
        return np.max(np.abs(X))
    else:
        return np.NaN

def hjorth_activity(X):
    """For a definition and description of the Hjorth paramters see: https://en.wikipedia.org/wiki/Hjorth_parameters"""

    if not X.empty and len(X) > minimum_length_epoch:
        return np.var(X)
    else:
        return np.NaN

def hjorth_complexity(X, D=None):
    """For a definition and description of the Hjorth paramters see: https://en.wikipedia.org/wiki/Hjorth_parameters"""

    if not X.empty and len(X) > minimum_length_epoch:
        X= X.values
        D = np.diff(X)

        D = np.array(D)
        n = len(X)

        M2 = float(np.sum(D ** 2)) / n
        TP = sum(np.array(X) ** 2)
        M4 = 0
        for i in range(1, len(D)):
            M4 += (D[i] - D[i - 1]) ** 2
        M4 = M4 / n

        return np.sqrt(
            np.multiply(float(M4),np.divide(TP,np.multiply(M2,M2)))
        )
    else:
        return np.NaN

def hjorth_mobility(X):
    """For a definition and description of the Hjorth paramters see: https://en.wikipedia.org/wiki/Hjorth_parameters"""

    if not X.empty and len(X) > minimum_length_epoch:
        D = np.diff(X)
        n = len(X)
        M2 = float(np.sum(D ** 2)) / n
        TP = sum(np.array(X) ** 2)
        return np.sqrt(M2 / TP)
    else:
        return np.NaN

def hfd(X, Kmax=6):
    """Takes a series or one-dimensional numpy array and computes the Higuchi Fractal dimension - see https://en.wikipedia.org/wiki/Higuchi_dimension."""

    if not X.empty and len(X) > minimum_length_epoch:
        X = X.values
        L = []
        x = []
        N = len(X)
        for k in range(1, Kmax):
            Lk = []
            for m in range(0, k):
                Lmk = 0
                for i in range(1, int(np.floor((N - m) / k))):
                    Lmk += abs(X[m + i * k] - X[m + i * k - k])
                Lmk = Lmk * (N - 1) / np.floor((N - m) / float(k)) / k
                Lk.append(Lmk)
            L.append(np.log(np.mean(Lk)))
            x.append([np.log(float(1) / k), 1])
        (p, _, _, _) = np.linalg.lstsq(x, L, rcond=None)
        return p[0]
    else:
        return np.NaN

def pfd(X, D=None):
    """Takes a series or one-dimensional numpy array and computes the Petrosian Fractal dimension - A. Petrosian, Kolmogorov complexity of finite sequences and recognition of different preictal EEG patterns, in Proceedings of the Eighth IEEE Symposium on Computer-Based Medical Systems, 1995, pp. 212-217."""

    if not X.empty and len(X) > minimum_length_epoch:

        if D is None:
            D = np.diff(X)
            D = D.tolist()
        N_delta = 0  # number of sign changes in derivative of the signal
        for i in range(1, len(D)):
            if D[i] * D[i - 1] < 0:
                N_delta += 1
        n = len(X)
        return np.log10(n) / (
                np.log10(n) + np.log10(n / n + 0.4 * N_delta)
        )
    else:
        return np.NaN


# SIGNAL PROCESSING AUTOMATION (BATCH - ALL CHANNELS)
def preprocess_channel(signal_df, fs=125):
    """Takes a a series or one-dimensional numpy array of a single-channel EEG signal and returns the series after completing several pre-processing steps."""

    # Subtract the mean
    signal_df = mean_center(signal_df.to_numpy())

    # Apply a bandpass filter
    signal_df = filter_data(signal_df, sfreq=fs, l_freq=5, h_freq=62, method='iir', copy=True, verbose='WARNING')

    # Apply notch filters (to remove possible line noise)
    signal_df = notch_filter(signal_df, Fs=fs, freqs=50, method='iir', copy=False, verbose='WARNING')

    return signal_df

def extract_features(signal_df, time_interval):
    """Takes a DataFrame of only signal data columns and returns a summarised DataFrame (single row) of computed features for each channel."""

    # Retain the channel names
    channel_names = signal_df.columns

    # Extract absolute amplitude maxima and sums
    abs_mx = signal_df.resample(time_interval).apply(abs_max)
    abs_mx.columns = [str(n) + '_max' for n in channel_names]
    abs_sm = signal_df.resample(time_interval).apply(abs_sum)
    abs_sm.columns = [str(n) + '_sum' for n in channel_names]

    # Extract hjorth paramteres
    hj_ac = signal_df.resample(time_interval).apply(hjorth_activity)
    hj_ac.columns = [str(n)+'_activity' for n in channel_names]
    hj_co = signal_df.resample(time_interval).apply(hjorth_complexity)
    hj_co.columns = [str(n)+'_hjorth_complexity' for n in channel_names]
    hj_mo = signal_df.resample(time_interval).apply(hjorth_mobility)
    hj_mo.columns = [str(n) + '_hjorth_mobility' for n in channel_names]

    # Extract fractal dimensions
    h_fd = signal_df.resample(time_interval).apply(hfd)
    h_fd.columns = [str(n)+'_hfd' for n in channel_names]
    p_fd = signal_df.resample(time_interval).apply(pfd)
    p_fd.columns = [str(n)+'_pfd' for n in channel_names]

    # Return the joined features
    features_df = pd.concat([abs_mx, abs_sm, hj_ac, hj_co, hj_mo, h_fd, p_fd], axis=1)
    return features_df

def process_and_extract_bruxism_features(signal_df, time_interval, fs = 125):
    """Helper function that takes a DataFrame of raw signal data and returns extracted features."""

    processed_values = signal_df.resample(time_interval).transform(preprocess_channel, fs=fs)
    return extract_features(processed_values, time_interval)