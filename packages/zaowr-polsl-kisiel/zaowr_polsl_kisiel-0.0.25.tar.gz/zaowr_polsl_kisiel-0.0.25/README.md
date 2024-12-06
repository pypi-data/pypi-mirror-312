# ZAOWR Package

<br/>

This is a **ZAOWR** (Zaawansowana Analiza Obrazu, Wideo i Ruchu, eng. _Advanced Image, Video, and Motion Analysis_) Python package used by me and a friend at the university.

PyPI link to the package: <a href="https://pypi.org/project/zaowr-polsl-kisiel/" target="_blank">MAIN PyPI</a>, <a href="https://test.pypi.org/project/zaowr-polsl-kisiel/" target="_blank">TEST PyPI</a>.

<br/>
<br/>

## Table of contents

1. [Windows tutorial](./docs/WINDOWS.md)

2. [RTFM - Use Cases for zaowr_polsl_kisiel and the importance of docstrings](./docs/USE_CASES.md)

3. [Installing the package on Linux using `pip`](#installing-the-package-on-linux-using-pip)

4. [Removing the package on Linux using `pip`](#removing-the-package-on-linux-using-pip)

5. [Creating virtual environment and installing the package](#creating-virtual-environment-and-installing-the-package)

6. [Testing the installation](#testing-the-installation)

7. [Automation: building and uploading with `Makefile` - DEV Tutorial](./docs/DEV_TUTORIAL.md#automation-building-and-uploading-with-makefile---dev-tutorial)

8. [Building package - DEV Tutorial based on official DOCS](./docs/DEV_TUTORIAL.md#building-package---dev-tutorial-based-on-official-docs)

9. [TODO for tracking issues / backlog / progress](./docs/TODO.md) 

10. [Code requirements](#code-requirements)

11. [Sources](#sources)

<br/>
<br/>

## Windows tutorial

The Windows tutorial can be found [here](./docs/WINDOWS.md)

<br/>
<br/>

## RTFM - Use Cases for zaowr_polsl_kisiel and the importance of docstrings

[RTFM here](./docs/USE_CASES.md)

<br/>
<br/>

## Installing the package on Linux using `pip`

<ol>

<li> PyPI MAIN

<br/>
<br/>

```bash
python3 -m pip install --upgrade zaowr-polsl-kisiel
```

</li>
<br/>
<li> TestPyPI

<br/>
<br/>

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --upgrade zaowr-polsl-kisiel
```

</li>

</ol>

<br/>
<br/>


## Removing the package on Linux using `pip`

<br/>

```bash
python3 -m pip uninstall zaowr-polsl-kisiel
```

<br/>
<br/>

## Creating virtual environment and installing the package

<br/>

> [!NOTE]
>
> Complete instructions on managing Python virtual environments
>
> can be found [here](https://github.com/revalew/Python-Venv).

<br/>
<ol>
<li> Create project directory and open it (directory where you will create your files and where the venv will be created). Below is an example of how to do it through Bash - you can also do it through file explorer

<br/>
<br/>

```bash
testDir=/home/user/test
```

```bash
mkdir -p $testDir
```

```bash
cd $testDir
```

<br/>

</li>
<li> Create venv

<br/>
<br/>

```bash
python -m venv ENV_NAME
```

</li>
<br/>

> [!NOTE]
>
> `ENV_NAME` is the name of your venv, so you can change it however you like

<br/>

<li> Activate the venv (while in the project directory)

<br/>
<br/>

```bash
source ENV_NAME/bin/activate
```

or

```bash
. ENV_NAME/bin/activate
```

</li>

<br/>

<li> Install the package from PyPI

<br/>
<br/>

```bash
python3 -m pip install --upgrade zaowr-polsl-kisiel
```

</li>

<br/>

<li> <b>(ADDITIONAL COMMAND)</b> If you want to deactivate the currently active venv

<br/>
<br/>

```bash
deactivate
```

</li>

<br/>

<li> <b>(ADDITIONAL COMMAND)</b> To reactivate the venv, navigate to the path where you created the venv and source it again (command shown above in section number 3)
</li>

</ol>

<br/>
<br/>

## Testing the installation

<br/>

<ul>
<li> Activate the venv (while in the project directory) - <b>Skip this step if you are not using a virtual environment</b>

<br/>
<br/>

```bash
source ENV_NAME/bin/activate
```

or

```bash
. ENV_NAME/bin/activate
```

</li>

<br/>

<li> Launch python

<br/>
<br/>

```bash
python3
```

</li>

<br/>

<li> Import the package

<br/>
<br/>

```python
from zaowr_polsl_kisiel import load_calibration
```

</li>
<br/>

<li> Locate the file with calibration params in tests folder and download it (link below)

<br/>
<br/>

[`./tests/calibration_params/calibration_params.json`](./tests/calibration_params/calibration_params.json)

</li>
<br/>

<li> Try reading the params from file

<br/>
<br/>

```python
# remember to provide appropriate path to the calibration params
calibrationParams = load_calibration("../../tests/calibration_params/calibration_params.json")
```

</li>
<br/>

<li> Display the <code>MSE</code> value to test if the load succeeded

<br/>
<br/>

```python
print(calibrationParams["mse"])
```

</li>
</ul>

<br/>
<br/>


## Code requirements

The code fulfills all the requirements necessary to pass the course. Detailed descriptions of the requirements for each lab are provided in the [`./docs/code_requirements`](./docs/code_requirements/) directory in the form of images (in Polish).

<br/>
<br/>


## Sources

This package has been prepared following [this tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

The publishing to PyPI was created with [this tutorial](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
