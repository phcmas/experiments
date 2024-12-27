import pickle
import time

import msgpack
import msgpack_numpy as m
import numpy as np

json0 = {
    0: np.random.rand(80, 4),
    "base1": np.random.rand(80, 4),
    "base2": np.random.rand(80, 4),
    "base3": np.random.rand(80, 4),
}

bin0 = msgpack.packb(json0, default=m.encode)
res0 = msgpack.unpackb(bin0, object_hook=m.decode, strict_map_key=False)

base = np.random.rand(80, 4)

test0 = base.astype(np.float32)
test1 = base.astype(np.float64)
test2 = base.astype(np.int8)
test3 = base.astype(np.uint8)

byte0 = test0.tobytes()
byte1 = test1.tobytes()
byte2 = test2.tobytes()
byte3 = test3.tobytes()

pbyte0 = pickle.dumps(test0)
pbyte1 = pickle.dumps(test1)
pbyte2 = pickle.dumps(test2)
pbyte3 = pickle.dumps(test2)

mbyte0 = msgpack.packb(test0, default=m.encode)
mbyte1 = msgpack.packb(test1, default=m.encode)
mbyte2 = msgpack.packb(test2, default=m.encode)
mbyte3 = msgpack.packb(test3, default=m.encode)

print(len(byte0), len(byte1), len(byte2), len(byte3))
print(len(pbyte0), len(pbyte1), len(pbyte2), len(pbyte3))
print(len(mbyte0), len(mbyte1), len(mbyte2), len(mbyte3))

start = time.perf_counter()
base = {i: np.random.rand(40, 4) for i in range(700)}

byte = msgpack.packb(base, default=m.encode)
arr = msgpack.unpackb(byte, object_hook=m.decode, strict_map_key=False)
end = time.perf_counter()

print(f"duration: {end - start}")

start = time.perf_counter()
byte = test0.tobytes()
arr = np.frombuffer(byte, dtype=np.float32).reshape((80, 4))
end = time.perf_counter()

print(f"duration: {end - start}")


start = time.perf_counter()
byte = pickle.dumps(test0)
arr = pickle.loads(byte)

print(f"type: {type(arr)}")
end = time.perf_counter()

print(f"duration: {end - start}")
