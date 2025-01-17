#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Run Observation
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import osmosdr
import time




class run_observation(gr.top_block):

    def __init__(self, bandwidth=2e6, bb_gain=20, channels=1024, dev_args='', duration=60, frequency=1420e6, if_gain=20, obs_file='observation.dat', raw_file='raw.dat', rf_gain=30, t_sample=1):
        gr.top_block.__init__(self, "Run Observation", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.bandwidth = bandwidth
        self.bb_gain = bb_gain
        self.channels = channels
        self.dev_args = dev_args
        self.duration = duration
        self.frequency = frequency
        self.if_gain = if_gain
        self.obs_file = obs_file
        self.raw_file = raw_file
        self.rf_gain = rf_gain
        self.t_sample = t_sample

        ##################################################
        # Variables
        ##################################################
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/channels)
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.custom_window = custom_window = sinc*np.hamming(4*channels)

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + dev_args
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(bandwidth)
        self.osmosdr_source_0.set_center_freq(frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.fft_vxx_0 = fft.fft_vcc(channels, True, window.blackmanharris(channels), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, channels)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(int(t_sample*bandwidth/channels), channels)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(duration*bandwidth))
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, raw_file, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*channels, obs_file, True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(channels)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_head_0, 0))


    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.blocks_head_0.set_length(int(self.duration*self.bandwidth))
        self.osmosdr_source_0.set_sample_rate(self.bandwidth)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_channels(self):
        return self.channels

    def set_channels(self, channels):
        self.channels = channels
        self.set_custom_window(self.sinc*np.hamming(4*self.channels))
        self.set_sinc_sample_locations(np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.channels))

    def get_dev_args(self):
        return self.dev_args

    def set_dev_args(self, dev_args):
        self.dev_args = dev_args

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration
        self.blocks_head_0.set_length(int(self.duration*self.bandwidth))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_source_0.set_center_freq(self.frequency, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_obs_file(self):
        return self.obs_file

    def set_obs_file(self, obs_file):
        self.obs_file = obs_file
        self.blocks_file_sink_0.open(self.obs_file)

    def get_raw_file(self):
        return self.raw_file

    def set_raw_file(self, raw_file):
        self.raw_file = raw_file
        self.blocks_file_sink_1.open(self.raw_file)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_t_sample(self):
        return self.t_sample

    def set_t_sample(self, t_sample):
        self.t_sample = t_sample

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_custom_window(self.sinc*np.hamming(4*self.channels))
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--bandwidth", dest="bandwidth", type=eng_float, default=eng_notation.num_to_str(float(2e6)),
        help="Set bandwidth [default=%(default)r]")
    parser.add_argument(
        "--bb-gain", dest="bb_gain", type=eng_float, default=eng_notation.num_to_str(float(20)),
        help="Set bb_gain [default=%(default)r]")
    parser.add_argument(
        "--channels", dest="channels", type=intx, default=1024,
        help="Set channels [default=%(default)r]")
    parser.add_argument(
        "--dev-args", dest="dev_args", type=str, default='',
        help="Set dev_args [default=%(default)r]")
    parser.add_argument(
        "--duration", dest="duration", type=eng_float, default=eng_notation.num_to_str(float(60)),
        help="Set duration [default=%(default)r]")
    parser.add_argument(
        "--frequency", dest="frequency", type=eng_float, default=eng_notation.num_to_str(float(1420e6)),
        help="Set frequency [default=%(default)r]")
    parser.add_argument(
        "--if-gain", dest="if_gain", type=eng_float, default=eng_notation.num_to_str(float(20)),
        help="Set if_gain [default=%(default)r]")
    parser.add_argument(
        "--obs-file", dest="obs_file", type=str, default='observation.dat',
        help="Set obs_file [default=%(default)r]")
    parser.add_argument(
        "--raw-file", dest="raw_file", type=str, default='raw.dat',
        help="Set raw_file [default=%(default)r]")
    parser.add_argument(
        "--rf-gain", dest="rf_gain", type=eng_float, default=eng_notation.num_to_str(float(30)),
        help="Set rf_gain [default=%(default)r]")
    parser.add_argument(
        "--t-sample", dest="t_sample", type=intx, default=1,
        help="Set t_sample [default=%(default)r]")
    return parser


def main(top_block_cls=run_observation, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(bandwidth=options.bandwidth, bb_gain=options.bb_gain, channels=options.channels, dev_args=options.dev_args, duration=options.duration, frequency=options.frequency, if_gain=options.if_gain, obs_file=options.obs_file, raw_file=options.raw_file, rf_gain=options.rf_gain, t_sample=options.t_sample)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
