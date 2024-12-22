import socket
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return

        data.extend(packet)

    return data


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (np.abs(x1 - x2) ** 2 + np.abs(y1 - y2) ** 2) ** 0.5


host = "84.237.21.36"
port = 5152

plt.figure()
plt.ion()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    i = 0
    delay = 0.5
    ans = ""

    while beat != b"yep":
        i += 1

        sock.send(b"get")
        bts = recvall(sock, 40_002)

        image = np.frombuffer(
            bts[2:],
            dtype="uint8").reshape(bts[0], bts[1])

        img_max = np.max(image)

        binary = image.copy()
        binary[image < img_max * 0.7] = 0
        binary[image >= img_max * 0.7] = 1
        labeled = label(binary)

        points = regionprops(labeled)
        if len(points) != 2:
            continue
        else:
            pos1 = points[0].centroid
            pos2 = points[1].centroid
            d = distance(pos1, pos2)
            d = round(d, 1)

            sock.send(f"{d}".encode())
            answer = sock.recv(6)
            if answer:
                ans = "correct"
            else:
                ans = "wrong"

            print(f"{i}) {d} - {ans}")

            plt.clf()
            plt.title(f"{i}) d = {d}, answer = {answer}")
            plt.subplot(1, 3, 1)
            plt.imshow(image)
            plt.subplot(1, 3, 2)
            plt.imshow(binary)
            plt.subplot(1, 3, 3)
            plt.imshow(labeled)
            plt.pause(delay)

        sock.send(b"beat")
        beat = sock.recv(6)

