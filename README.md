  <h3 align="center">Hades Command & Control</h3>

  <p align="center">
    Hades is a basic Command & Control server built using Python. It is currently extremely bare bones, but I plan to add more features soon.
Features are a work in progress currently.</p>
  <p align="center">⚠ Expect bugs ⚠
    <br/>
</p>

![Downloads](https://img.shields.io/github/downloads/Lavender-exe/Hades-C2/total) ![Contributors](https://img.shields.io/github/contributors/Lavender-exe/Hades-C2?color=dark-green) ![Stargazers](https://img.shields.io/github/stars/Lavender-exe/Hades-C2?style=social) ![Issues](https://img.shields.io/github/issues/Lavender-exe/Hades-C2) ![License](https://img.shields.io/github/license/Lavender-exe/Hades-C2) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

![Screen Shot](https://media.discordapp.net/attachments/504609193060466694/1099041152306528266/image.png?width=748&height=621)

This is a project made (mostly) for me to learn Malware Development, Sockets, and C2 infrastructure setups. Currently, the server can be used for CTFs but it is still a buggy mess with a lot of things that need ironed out.

I am working on a Web UI using Flask currently so new features are being put on hold until then, if you face any issues then please be sure to create an issues request.

### Features
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

## Getting Started

### Help
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


### Prerequisites

- Python3 Pip
- Colorama

### Installation

```bash
git clone https://github.com/lavender-exe/Hades-C2.git
cd Hades-C2
# Windows
python install.py
# Linux
python3 install.py
python3 hades-c2.py
```

#### Server:
1. Run the server using `python hades-c2.py`
2. Run `listeners -g / --generate` to generate a listener
3. Select the IP and Port for the listener

#### Implant:
1. Create an implant using `winplant.py`, `linplant.py` or `exeplant.py`
2. Run the implant on the target machine

## Roadmap

See the [open issues](https://github.com/Lavender-exe/Hades-C2/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/Lavender-exe/Hades-C2/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/Lavender-exe/Hades-C2/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Plans

- [ ] Better Implant Functions
- [ ] Add more persistence methods
- [ ] Add more command functionality
- [ ] Use Nim/C++ to create cross-platform malware
- [ ] Add more Quality of Life features
- [ ] Flask Web Interface

## License

Distributed under the MIT License. See [LICENSE](https://github.com/Lavender-exe/Hades-C2/blob/main/LICENSE.md) for more information.

## Authors

* **Lavender** - *Nerd* - [Lavender](https://github.com/Lavender-exe/) - *Created Project*

## Acknowledgements

* [Joe Helle](https://twitter.com/joehelle?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)
