import os
import io

c = 0
with open("inside.jpg", "rb") as image:
    bs = image.read()
    for b in bs:
        if c < 996:
            print(hex(b), end= ",")
            c += 1

    print("\n\n", len(bs))