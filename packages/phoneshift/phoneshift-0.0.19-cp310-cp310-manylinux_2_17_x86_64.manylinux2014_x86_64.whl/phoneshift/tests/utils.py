import logging

import os
import sys
import glob

import numpy as np
import soundfile

import phoneshift

def assert_diff_maxabs_bounded(ref, test, threshold=phoneshift.float32.eps):
    assert ref.shape == test.shape

    diff = ref - test
    diff_idx = np.where(abs(diff)>threshold)[0]
    if len(diff_idx)>0:
        for n in diff_idx:
            logging.error(f'ref[{n}]={ref[n]} test[{n}]={test[n]} err={diff[n]} ({phoneshift.lin2db(diff[n])}dB) > {threshold} ({phoneshift.lin2db(threshold)}dB)')

        return False

    return True

def filepaths_to_process():
    fpaths = glob.glob(f"{os.path.dirname(__file__)}/test_data/wav/*.wav")
    assert len(fpaths) > 0
    return fpaths


# def dir_refs(self):
#     return '../phoneshift/sdk_python3/test_data/refs'

# def dir_output(self):
#     return 'test_data/sdk_python3'
