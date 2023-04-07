# Hades-C2

Hades is a basic Command & Control framework built using Python. It is currently _extremely_ barebones, but I plan to add more features soon.

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
  - Linux Cronjobs
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
### Server:
1. Run the server using `python server.py`
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
