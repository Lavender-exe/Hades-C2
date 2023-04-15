# Hades-C2

Hades is a basic Command & Control framework built using Python. It is currently _extremely_ bare bones, but I plan to add more features soon.

**Server tested on Windows - Currently working on an overhaul and remake of the server**

**⚠️ Expect bugs**

## Features
- [x] Windows Implant
  - Python Implant
  - Executable Implant
  - Powershell Cradle
- [x] Linux Implant
- [x] Basic Command & Control functionality
  - CMD Commands
  - BASH Commands
- [x] Basic Persistence
  - Linux Cronjob
  - Windows Registry Autorun

## Installation
1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`

```bash
git clone https://github.com/lavender-exe/Hades-C2.git
cd Hades-C2
pip install -r requirements.txt
```

## Usage

### Help:
```bash
Listener Commands
---------------------------------------------------------------------------------------

listeners -g --generate           --> Generate Listener

Session Commands
---------------------------------------------------------------------------------------

sessions -l --list                --> List Sessions
sessions -i --interact            --> Interact with Session
sessions -k --kill <value>        --> Kill Active Session

Payload Commands
---------------------------------------------------------------------------------------

winplant.py                       --> Windows Python Implant
exeplant.py                       --> Windows Executable Implant
linplant.py                       --> Linux Implant
pshell_shell                      --> Powershell Implant

Client Commands
---------------------------------------------------------------------------------------

persist / pt                      --> Persist Payload (After Interacting with Session) 
background / bg                   --> Background Session
exit                              --> Kill Client Connection

Misc Commands
---------------------------------------------------------------------------------------

help / h                          --> Show Help Menu
clear / cls                       --> Clear Screen
```
### Server:
1. Run the server using `python hades-c2.py`
2. Run `listeners -g / --generate` to generate a listener
3. Select the IP and Port for the listener

### Implant:
1. Create an implant using `winplant.py`, `linplant.py` or `exeplant.py`
2. Run the implant on the target machine

## Future Plans

- [ ] Add more persistence methods
- [ ] Add more command functionality
- [ ] Use Nim/C++ to create cross-platform malware
- [ ] Add more Quality of Life features
- [ ] Flask Web Interface
- [ ] Add more Implant types
