import random
import os
from clear import clear

def chaff():
    clear()
    characters = [b"0", b"1", b"2", b"3", b"4", b"5", b"6", b"7", b"8", b"9", b"A", b"B", b"C", b"D", b"E", b"F"]

    print("CREATING CHAFF")
    try:
        with open("CHAFF", "wb") as file:
            while True:
                code = random.choice(characters)
                file.write(code)

    except:
        pass

    print("REMOVING CHAFF")
    os.remove("CHAFF")
    print("DONE!")
    
if __name__ == "__main__":
    chaff()
