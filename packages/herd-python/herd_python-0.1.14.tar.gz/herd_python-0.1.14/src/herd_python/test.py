from herd_python import *

herd = HerdClient(port=7878, cert_path="../../certs")
herd.set("0", "Hello, World!")