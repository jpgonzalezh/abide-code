#!/bin/python3
import os

import nrrd
import nibabel as nb

ROOT = os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    # Define all NRRD files
    nrrd_files = [os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.lower().endswith('.nrrd')]

    for f in nrrd_files:
        readdata, header = nrrd.read(f)
        print(readdata)
        break


