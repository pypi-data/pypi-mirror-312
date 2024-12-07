from client import HerdClient

herd = HerdClient(port=7878)
herd.set("0", "Hello, World!")