# Citation Counter

Simple Python script which counts the citations in a set of publications. The idea is to find other interesting publications that are heavily linked with the already present ones. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary dependencies.

```bash
pip install -r requirements.txt
```

### OS Dependencies

Debian, Ubuntu, and friends:

```
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
```

Fedora, Red Hat, and friends:

```
sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python-devel redhat-rpm-config
```

macOS:

```
brew install pkg-config poppler
brew install libmagic
```

Conda users may also need `libgcc`:

```
conda install libgcc
```

## Usage

```bash
python count_citations.py -d /Directory/To/Publications 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)