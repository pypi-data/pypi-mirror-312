import json
import base64
import os
import numpy as np


NUMPY_TO_BYTES_MAP = {
    np.float16: ('float16', '<f2'),
    np.float32: ('float32', '<f4'),
    np.float64: ('float64', '<f8'),
    np.int32: ('int32', '<i4'),
    np.int64: ('int64', '<i8')
}

TYPE_TO_FORMAT_MAP = {
    'float16': '<f2',
    'float32': '<f4',
    'float64': '<f8',
    'int32': '<i4',
    'int64': '<i8'
}


def numpy_encoder(obj):
    if isinstance(obj, np.ndarray):
        if obj.dtype.type in NUMPY_TO_BYTES_MAP:
            data_type, byte_format = NUMPY_TO_BYTES_MAP[obj.dtype.type]
            byte_data = obj.astype(byte_format).tobytes()
        else:
            raise TypeError(f"Unsupported dtype: {obj.dtype}")

        encoded_data = base64.b64encode(byte_data).decode('utf-8')
        result = {
            '_elementType': data_type,
            '_shape': obj.shape,
            '_data': encoded_data
        }
        return result
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def numpy_decoder(dct):
    if '_elementType' in dct and '_data' in dct:
        data_type = dct['_elementType']
        shape = dct.get('_shape', None)
        data = base64.b64decode(dct['_data'])

        if data_type in TYPE_TO_FORMAT_MAP:
            array = np.frombuffer(data, dtype=TYPE_TO_FORMAT_MAP[data_type])
        else:
            raise TypeError(f"Unsupported element type: {data_type}")

        if shape:
            array = array.reshape(shape)
        return array
    return dct


def execute(**kwargs):
    rd, wd = 3, 4  # the read and write pipe indexes
    with os.fdopen(rd, "rb") as rf:
        os.write(wd, "ready".encode())
        while True:
            to_read = int.from_bytes(rf.read(4), "big")
            func_name_bytes = rf.read(to_read)
            func_name = func_name_bytes.decode()
            to_read = int.from_bytes(rf.read(4), "big")
            func_input = json.loads(rf.read(to_read), object_hook=numpy_decoder)
            result = kwargs[func_name](func_input)
            msg_to_write = json.dumps(result, default=numpy_encoder).encode()
            x = int.to_bytes(len(msg_to_write), 4, "big")
            os.write(wd, x)
            os.write(wd, msg_to_write)