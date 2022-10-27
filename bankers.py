# Imports and Globals

from locale import currency
import os, platform, struct, sys
from time import sleep
from datetime import datetime
from math import inf as infinity
from random import randrange as random
from tkinter import N

now = datetime.now()
CanSave = None
EndlessBlurbs = [
    "Great play!",
    "An amazing display.",
    "May the cards be ever in your favor!",
    "Heart of the cards!",
    "You didn't stack the deck, did you?",
    "Now try Standard!",
    "A real ace up the sleeve!",
    "Jack of all trades!",
    "Talk about a wild card!"
]

# Classes and Exceptions

class c:
    r = '\033[91m'
    o = '\033[38;2;81;57;47m'
    y = '\033[93m'
    g = '\033[92m'
    c = '\033[38;2;0;255;255m'
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

class UnsupportedError(Exception):
    pass

class InvalidAffirmativeError(Exception):
    def __init__(self,response,message='''isn't a valid option! Expected "y", "n", or nothing.'''):
        self.response = response
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''{c.r}"{self.response}"{c.e} {self.message}''' 

class InvalidResponseError(Exception):
    def __init__(self,response,message='''isn't a valid option!'''):
        self.response = response
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''{c.r}"{self.response}"{c.e} {self.message}''' 

class NotANumberError(Exception):
    def __init__(self,response,message='''isn't a valid number!'''):
        self.response = response
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''{c.r}"{self.response}"{c.e} {self.message}''' 

class OutOfRangeError(Exception):
    def __init__(self,min,max,val,message='''is out of range!'''):
        self.min = min
        self.max = max
        self.val = val
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'''{c.r}{self.val}{c.e} {self.message}. Expected {self.min} to {self.max}.'''

# System check

System = platform.system()

def MakeDirChoice(Path):
    SavingDisabled = False
    while True:
        try:
            MakeDirectory = input(f"{c.y}Would you like to create it now?{c.b} [Y/n] {c.e}")
            if MakeDirectory.lower() == 'y' or MakeDirectory.strip() == '':
                print(f"{c.g}Creating Bankers.py directory...{c.e}")
                os.makedirs(Path)
                print(f"{c.c}Done!{c.e}")
                SavingDisabled = False
                return SavingDisabled
            elif MakeDirectory.lower() == 'n':
                try:
                    Confirm = input(f'{c.r}Are you sure?{c.e} Not creating the directory will result in saving being disabled.{c.b} [Y/n] {c.e}')
                    if Confirm.lower() == 'y' or Confirm.strip() == '':
                        SavingDisabled = True
                        return SavingDisabled
                    elif Confirm.lower() == 'n':
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
        GamePath = os.getenv('appdata') + "\\Bankers.py\\"
        if not os.path.exists(GamePath):
            print(f"{c.y}[ATTN]:{c.e} No Bankers.py directory found!")
            CanSave = MakeDirChoice(GamePath)
            not CanSave
    elif System == "Linux":
        GamePath = os.getenv('HOME') + "/Bankers.py/"
        if not os.path.exists(GamePath):
            print(f"{c.y}[ATTN]:{c.e} No Bankers.py directory found!")
            CanSave = MakeDirChoice(GamePath)
            not CanSave
    else:
        raise UnsupportedError
except UnsupportedError:
    print("{c.r}[FATAL]:{c.e} This OS isn't currently supported by Bankers.py!")
    print("We're trying hard to get this compatible with every OS we can,")
    print("so stick with us and we'll update you!")
    exit()

# Data and Save/load

CurrentGameData = {
    'GameInProgress': False,
    'CurrentHand': [],
    'CurrentBet': 0,
    'HouseCard': None,
    'PlacedCard': None,
    'Wallet': 1000,
    'InitialDeck': ["K","K","K","K","Q","Q","Q","Q","J","J","J","J","10","10","10","10","9","9","9","9","8","8","8","8","7","7","7","7","6","6","6","6","5","5","5","5","4","4","4","4","3","3","3","3","2","2","2","2","A","A","A","A"],
    'CurrentDeck': ["K","K","K","K","Q","Q","Q","Q","J","J","J","J","10","10","10","10","9","9","9","9","8","8","8","8","7","7","7","7","6","6","6","6","5","5","5","5","4","4","4","4","3","3","3","3","2","2","2","2","A","A","A","A"],
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
    elif CanSave == None:
        print(f'{c.r}[FATAL]:{c.e} Failed to check if saving can be done safely! Bankers.py will now quit.')
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

# Main Menu and The Game

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
    CurrentGameData['CurrentDeck'] = CurrentGameData['InitialDeck'].copy()
    CurrentGameData['PlayerHandMax'] = 2
    CurrentGameData['HouseHandMax'] = 1
    CurrentGameData['CurrentBet'] = 0
    not CurrentGameData['GameInProgress']


print(f'''╔═══════════════════════════════════════════════════════════╗
║    {c.c}______             _                               {c.e}    ║
║    {c.c}| ___ \           | |                              {c.e}    ║
║    {c.c}| |_/ / __ _ _ __ | | _____ _ __ ___   _ __  _   _ {c.e}    ║
║    {c.c}| ___ \/ _` | '_ \| |/ / _ \ '__/ __| | '_ \| | | |{c.e}    ║
║    {c.c}| |_/ / (_| | | | |   <  __/ |  \__ \_| |_) | |_| |{c.e}    ║
║    {c.c}\____/ \__,_|_| |_|_|\_\___|_|  |___(_) .__/ \__, |{c.e}    ║
║    {c.c}                                      | |     __/ |{c.e}    ║
║    {c.c}Beta v1.1                            |_|    |___/ {c.e}     ║
╚═══════════════════════════════════════════════════════════╝''')
print()
print(f'''{c.y}Welcome to{c.e} Bankers.py{c.y}!{c.e}''')

def PlayGame():
    while not ExitGame:
        try:

            # Make your bet
            if CurrentGameData['WalletType'] == "Standard":
                print(f"{c.g}Wallet: {CurrentGameData['Wallet']}{c.e}")
                while True:
                    try:
                        print(f'''{c.c}How much would you like to bet? {c.m}(Type P to pause. Minimum bet: 1){c.e}''')
                        BetAmount = input(">> ")
                        if BetAmount.isnumeric() and (1 <= int(BetAmount) <= CurrentGameData['Wallet']):
                            CurrentGameData['CurrentBet'] = int(BetAmount)
                            CurrentGameData['Wallet'] = CurrentGameData['Wallet'] - int(BetAmount)
                            print()
                            break
                        elif BetAmount.isnumeric() and not (1 <= int(BetAmount) <= CurrentGameData['Wallet']):
                            raise OutOfRangeError(1,CurrentGameData['Wallet'],int(BetAmount))
                        elif BetAmount.lower() == "p":
                            pass
                        else:
                            raise NotANumberError(BetAmount)
                    except OutOfRangeError as e:
                        print()
                        print(str(e.val) + " " + str(e))
                        continue
                    except NotANumberError as e:
                        print()
                        print(str(e.response) + " " + str(e))
                        continue
            
            # Card selection
            Matched = False
            Origin = CurrentGameData["CurrentDeck"].copy()
            while not Matched:
                if not len(CurrentGameData["CurrentDeck"]) == 0 and not CurrentGameData["Wallet"] == 0:
                    if CurrentGameData["HouseHandMax"] == 1:
                        CurrentGameData['HouseCard'] = CurrentGameData["CurrentDeck"].pop(random(len(Origin)))
                        Origin = CurrentGameData["CurrentDeck"].copy()
                        print(f'''The House puts down {CurrentGameData["HouseCard"]}''')
                        if CurrentGameData["HouseCard"] == CurrentGameData["PlacedCard"]:
                            if CurrentGameData["WalletType"] == "Standard":
                                print(f'''{c.r}Match!{c.e} You lost the bet this time...''')
                            else:
                                print(f'''{c.r}Match!{c.e} Better luck next time.''')
                            print()
                            CurrentGameData['CurrentBet'] = 0
                            CurrentGameData["CurrentDeck"] = CurrentGameData['InitialDeck'].copy()
                            Origin = CurrentGameData["CurrentDeck"].copy()
                            CurrentGameData["HouseCard"] = None
                            CurrentGameData["PlacedCard"] = None
                            CurrentGameData["CurrentHand"] = []
                            Matched = True
                    else:

                        for i in range(CurrentGameData["HouseHandMax"]):
                            CurrentGameData["HouseCard"] = []
                            CurrentGameData["HouseCard"].append(CurrentGameData["CurrentDeck"].pop(random(len(Origin))))
                            Origin = CurrentGameData["CurrentDeck"].copy()
                            print(f'''The House put down {CurrentGameData["HouseCard"]}''')

                            for i in range(len(CurrentGameData["HouseCard"])):
                                if CurrentGameData["HouseCard"][i] == CurrentGameData["PlacedCard"]:
                                    if CurrentGameData["WalletType"] == "Standard":
                                        print(f'''{c.r}Match!{c.e} You lost the bet this time...''')
                                    else:
                                        print(f'''{c.r}Match!{c.e} Better luck next time.''')
                                    print()
                                    CurrentGameData['CurrentBet'] = 0
                                    CurrentGameData["CurrentDeck"] = CurrentGameData['InitialDeck'].copy()
                                    Origin = CurrentGameData["CurrentDeck"].copy()
                                    CurrentGameData["HouseCard"] = None
                                    CurrentGameData["PlacedCard"] = None
                                    CurrentGameData["CurrentHand"] = []
                                    Matched = True

                    for i in range((CurrentGameData["PlayerHandMax"] - len(CurrentGameData["CurrentHand"]))):
                        CurrentGameData["CurrentHand"].append(CurrentGameData["CurrentDeck"].pop(random(len(Origin))))
                        Origin = CurrentGameData["CurrentDeck"].copy()

                    while True:
                        if Matched:
                            break

                        try:
                            print('Your hand:')
                            print(*CurrentGameData["CurrentHand"],sep=", ")
                            print()
                            print(f'''{c.c}Starting from the left at 1, which card do you wish to put down? (Type P to pause.){c.e}''')
                            CardChoice = input(">> ")
                            if CardChoice.isnumeric() and (1 <= int(CardChoice) <= len(CurrentGameData["CurrentHand"])):
                                print()
                                CurrentGameData["PlacedCard"] = CurrentGameData["CurrentHand"].pop(int(CardChoice) - 1)
                                if CurrentGameData["PlacedCard"] == CurrentGameData["HouseCard"] or CurrentGameData["PlacedCard"] in CurrentGameData["HouseCard"]:
                                    if CurrentGameData["WalletType"] == "Standard":
                                        print(f'''{c.g}Match!{c.m} Here's your payout!{c.e}''')
                                    else:
                                        print(f'''{c.g}Match!{c.m} {EndlessBlurbs[random(len(EndlessBlurbs))]}{c.e}''')
                                    print()
                                    CurrentGameData['Wallet'] = CurrentGameData['Wallet'] + (CurrentGameData["CurrentBet"] * 2)
                                    CurrentGameData["CurrentDeck"] = CurrentGameData['InitialDeck'].copy()
                                    Origin = CurrentGameData["CurrentDeck"].copy()
                                    CurrentGameData["HouseCard"] = None
                                    CurrentGameData["PlacedCard"] = None
                                    CurrentGameData["CurrentHand"] = []
                                    Matched = True
                                else:
                                    break
                            elif CardChoice.isnumeric() and not (1 <= int(CardChoice) <= len(CurrentGameData["CurrentHand"])):
                                raise OutOfRangeError(1,len(CurrentGameData["CurrentHand"]),int(CardChoice))
                            elif CardChoice.lower() == "p":
                                pass
                            else:
                                raise NotANumberError(CardChoice)
                        except OutOfRangeError as e:
                            print()
                            print(str(e.val) + " " + str(e))
                            continue
                        except NotANumberError as e:
                            print()
                            print(str(e.response) + " " + str(e))
                            continue
                elif len(CurrentGameData["CurrentDeck"]) == 0:
                    print(f'''{c.o}Out of cards! Shuffling the deck with the available cards...{c.e}''')
                    CurrentGameData["CurrentDeck"] = CurrentGameData["InitialDeck"]
                    if CurrentGameData["HouseHandMax"] == 1:
                        CurrentGameData["CurrentDeck"].remove(CurrentGameData["HouseCard"])
                    else:
                        for i in CurrentGameData["HouseCard"]:
                            CurrentGameData["CurrentDeck"].remove(CurrentGameData["HouseCard"][i])
                    for i in CurrentGameData["CurrentHand"]:
                        CurrentGameData["CurrentDeck"].remove(CurrentGameData["CurrentHand"][i])
                elif CurrentGameData["Wallet"] == 0 and CurrentGameData["CurrentBet"] == 0:
                    print()
                    print(f'''{c.r} ______                __                         __   
|   __ \.---.-..-----.|  |--..----..--.--..-----.|  |_ 
|   __ <|  _  ||     ||    < |   _||  |  ||  _  ||   _|
|______/|___._||__|__||__|__||__|  |_____||   __||____|
                                            |__|{c.e}''')
                    print()
                    print(f'''{c.o}Your money ran out!{c.e}''')
                    while True:
                        try:
                            PlayAgain = input(f'''{c.m}Would you like to try again?{c.b} [Y/n] {c.e}''')
                            if PlayAgain.lower() == "y" or PlayAgain.strip() == "":
                                break
                            elif PlayAgain.lower() == "n":
                                MainMenu()
                            else:
                                raise InvalidAffirmativeError(PlayAgain.lower())
                        except InvalidResponseError as e:
                            print(str(e.response) + " " + str(e))
                            continue
                
                
        except KeyboardInterrupt:
            print(f'{c.r}[ATTN:]{c.e} Bankers.py detected a keyboard interrupt exit (Ctrl+C)!')
            print('You can always exit at any time via the Pause menu; keyboard interrupts can cause data loss!')
            ExitCheck = input(f'{c.m}Would you like to save your progress and exit?{c.b} [Y/n] {c.e}')
            while True:
                if ExitCheck.lower() == 'y' or ExitCheck.strip() == '':
                    SaveGame()
                    exit()
                else:
                    break

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

>> ''')
        try:
            if Config.lower() == 'b' or Config.strip() == '':
                break
            elif Config.lower() == "w":
                while True:
                    try:
                        WalletType = input(f'''
{c.y}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                 {c.m}What type do you want?{c.y}                   ┃
┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨
┃                                                          ┃
┃  {c.g}►{c.o} (S)tandard ($1000, one-by-one){c.y}                        ┃
┃  {c.g}►{c.o} (E)ndless (Infinite money; no achievements){c.y}           ┃
┃  {c.c}►{c.o} (B)ack{c.y}                                                ┃
┃                                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{c.e}

>> ''')
#┃  {c.g}►{c.o} (D)enominations ($1000, split into 5 chip groups){c.y}     ┃ -- Denominations doesn't work with how WalletType is currently set, so it's disabled
                        if WalletType.lower() == "b" or WalletType.strip() == "":
                            break
                        elif WalletType.lower() == "s":
                            CurrentGameData['WalletType'] = "Standard"
                            break
                        #elif WalletType.lower() == "d":
                        #    CurrentGameData['WalletType'] = "Denominations"
                        elif WalletType.lower() == "e":
                            CurrentGameData['WalletType'] = "Endless"
                            break
                        else:
                            raise InvalidResponseError(WalletType)
                    except InvalidResponseError as e:
                        print(str(e.response) + " " + str(e))
                        continue
            elif Config.lower() == "p":
                while True:
                    try:
                        PlayerCards = input(f'{c.m}Enter a valid number, between 2 and 5: {c.b}>>{c.e} ')
                        if PlayerCards.isnumeric() and (2 <= int(PlayerCards) <= 5):
                            CurrentGameData['PlayerHandMax'] = int(PlayerCards)
                            print()
                            print(f"{c.g}Set your maximum hand count to {int(PlayerCards)}!{c.e}")
                            break
                        elif PlayerCards.isnumeric() and not (2 <= int(PlayerCards) <= 5):
                            raise OutOfRangeError(2,5,int(PlayerCards))
                        elif not PlayerCards.isnumeric():
                            raise NotANumberError(int(PlayerCards))
                    except NotANumberError as e:
                        print(str(e.response) + " " + str(e))
                        continue
                    except OutOfRangeError as e:
                        print(str(e.val) + " " + str(e))
                        continue
            elif Config.lower() == "h":
                while True:
                    try:
                        HouseCards = input(f'{c.m}Enter a valid number, between 1 and 3: {c.b}>>{c.e} ')
                        if HouseCards.isnumeric() and (1 <= int(HouseCards) <= 3):
                            CurrentGameData['HouseHandMax'] = int(HouseCards)
                            print()
                            print(f"{c.g}Set the House's maximum hand count to {int(HouseCards)}!{c.e}")
                            print()
                            break
                        elif HouseCards.isnumeric() and not (1 <= int(HouseCards) <= 3):
                            raise OutOfRangeError(1,3,int(HouseCards))
                        elif not HouseCards.isnumeric():
                            raise NotANumberError(int(HouseCards))
                    except NotANumberError as e:
                        print(str(e.response) + " " + str(e))
                        continue
                    except OutOfRangeError as e:
                        print(str(e.val) + " " + str(e))
                        continue
            else:
                raise InvalidResponseError(Config.lower())
        except InvalidResponseError as e:
            print(str(e.response) + " " + str(e))
            continue            

def DataCheck():
    while True:
        try:
            if os.path.exists(GamePath + 'save.dat'):
                print(f'''{c.r}[ATTN]:{c.e} Save data for Bankers.py was found!''')
                Overwrite = input(f'''{c.m}Are you sure you want to load a new game?{c.b} [y/N] {c.e}''')
                if Overwrite.lower() == 'n' or Overwrite.strip() == "":
                    break
                elif Overwrite.lower() == "y":
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

def MainMenu():
    while True:
        try:
            MainOptions = input(f'''
╭──────────────────────────────────────────────╮
│          {c.m}What would you like to do?{c.e}          │
├──────────────────────────────────────────────┤
│                                              │
│  {c.g}► {c.y}(N)ew game{c.e}                                │
│  {c.c}► {c.y}(L)oad game{c.e}                               │
│  {c.c}► {c.y}(C)onfigure games{c.e}                         │
│  {c.c}► {c.y}(E)xit Bankers.py{c.e}                         │
│                                              │
╰──────────────────────────────────────────────╯

>> ''')
            if MainOptions.lower() == 'n' or MainOptions.strip() == '':
                try:
                    DataCheck()
                    break
                except KeyboardInterrupt:
                    print(f'{c.r}[ATTN:]{c.e} Bankers.py detected a keyboard interrupt exit (Ctrl+C)!')
                    print('You can always exit at any time via the Pause menu; keyboard interrupts can cause data loss!')
                    ExitCheck = input(f'{c.m}Would you like to save your progress and exit?{c.b} [Y/n] {c.e}')
                    while True:
                        if ExitCheck.lower() == 'y' or ExitCheck.strip() == '':
                            SaveGame()
                            exit()
                        else:
                            break
            elif MainOptions.lower() == "l":
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
            elif MainOptions.lower() == "c":
                ConfigureGame()
            elif MainOptions.lower() == "e":
                print(f'{c.c}Thank you for playing!{c.e}')
                exit()
            elif MainOptions.lower() == "debug":
                DebugEnabled = True
            else:
                raise InvalidResponseError(MainOptions.lower())
        except KeyboardInterrupt:
            print(f'{c.r}[ATTN:]{c.e} Bankers.py detected a keyboard interrupt exit (Ctrl+C)!')
            print('''You're at the main menu; exiting is easy from here!''')
            ExitCheck = input(f'{c.m}Are you sure you want to exit?{c.b} [Y/n] {c.e}')
            while True:
                try:
                    if ExitCheck.lower() == 'y' or ExitCheck.strip() == '':
                        exit()
                    elif ExitCheck.lower() == "n":
                        break
                    else:
                        raise InvalidAffirmativeError(ExitCheck.lower())
                except InvalidAffirmativeError as e:
                    print(str(e.response) + " " + str(e))
                    continue
        except InvalidResponseError as e:
            print(str(e.response) + " " + str(e))
            continue

MainMenu()
ExitGame = False
print()
print(f'''{c.y}╔═════════════════════════════════════════════════════════════════╗
║          {c.m}___      _                            _      __{c.y}        ║
║         {c.m}F __".   FJ_       ___ _     _ ___    FJ_     LJ{c.y}        ║
║        {c.m}J (___|  J  _|     F __` L   J '__ ", J  _|    FJ{c.y}        ║
║        {c.m}J\___ \  | |-'    | |--| |   | |__|-J | |-'   J__L{c.y}       ║
║       {c.m}.--___) \ F |__-.  F L__J J   F L  `-' F |__-.  __{c.y}        ║
║       {c.m}J\______J \_____/ J\____,__L J__L      \_____/ J__L{c.y}       ║
║        {c.m}J______F J_____F  J____,__F |__L      J_____F |__|{c.y}       ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝{c.e}''')
print()
PlayGame()