# clone-auto
Clone auto is a small script to clone all public repositories of a user from platforms like Gitlab, Github or codeberg.

## Requeriments
- python3 >= 3.11
- requests >= 2.32.3

## :file_folder: Installation

### :penguin: Binary dependencies (Unix)
```sh
sudo apt-get install python3 python3-pip python3-setuptools git
```

### Pypi
```sh
python3 -m pip install clone-auto
```

## :computer: Usage
### :clipboard: Clone all my public repositories
```sh
clone_auto -u sivefunc --platforms gitlab codeberg github
```
### :clipboard: Setting up timeout
```sh
clone_auto -u sivefunc --platforms gitlab --timeout 7.77
```

## Supported platforms
<table>
    <tr>
        <td>Name</td>
        <td>Image</td>
    </tr>
    <tr>
        <td>Gitlab</td>
        <td><img src="https://codeberg.org/Sivefunc/clone_auto/raw/branch/master/readme_res/gitlab.png" width="100" height="100"></td>
    </tr>
    <tr>
        <td>Codeberg</td>
        <td><img src="https://codeberg.org/Sivefunc/clone_auto/raw/branch/master/readme_res/codeberg.png" width="100" height="100"></td>
    </tr>
    <tr>
        <td>Github</td>
        <td><img src="https://codeberg.org/Sivefunc/clone_auto/raw/branch/master/readme_res/github.png" width="100" height="100"></td>
    </tr>
 </table>

# Made by :link: [Sivefunc](https://gitlab.com/sivefunc)
# Licensed under :link: [GPLv3](https://codeberg.org/Sivefunc/clone_auto/src/branch/master/LICENSE)
