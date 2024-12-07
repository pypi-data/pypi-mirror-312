import numpy as np

def read_array_from_gputils_binary_file(path, dt='d'):
    with open(path, 'rb') as f:
        nr = int.from_bytes(f.read(8), byteorder='little', signed=False)
        nc = int.from_bytes(f.read(8), byteorder='little', signed=False)
        nm = int.from_bytes(f.read(8), byteorder='little', signed=False)
        dat = np.fromfile(f, dtype=np.dtype(dt))
        dat = dat.reshape((nr, nc, nm))
    return dat


def write_array_to_gputils_binary_file(x, path):
    x_shape = x.shape
    x_dims = len(x_shape)
    if x_dims >= 4:
        raise Exception("given array cannot have more than 3 dimensions")
    nr = x_shape[0]
    nc = x_shape[1] if x_dims >= 2 else 1
    nm = x_shape[2] if x_dims == 3 else 1
    with open(path, 'wb') as f:
        f.write(nr.to_bytes(8, 'little'))
        f.write(nc.to_bytes(8, 'little'))
        f.write(nm.to_bytes(8, 'little'))
        x.tofile(f)