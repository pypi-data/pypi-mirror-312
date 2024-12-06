
from setuptools import setup, find_packages

long_description = '''
# PyJDK Documentation

PyJDK is a Python utility library that simplifies the process of managing Java Development Kit (JDK) installations, compiling Java code, packaging JAR files, and running Java applications directly from Python. It automates the tedious tasks involved in setting up and using the JDK, allowing developers to focus on writing code.

## Features

- **Automatic JDK Download and Extraction**: Specify the JDK version you need, and PyJDK will handle the download and extraction.
- **Compile Java Code**: Programmatically compile Java source files from Python.
- **Package JAR Files**: Easily package compiled Java classes into executable JAR files.
- **Run JAR Files**: Execute JAR files directly through Python scripts.
- **Cleanup Utilities**: Clean up downloaded files and build directories to save space.

## Installation

Install PyJDK using pip:

```bash
pip install pyjdk
```

## Usage

### Importing PyJDK

```python
from pyjdk import PyJDK
```

### Initializing PyJDK

Create an instance of the `PyJDK` class:

```python
jdk = PyJDK(version=8, logging_enabled=True)
```

- `version`: The JDK version to use (available options are `8`, `11`, or `17`). Default is `8`.
- `logging_enabled`: Enable or disable logging. Default is `False`.

### Listing Available JDK Versions

List all available JDK versions and check their installation status:

```python
jdk.list_versions()
```

### Compiling Java Code

Compile a Java source file:

```python
jdk.compile_code('path/to/YourJavaFile.java')
```

- Replace `'path/to/YourJavaFile.java'` with the actual path to your Java source file.

### Packaging a JAR File

Package compiled classes into a JAR file:

```python
jdk.pack_jar(main_class='com.example.Main', jar_file_path='build/app.jar')
```

- `main_class`: The fully qualified name of the main class (e.g., `com.example.Main`).
- `jar_file_path`: The output path for the JAR file.

### Running a JAR File

Run an existing JAR file:

```python
jdk.run_jar('build/app.jar', args=['arg1', 'arg2'])
```

- `jar_path`: The path to the JAR file you want to run.
- `args`: A list of arguments to pass to the JAR file.

### Cleaning Up

Clean up downloaded JDK files and build directories:

```python
jdk.cleanup()
```

## API Reference

### `PyJDK` Class

- **`__init__(self, version=8, download_dir='jdk_download', extract_dir='jdk_extracted', logging_enabled=False)`**

  Initializes the PyJDK instance.

- **`list_versions(self)`**

  Lists available JDK versions and their installation status.

- **`is_installed(self, version)`**

  Checks if a specific JDK version is installed.

- **`compile_code(self, java_file_path)`**

  Compiles a Java source file.

- **`pack_jar(self, main_class, jar_file_path)`**

  Packages compiled classes into a JAR file.

- **`run_jar(self, jar_path, args=None)`**

  Runs a JAR file with optional arguments.

- **`cleanup(self)`**

  Cleans up download and build directories.

## License

This project is licensed under the MIT License.
'''

setup(
    name="pyjdk",
    version="1.0.0",
    author="Maehdakvan",
    author_email="visitanimation@google.com",
    description="Utilities for using JDK compiling, running on Linux Server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://t.me/maehdak_van",
    project_urls={
        "Bug Tracker": "https://t.me/maehdak_van",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['requests'],
    python_requires='>=3.6'
)