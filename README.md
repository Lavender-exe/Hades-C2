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
* [Acknowledgements](#acknowledgements)

## About The Project

![Project Banner](https://repository-images.githubusercontent.com/624929971/355d4e3d-1c4c-459e-9c62-8c8bf5f04a57)

This is a project made (mostly) for me to learn Malware Development, Sockets, and C2 infrastructure setups. Currently, the server can be used for CTFs but it is still a buggy mess with a lot of things that need ironed out.

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

### Prerequisites

- Python3 Pip

### Installation

```bash
git clone https://github.com/lavender-exe/Hades-C2.git

cd Hades-C2

pip install -r misc/requirements.txt
```

#### Server:
1. Run the server using `python hades-c2.py`
2. Run `listeners -g / --generate` to generate a listener
3. Select the IP and Port for the listener

## Roadmap

See the [open issues](https://github.com/Lavender-exe/Hades-C2/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/Lavender-exe/Hades-C2/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Plans

- [x] SSL/TLS Encryption
- [ ] Command and Session Logging
- [ ] Client Interface 
- [ ] Additional Communication Channels/Protocols (HTTP/TLV)
- [ ] Exfiltration Capabilities
- [ ] Increased Malleability
- [ ] Multithreaded Listeners (Start for Team Server)

## License

Distributed under the GNU GPLv3. See [LICENSE](https://github.com/Lavender-exe/Hades-C2/blob/dev-broken/misc/LICENSE) for more information.

## Acknowledgements

* [Joe Helle](https://twitter.com/joehelle?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)
