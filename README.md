# ViperDefender
ViperDefender is a python based client that can be used to detect and remove malware from a system. It uses the [VirusTotal]() API to scan files and a cloud sandbox that test every file downloaded on the Computer. It also has a public API that can be used to scan files.

## Table of Contents
- [ViperDefender](#viperdefender)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [API](#api)
  - [Contributing](#contributing)

## Requirements
A computer using Windows 10&trade; or Windows 11&trade; 
[python 3 or higher](https://www.python.org/downloads/)
[pip](https://pypi.org/project/pip/)

The api [url](https://viperdefense.azurewebsites.net/api/)
=======
## Installation
You can download and install the latest version of ViperDefender [here](https://github.com/Mattherix/ViperDefender/releases/tag/v1.0.0)

## API
We also have a public API that can be used.
The client is depending on the API.
Here is the api [url](https://viperdefense.azurewebsites.net/api/) and an [example endpoint](https://viperdefense.azurewebsites.net/api/HttpTrigger2?name=test). You can find the Insomnia configuration [here](https://github.com/Mattherix/ViperDefender/blob/main/src/orchestrator/insomnia.config.json).

## Contributing
<a href="https://github.com/Mattherix/ViperDefender/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Mattherix/ViperDefender" />
</a>
