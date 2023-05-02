import argparse
import logging
import numpy as np
import pygame
import pandas as pd
import pyqtgraph as pg
from PIL import Image
from pyqtgraph.Qt import QtGui, QtCore
import preprocessing as prpr
import sklearn
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations

"""
This is a demonstrator for a live jaw clenching detector.
The code is primarily borrowed from the BrainFlow live streeam example:
https://brainflow.readthedocs.io/en/stable/Examples.html#python-real-time-plot

We have adapted:
 - the data processing of incoming epochs
 - the feature extraction
 - the scaling and prediction of epochs via a pre-trained classifier
"""

class Graph:
    """Sets up a graphical interface to display the incoming data and prediction results."""

    def __init__(self, board_shim):
        """Initialize the PyQt graphical interface."""

        # Store the operational parameters in the Graph object.
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 1000 # frequency for grabbing samples form the board and updating the GUI
        self.window_size_sec = 1 # epoch size in seconds.
        self.num_points = self.window_size_sec * self.sampling_rate # nr. of samples to get from the board on each update
        self.prediction_update_after_n_updates = 1000 / self.update_speed_ms
        self.prediction_state = 0  # 0 = Rest; 1 = Brux

        # Init the GUI Window
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title='Bruxism Live Prediction Demo',size=(950, 1200))

        # Load the prediction images
        self.label_brux = pg.ImageItem(np.flipud(np.array(Image.open('res/img/label_brux.png'))).transpose([1, 0, 2]))
        self.label_rest = pg.ImageItem(np.flipud(np.array(Image.open('res/img/label_rest.png'))).transpose([1, 0, 2]))

        # Add main display components to the GUI
        self._init_timeseries()
        self._init_prediction_report()

        # Load the audio file to be played when jaw clenching/bruxing events are detected
        pygame.init()
        self.sound = pygame.mixer.Sound('res/audio/PUNCH.mp3')

        # Load the pre-trained scaler & model
        self.model = pd.read_pickle('classification_model.sav') # Currently, this is an AdaBoost model (requires sklearn)
        self.scaler = pd.read_pickle('feature_scaler.sav') # Currently, this is an StandardScaler (requires sklearn)

        # Define the channel names (this might vary for your setup)
        # - Here it is important to make sure the same elecs were used for the classifier
        self.elec_names = ['CH01.R1', 'CH02.R2', 'CH03.R8', 'CH04.R4', 'CH05.R5', 'CH06.R7', 'CH07.R9', 'CH08.R10',
                           'CH09.L1', 'CH10.L2', 'CH11.L8', 'CH12.L4', 'CH13.L5', 'CH14.L7', 'CH15.L9', 'CH16.L10']

        # Connect the update method (see below) to a timer that keeps updating the application.
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()

    def _init_timeseries(self):
        """Add rows that show the signal traces of each channel."""
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.win.addPlot(row=i,col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            if i == 0:
                p.setTitle('EXG Data')
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)

    def _init_prediction_report(self):
        """Add a row that shows the current classification result as a text message."""

        # Add label
        self.win.addItem(pg.LabelItem("Prediction"), row=len(self.exg_channels)+1,col=0)
        # Add image with prediction result
        self.prediction_img = self.win.addViewBox(row=len(self.exg_channels)+2,col=0)
        self.prediction_img.addItem(self.label_rest)

    def update(self):
        """Process a single epoch of data and update the GUI display with the results."""

        # Get latest n packages or less, doesnt remove them from internal buffer
        data = self.board_shim.get_current_board_data(self.num_points) # These data are displayed.

        # Convert the data sample to a DataFrame containing only the signal channels
        # This is a preparatory step for pre-processing the data for the clenching/bruxism prediction
        raw = pd.DataFrame(np.transpose(data[self.exg_channels]), columns=self.elec_names)

        # Filter the last epoch for display of the signal traces.
        for count, channel in enumerate(self.exg_channels):
            # Mean-center the data
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            # Apply a high-pass filter
            DataFilter.perform_highpass(data[channel], self.sampling_rate, 5.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            # Apply a notch filter
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 50.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            # Update the GUI
            self.curves[count].setData(data[channel].tolist())

        # Pre-process the epoch and make a prediction
        # Include TS index (to re-use the pre-processing code from the classifier training)
        raw['TimestampMilliPOSX'] = pd.Timestamp.now()
        raw.index = raw['TimestampMilliPOSX']
        raw.drop("TimestampMilliPOSX", axis=1, inplace=True)

        # Preprocess the data
        features = prpr.process_and_extract_bruxism_features(raw, '1S', self.sampling_rate)

        # Scale the features
        features = self.scaler.transform(features)

        # Make a prediction
        prediction = self.model.predict(features)
        print(prediction)

        # If a change in prediction is detected, update the GUI (show different image and play sound)
        if prediction == 1 and self.prediction_state == 0:
            self.prediction_state = 1
            self.prediction_img.removeItem(self.label_rest)
            self.prediction_img.addItem(self.label_brux)
            self.sound.play()
        elif prediction == 0 and self.prediction_state == 1:
            self.prediction_state = 0
            self.prediction_img.removeItem(self.label_brux)
            self.prediction_img.addItem(self.label_rest)

        self.app.processEvents()

def main():
    """Initializes the EEG board (synthetic or real) and starts the main application thread."""

    # Setting up the BrainFlow board object parameters
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    # Use the BrainFlow docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    # See: https://brainflow.readthedocs.io/en/stable/SupportedBoards.html#openbci
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=BoardIds.SYNTHETIC_BOARD)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    args = parser.parse_args()

    # Specify which type of board is used
    # Setup for OpenBCI Cyton on Windows - Adjust the COM port that the USB dongle is connected to
    args = parser.parse_args(['--serial-port', 'COM6', '--board-id', '-1'])  # Set board to -1 for synthetic data; 2 for cyton+daisy

    # Setup for OpenBCI Cyton on MacOS - Adjust the COM port that the USB dongle is connected to
    # The '/dev/cu.' path must be included - see: https://brainflow.readthedocs.io/en/stable/SupportedBoards.html#cyton-daisy
    # args = parser.parse_args(['--serial-port', '/dev/cu.usbserial-DM02586I', '--board-id', '2'])  # Set board to -1 for synthetic data; 2 for cyton+daisy

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    # Create the board object and start the session
    try:
        board_shim = BoardShim(args.board_id, params)
        board_shim.prepare_session()
        board_shim.start_stream(450000, args.streamer_params)
        g = Graph(board_shim)
    except BaseException as e:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()

if __name__ == '__main__':
    main()