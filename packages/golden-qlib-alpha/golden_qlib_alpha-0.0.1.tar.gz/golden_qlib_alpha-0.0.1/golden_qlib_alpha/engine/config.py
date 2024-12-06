from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.joinpath("data")

DATA_DIR_HDF5 = DATA_DIR.joinpath('hdf5')
DATA_DIR_HDF5_ALL = DATA_DIR_HDF5.joinpath('all.h5')


dirs = [DATA_DIR]
for dir in dirs:
    dir.mkdir(exist_ok=True, parents=True)


