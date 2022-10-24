# Imports

import os, platform, struct, sys
from time import sleep
from datetime import datetime

now = datetime.now()

# Classes and Exceptions

class UnsupportedError(Exception):
    pass

class InvalidCardError(Exception):
    pass

class InvalidResponseError(Exception):
    def __init__(self,response,message='''isn't a valid option! Expected "y", "n", or nothing.'''):
        self.response = response
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''"{self.response}" {self.message}''' 

class c:
    r = '\033[91m'
    o = '\033[38;5;203m'
    y = '\033[93m'
    g = '\033[92m'
    c = '\033[96m'
    b = '\033[94m'
    p = '\033[35m'
    m = '\033[95m'
    e = '\033[0m'

    def disable(self):
        self.r = ''
        self.y = ''
        self.g = ''
        self.c = ''
        self.b = ''
        self.p = ''
        self.m = ''
        self.e = ''

# System check

System = platform.system()

def MakeDirChoice(Path):
    while True:
        try:
            MakeDirectory = input(f"{c.y}Would you like to create it now?{c.b} [Y/n] {c.e}")
            if MakeDirectory.lower().strip() in ('y',''):
                print(f"{c.g}Creating Bankers.py directory...{c.e}")
                os.makedirs(Path)
                print(f"{c.c}Done!{c.e}")
                SavingDisabled = False
                return SavingDisabled
            elif MakeDirectory.lower().strip() == 'n':
                try:
                    Confirm = input(f'{c.r}Are you sure?{c.e} Not creating the directory will result in saving being disabled.{c.b} [Y/n] {c.e}')
                    if Confirm.lower().strip() in ('y',''):
                        SavingDisabled = True
                        return SavingDisabled
                    elif Confirm.lower().strip() == 'n':
                        pass
                    else:
                        raise InvalidResponseError(Confirm.lower().strip())
                except InvalidResponseError as e:
                    print(str(e.response) + " " + str(e))
                    continue
            else:
                raise InvalidResponseError(MakeDirectory.lower().strip())
        except InvalidResponseError as e:
            print(str(e.response) + " " + str(e))
            continue

try:
    if System == "Windows":
        GamePath = os.getenv('HOME') + "\\Bankers.py"
        if not os.path.exists(GamePath):
            print(f"{c.y}[ATTN]:{c.e} No Bankers.py directory found!")
            CanSave = MakeDirChoice(GamePath)
    elif System == "Linux":
        GamePath = os.getenv('HOME') + "/Bankers.py"
        if not os.path.exists(GamePath):
            print(f"{c.y}[ATTN]:{c.e} No Bankers.py directory found!")
            CanSave = MakeDirChoice(GamePath)
    else:
        raise UnsupportedError
except UnsupportedError:
    print("[FATAL]: This OS isn't currently supported by Bankers.py!")
    print("We're trying hard to get this compatible with every OS we can,")
    print("so stick with us and we'll update you!")
    exit()

# Data and Save/load

CurrentGameData = {
    'GameInProgress': False,
    'CurrentHand': [],
    'HouseCard': None,
    'Wallet': 1000,
    'Deck': ["🂡","🂱","🃁","🃑","🂢","🂲","🃂","🃒","🂣","🂳","🃃","🃓","🂤","🂴","🃄","🃔","🂥","🂵","🃅","🃕","🂦","🂶","🃆","🃖","🂧","🂷","🃇","🃗","🂨","🂸","🃈","🃘","🂩","🂹","🃉","🃙","🂪","🂺","🃊","🃚","🂫","🂻","🃋","🃛","🂭","🂽","🃍","🃝","🂮","🂾","🃎","🃞"],
    'WalletType': "Standard",
    'PlayerHandMax': 2,
    'HouseHandMax': 1
}

def SaveGame():
    if not CanSave:
        print(f'{c.r}[ATTN]:{c.e} No Bankers.py directory was found. Saving has been disabled.')
    else:
        print(f'{c.g}Saving data...{c.e}')
        try:
            with open(GamePath + 'save.dat', 'wb') as DataFile:
                DataFile.write(struct.pack('i'*len(CurrentGameData), *CurrentGameData))
            print(f'{c.c}Success!{c.e}')
        except:
            print(f'{c.r}[FATAL]:{c.e} Something went wrong when saving! To avoid more problems, Bankers.py will now quit.')
        finally:
            DataFile.close
            exit()

def LoadGame():
    if (not CanSave) or (not os.path.exists(GamePath + 'save.dat')):
        print(f"{c.r}[ATTN]:{c.e} No Bankers.py directory was found, or there's no save data to load.")
    else:
        try:
            with open(GamePath + 'save.dat', 'rb') as DataFile:
                values = struct.unpack('i'*len(CurrentGameData), DataFile.read())
            for i, v in CurrentGameData.items():
                CurrentGameData[i] = v
        except:
            print(f'{c.r}[FATAL]:{c.e} Something went wrong when loading! To avoid more problems, Bankers.py will now quit.')
        finally:
            DataFile.close
            exit()

# Main game


print(f'''╔═══════════════════════════════════════════════════════════╗
║    {c.c}______             _                               {c.e}    ║
║    {c.c}| ___ \           | |                              {c.e}    ║
║    {c.c}| |_/ / __ _ _ __ | | _____ _ __ ___   _ __  _   _ {c.e}    ║
║    {c.c}| ___ \/ _` | '_ \| |/ / _ \ '__/ __| | '_ \| | | |{c.e}    ║
║    {c.c}| |_/ / (_| | | | |   <  __/ |  \__ \_| |_) | |_| |{c.e}    ║
║    {c.c}\____/ \__,_|_| |_|_|\_\___|_|  |___(_) .__/ \__, |{c.e}    ║
║    {c.c}                                      | |     __/ |{c.e}    ║
║    {c.c}                                      |_|    |___/ {c.e}    ║
╚═══════════════════════════════════════════════════════════╝''')
print()
print(f'''{c.y}Welcome to{c.e} Bankers.py{c.y}!{c.e}''')
print()

