# Utility Functions Repository

## Overview

* A collection of optimized reusable utility functions for various tasks.
* View author details [at the bottom.](#authors)


## Installation

To install the utility functions, run:

```bash
pip install git+https://github.com/vatsal1306/vatsal.git
```

or, you can directly install from pip.

```bash
pip install vatsal
```

## Usage

### Path operations
Import `utils.Path` class and use its methods for file operations.

```python
from vatsal.utils import Path

# Validates path. If valid path, returns path in string, else returns FileNotFoundError.
obj = Path('/valid/path')
print(obj)

# Read file content. Optional mode and encoding params.
content = Path.read('/valid/path')

# Write to file. Optional mode and encoding params.
Path.write('/valid/path', "Hello world!")

# Append to file
Path.append('/valid/path', "Append text.")

# Get a list of all custom methods for Path .
obj.__dir__()
```

### Wrappers
Use `Wrappers` class for using decorators.
```python
from vatsal.utils import Wrappers


# Make any class method as a private method. Use private_method this as decorator, then that method can only be called internally by class. It cannot be used outside the class or by class object.
class DemoClass:
	@Wrappers.private_method
	def func(self):
		print("This is a private method.")
		

# Make any class as a singleton class. Singleton class is only initialized once. Wrapping @singleton on a class will make sure the class __init__ is only called once. On initialzing the class again, it will return the previously initialized object.
@Wrappers.singleton
class DemoClass:
	def __init__(self):
		print("Inside init method.")

obj1 = DemoClass()  # This will print 'Inside init method.'
obj2 = DemoClass()  # This will not print anything because DemoClass is already initialized once.
```

### Config
Use `Config` class to read .ini file. It will read all the sections and return a variable with .ini data in key-value pairs (dictionary).
```python
from vatsal.utils import Config

config = Config('/path/to/config.ini')
print(config['key'])	# prints value for key.
```

### Progress tracking

Use the `ProgressPercentage` class for real time file upload data in bytes.

```python
from vatsal.utils import ProgressPercentage
import boto3

# Initialize a ProgressPercentage object
progress = ProgressPercentage('file.txt')

# Upload file to S3 with progress tracking
s3 = boto3.client('s3')
s3.upload_file('file.txt', 'bucket-name', 'object-name', Callback=progress)
```

## Contributing

Contributions are welcome. To contribute:
1. Fork the repository.
2. Create a new branch.
3. Make changes and commit.
4. Submit a pull request.

## Authors

*   [Vatsal Vadodaria](https://pypi.org/user/vatsal1399/)
	+ [Github](https://github.com/vatsal1306)
	+ [LinkedIn](https://www.linkedin.com/in/vatsalvadodaria/)