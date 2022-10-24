# Imports

import os, platform, struct, sys
from time import sleep
from datetime import datetime
from math import inf as infinity
from random import randint

now = datetime.now()

# Classes and Exceptions

class UnsupportedError(Exception):
    pass

class InvalidCardError(Exception):
    pass

class InvalidAffirmativeError(Exception):
    def __init__(self,response,message='''isn't a valid option! Expected "y", "n", or nothing.'''):
        self.response = response
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''"{self.response}" {self.message}''' 

class InvalidResponseError(Exception):
    def __init__(self,response,message='''isn't a valid option!'''):
        self.response = response
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''"{self.response}" {self.message}''' 

class NotANumberError(Exception):
    def __init__(self,response,message='''isn't a valid number!'''):
        self.response = response
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''"{self.response}" {self.message}''' 

class OutOfRangeError(Exception):
    def __init__(self,min,max,val,message='''Number is out of range!'''):
        self.min = min
        self.max = max
        self.val = val
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''{self.message} Expected {self.min} to {self.max}, got {self.val}.'''

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
                        raise InvalidAffirmativeError(Confirm.lower())
                except InvalidAffirmativeError as e:
                    print(str(e.response) + " " + str(e))
                    continue
            else:
                raise InvalidAffirmativeError(MakeDirectory.lower())
        except InvalidAffirmativeError as e:
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
    'InitialDeck': ["🂡","🂱","🃁","🃑","🂢","🂲","🃂","🃒","🂣","🂳","🃃","🃓","🂤","🂴","🃄","🃔","🂥","🂵","🃅","🃕","🂦","🂶","🃆","🃖","🂧","🂷","🃇","🃗","🂨","🂸","🃈","🃘","🂩","🂹","🃉","🃙","🂪","🂺","🃊","🃚","🂫","🂻","🃋","🃛","🂭","🂽","🃍","🃝","🂮","🂾","🃎","🃞"],
    'CurrentDeck': ["🂡","🂱","🃁","🃑","🂢","🂲","🃂","🃒","🂣","🂳","🃃","🃓","🂤","🂴","🃄","🃔","🂥","🂵","🃅","🃕","🂦","🂶","🃆","🃖","🂧","🂷","🃇","🃗","🂨","🂸","🃈","🃘","🂩","🂹","🃉","🃙","🂪","🂺","🃊","🃚","🂫","🂻","🃋","🃛","🂭","🂽","🃍","🃝","🂮","🂾","🃎","🃞"],
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

# Main Menu

DebugEnabled = False

def NewGame():
    if CurrentGameData['WalletType'] == "Standard":
        CurrentGameData['Wallet'] == 1000
    elif CurrentGameData['WalletType'] == "Denominations":
        CurrentGameData['Wallet'] == {
            '1':5,
            '5':4,
            '25':4,
            '125':2,
            '625':1
        }
    else: # Endless
        CurrentGameData['Wallet'] == infinity
    CurrentGameData['CurrentDeck'] = CurrentGameData['InitialDeck']
    CurrentGameData['PlayerHandMax'] = 2
    CurrentGameData['HouseHandMax'] = 1
    not CurrentGameData['GameInProgress']


print(f'''╔═══════════════════════════════════════════════════════════╗
║    {c.c}______             _                               {c.e}    ║
║    {c.c}| ___ \           | |                              {c.e}    ║
║    {c.c}| |_/ / __ _ _ __ | | _____ _ __ ___   _ __  _   _ {c.e}    ║
║    {c.c}| ___ \/ _` | '_ \| |/ / _ \ '__/ __| | '_ \| | | |{c.e}    ║
║    {c.c}| |_/ / (_| | | | |   <  __/ |  \__ \_| |_) | |_| |{c.e}    ║
║    {c.c}\____/ \__,_|_| |_|_|\_\___|_|  |___(_) .__/ \__, |{c.e}    ║
║    {c.c}                                      | |     __/ |{c.e}    ║
║    {c.c}Alpha v0.2                            |_|    |___/ {c.e}    ║
╚═══════════════════════════════════════════════════════════╝''')
print()
print(f'''{c.y}Welcome to{c.e} Bankers.py{c.y}!{c.e}''')
print()

def ConfigureGame():
    while True:
        Config = input(f'''
{c.y}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃          {c.m}What do you want to change?{c.y}          ┃
┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨
┃                                               ┃
┃  {c.g}►{c.o} (W)allet type{c.y}                              ┃
┃  {c.g}►{c.o} Maximum (p)layer cards{c.y}                     ┃
┃  {c.g}►{c.o} Maximum (H)ouse cards{c.y}                      ┃
┃  {c.c}►{c.o} (B)ack to main menu{c.y}                        ┃
┃                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{c.e}

>>
''')
        try:
            if Config.lower().split() in ('b', ''):
                break
            elif Config.lower() == "w":
                while True:
                    try:
                        WalletType = input(f'''
{c.y}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃          {c.m}What type do you want?{c.y}          ┃
┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨
┃                                               ┃
┃  {c.g}►{c.o} (S)tandard ($1000, one-by-one){c.y}                              ┃
┃  {c.g}►{c.o} (D)enominations ($1000, split into 5 chip groups){c.y}                     ┃
┃  {c.g}►{c.o} (E)ndless (Infinite money; no achievements){c.y}                      ┃
┃  {c.c}►{c.o} (B)ack{c.y}                        ┃
┃                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{c.e}

>>
''')
                        if WalletType.lower().strip() in ('b',''):
                            break
                        elif WalletType.lower() == "s":
                            CurrentGameData['WalletType'] = "Standard"
                        elif WalletType.lower() == "d":
                            CurrentGameData['WalletType'] = "Denominations"
                        elif WalletType.lower() == "e":
                            CurrentGameData['WalletType'] = "Endless"
                        else:
                            raise InvalidResponseError(WalletType)
                    except InvalidResponseError:
                        print(str(e.response) + " " + str(e))
                        continue
            elif Config.lower() == "p":
                while True:
                    try:
                        PlayerCards = input(f'{c.m}Enter a valid number, between 2 and 5: {c.b}>>{c.e} ')
                        if PlayerCards.isnumeric() and (2 <= PlayerCards >= 5):
                            CurrentGameData['PlayerHandMax'] = PlayerCards
                            break
                        elif PlayerCards.isnumeric() and not (2 <= PlayerCards >= 5):
                            raise OutOfRangeError(2,5,PlayerCards)
                        elif not PlayerCards.isnumeric():
                            raise NotANumberError(PlayerCards)
                    except NotANumberError:
                        print(str(e.response) + " " + str(e))
                        continue
                    except OutOfRangeError:
                        print(str(e.val) + " " + str(e))
                        continue
            elif Config.lower() == "h":
                while True:
                    try:
                        PlayerCards = input(f'{c.m}Enter a valid number, between 1 and 3: {c.b}>>{c.e} ')
                        if PlayerCards.isnumeric() and (1 <= PlayerCards >= 3):
                            CurrentGameData['HouseHandMax'] = PlayerCards
                            break
                        elif PlayerCards.isnumeric() and not (1 <= PlayerCards >= 3):
                            raise OutOfRangeError(1,3,PlayerCards)
                        elif not PlayerCards.isnumeric():
                            raise NotANumberError(PlayerCards)
                    except NotANumberError:
                        print(str(e.response) + " " + str(e))
                        continue
                    except OutOfRangeError:
                        print(str(e.val) + " " + str(e))
                        continue
            else:
                raise InvalidResponseError(Config.lower())
        except InvalidResponseError:
            print(str(e.response) + " " + str(e))
            continue            

def DataCheck():
    while True:
        try:
            if os.path.exists(GamePath + 'save.dat'):
                print(f'''{c.r}[ATTN]:{c.e} Save data for Bankers.py was found!''')
                Overwrite = input(f'''{c.m}Are you sure you want to overwrite?{c.b} [y/N] {c.e}''')
                if Overwrite.lower().strip() in ('n',''):
                    break
                elif Overwrite.lower().strip() == "y":
                    NewGame()
                    break
                else:
                    raise InvalidAffirmativeError(Overwrite.lower())
            else:
                NewGame()
                break
        except InvalidAffirmativeError as e:
            print(str(e.response) + " " + str(e))
            continue

while True:
    try:
        MainMenu = input(f'''
╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
│          {c.m}What would you like to do?{c.e}          │
├──────────────────────────────────────────────┤
│                                              │
│  {c.b}► {c.y}(N)ew game{c.e}                                │
│  {c.c}► {c.y}(L)oad game{c.e}                               │
│  {c.c}► {c.y}(C)onfigure games{c.e}                         │
│  {c.c}► {c.y}(E)xit Bankers.py{c.e}                         │
│                                              │
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯

>> ''')
        if MainMenu.lower().strip() in ('n',''):
            try:
                DataCheck()
                break
            except KeyboardInterrupt:
                print(f'{c.r}[ATTN:]{c.e} Bankers.py detected a keyboard interrupt exit (Ctrl+C)!')
                print('You can always exit at any time via the Pause menu; keyboard interrupts can cause data loss!')
                ExitCheck = input(f'{c.m}Would you like to save your progress and exit?{c.b} [Y/n] {c.e}')
                while True:
                    if ExitCheck.lower().strip() in ('y',''):
                        SaveGame()
                        exit()
                    else:
                        break
        elif MainMenu.lower() == "l":
            try:
                LoadGame()
            except KeyboardInterrupt:
                print(f'''{c.r} _    _  _____  ___   _   _ _ 
| |  | ||  _  |/ _ \ | | | | |
| |  | || | | / /_\ \| |_| | |
| |/\| || | | |  _  ||  _  | |
\  /\  /\ \_/ / | | || | | |_|
 \/  \/  \___/\_| |_/\_| |_(_){c.e}''')
                print("It looks like you just tried to Keyboard Interrupt while the game is loading!")
                print("The game has stopped loading and will now return to the main menu.")
        elif MainMenu.lower() == "c":
            ConfigureGame()
        elif MainMenu.lower() == "e":
            print(f'{c.c}Thank you for playing!{c.e}')
            exit()
        elif MainMenu.lower() == "debug":
            DebugEnabled = True
        else:
            raise InvalidResponseError(MainMenu.lower())
    except KeyboardInterrupt:
        print(f'{c.r}[ATTN:]{c.e} Bankers.py detected a keyboard interrupt exit (Ctrl+C)!')
        print('''You're at the main menu; exiting is easy from here!''')
        ExitCheck = input(f'{c.m}Are you sure you want to exit?{c.b} [Y/n] {c.e}')
        while True:
            try:
                if ExitCheck.lower().strip() in ('y',''):
                    exit()
                elif ExitCheck.lower() == "n":
                    break
                else:
                    raise InvalidAffirmativeError(ExitCheck.lower())
            except InvalidAffirmativeError as e:
                print(str(e.response) + " " + str(e))
                continue
    except InvalidResponseError:
        print(str(e.response) + " " + str(e))
        continue

