import unittest

import logging

import os
import sys
import glob

import numpy as np
import soundfile

# sys.path.append(os.path.dirname(__file__)+'/../..')
import phoneshift
import phoneshift.tests.utils as utils

class TestModule(unittest.TestCase):

    def test_nothing(self):
        pass

    # def test_transform_resynth(self):
    #     for fpath_in in utils.filepaths_to_process():
    #         # print(f'INFO: Testing {fpath_in} ...')
    #         wav, fs = soundfile.read(fpath_in, dtype='float32')

    #         syn = phoneshift.transform(wav, fs)

    #         self.assertFalse(np.isinf(syn).any())
    #         self.assertFalse(np.isnan(syn).any())
    #         self.assertTrue(self.assert_diff_maxabs_bounded(wav, syn, phoneshift.db2lin(-57.0)))

    # def test_transform_smoke(self):
    #     for fpath_in in self.filepaths_to_process():
    #         wav, fs = soundfile.read(fpath_in, dtype='float32')
    #         for first_frame_at_t0 in [True, False]:
    #             for timestep in [int(fs*0.01), int(fs*0.05)]:
    #                 for winlen_inner in [int(fs*0.10), int(fs*0.20)]:
    #                     syn = phoneshift.transform(wav, fs, first_frame_at_t0=first_frame_at_t0, timestep=timestep, winlen_inner=winlen_inner)

    # def test_transform_pitch_scaling_smoke(self):
    #     for fpath_in in self.filepaths_to_process():
    #         bbasename = os.path.splitext(os.path.basename(fpath_in))[0]
    #         wav, fs = soundfile.read(fpath_in, dtype='float32')

    #         for psf in [0.5, 0.75, 1.0, 1.5, 2.0]:
    #             for psf_max in [1.0, 1.5, 2.0]:
    #                 syn = phoneshift.transform(wav, fs, psf=psf, psf_max=psf_max)
    #                 self.assertFalse(np.isinf(syn).any())
    #                 self.assertFalse(np.isnan(syn).any())

    # def test_transform_time_scaling_smoke(self):
    #     for fpath_in in self.filepaths_to_process():
    #         bbasename = os.path.splitext(os.path.basename(fpath_in))[0]
    #         wav, fs = soundfile.read(fpath_in, dtype='float32')

    #         for tsf in [-0.75, 0, 0.75]:
    #             for ts_bdi in [0.0, 0.1]:
    #                 for ts_bdt in [0.0, 0.1]:
    #                     for ts_ffb in [0.0, 0.1]:
    #                         for ts_bdm in [0.0, 2.0]:
    #                             syn = phoneshift.transform(wav, fs, tsf=tsf, ts_bdi=ts_bdi, ts_ffb=0.0, ts_bdt=ts_bdt, ts_bdm=ts_bdm)
    #                             self.assertFalse(np.isinf(syn).any())
    #                             self.assertFalse(np.isnan(syn).any())

    #         for ts_skip_start in [True, False]:
    #             syn = phoneshift.transform(wav, fs, ts_bdi=0.1, ts_skip_start=ts_skip_start)
    #             self.assertFalse(np.isinf(syn).any())
    #             self.assertFalse(np.isnan(syn).any())

if __name__ == '__main__':
    unittest.main()
