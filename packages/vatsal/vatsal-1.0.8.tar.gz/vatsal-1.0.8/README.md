# Utility Functions Repository

## Overview

* A collection of reusable utility functions for various tasks, including [file operations](#file-operations) and [progress tracking](#progress-tracking).
* View author details [here](#authors)


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

### File operations
Import `utils.File` class and use its methods for file operations.

```python
from vatsal.utils import File

# Initialize a File object
file = File('/path/to/file.txt')

# Read file content
content = file.read()

# Write to file
file.write('Hello, world!')

# Append to file
file.append('Appended text')

# Print file information
print(file)
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