<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Python script that downloads files from the internet and saves them in a download directory.

The list of URLs to download will be provided in a simple text file.
URLs are separated by a newline. Assume that the files are small, so downloading them does not require streaming.

### Considered issues
> How to handle HTTP 404 errors?

Handled by checking status code and only responses that have 200 are Successful

> How to make the download process faster?

Async programing solve this issue. The hard limit is set by aiohttp which set
connection numbers to 100 by default. But also it could be configured by CLI
param
(REF: https://docs.aiohttp.org/en/latest/http_request_lifecycle.html#how-to-use-the-clientsession)

> How to display the progress of downloads?

`await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)` and especially
`asyncio.FIRST_COMPLETED` make it possible

> How to handle cancellation? (i.e., the user presses CTRL+C)

As I'm using event loop there is no problem with handling leftover python processes
as it could be if I would spawn separate processes for download

> Optional: How to handle retry in case of intermittent network errors?

Based on which exception is understood as retryable there is a retry functionality.
Implementation an exponential backoff retry strategy would be even better comparing
with constant time sleep

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
[![AIOHTTP][aiohttp-icon]][aiohttp-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* poetry ([Official Documentation Installation](https://python-poetry.org/docs/#installation))
* pre-commit
  ```sh
  make install-pre-commit-mac-os
  ```
* python > 3.10 ([Official Documentation Installation](https://www.python.org/downloads/))

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/artusiep/files_downloader.git
   ```
2. Install PIP packages and change shell to use virtual-env
   ```sh
   poetry install
   poetry shell
   # OR
   make install
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Help Usage:
After changing shell to use virtual-env
```
 python main.py --help
```

### Example Usage
Example `input.txt`:
```
https://cdn-9.motorsport.com/images/mgl/24vA3r46/s500/max-verstappen-red-bull-racing-1.webp
https://cdn-8.motorsport.com/images/mgl/24vA4nA6/s500/daniel-ricciardo-mclaren-1.webp
https://cdn-8.motorsport.com/images/mgl/0L1nLWJ2/s500/lando-norris-mclaren-1.webp
```

The download directory should be provided as a command line parameter.

And then execution: `python main.py example.txt data/output -p -s`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/artusiep/files_downloader](https://github.com/artusiep/files_downloader)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/artusiep/files_downloader.svg?style=for-the-badge
[contributors-url]: https://github.com/artusiep/files_downloader/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/artusiep/files_downloader.svg?style=for-the-badge
[forks-url]: https://github.com/artusiep/files_downloader/network/members
[stars-shield]: https://img.shields.io/github/stars/artusiep/files_downloader.svg?style=for-the-badge
[stars-url]: https://github.com/artusiep/files_downloader/stargazers
[issues-shield]: https://img.shields.io/github/issues/artusiep/files_downloader.svg?style=for-the-badge
[issues-url]: https://github.com/artusiep/files_downloader/issues
[license-shield]: https://img.shields.io/github/license/artusiep/files_downloader.svg?style=for-the-badge
[license-url]: https://github.com/artusiep/files_downloader/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/artur-siepietowski/
[python-icon]: https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/360px-Python.svg.png
[python-url]: https://www.python.org
[poetry-icon]: https://python-poetry.org/images/logo-origami.svg
[poetry-url]: https://python-poetry.org/


[aiohttp-url]: https://docs.aiohttp.org/en/stable/
[aiohttp-icon]: https://img.shields.io/pypi/implementation/aiohttp?style=for-the-badge
