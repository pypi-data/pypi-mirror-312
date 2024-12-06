# The Genovation python toolbox

This python tool-box is supposed to help Genovation associates in their day-to-day work.

## Install

# How to - Install

* Upgrade the `com-enovation-murex` tool-box:
  * `pip uninstall com-enovation-murex`
  * `pip install ./com-enovation-murex-0.0.1.tar.gz`

## Pre-requisites

* Windows PowerShell
  * Console to run `mx` tool box, and its commands
  * How-to from Microsoft: https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows

* Python:
  * `mx` is tested with Python 3.11
  * As of July 2023, Python 3.11.4 is available at: https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
  * Note: starting with Python 3.4, `pip` is by default included

Once installed, you can check in PowerShell:
```console
foo@bar:~$ python --version
           >> Python 3.11.0
foo@bar:~$ pip --version
           >> pip 23.2.1 from C:\Users\xxx\AppData\Local\Programs\Python\Python311\Lib\site-packages\pip (python 3.11)
```

## Install package `enov-murex`

In Windows PowerShell, from a directory where distribution files are stored (aka enov_murex-?.?.?-py3-none-any.whl), type the command
```console
foo@bar:~$ pip install .\enov_murex-?.?.?-py3-none-any.whl
           >> (…)
           >> Installing collected packages: com-enovation, enov-murex
           >> Successfully installed com-enovation-?.?.? enov-murex-?.?.?
```

Once installed, you can check in PowerShell:
```console
foo@bar:~$ mx
           >> Usage: mx [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...
           >> Options:
           >>   --verbose / --no-verbose  Level of logging verbosity: INFO (--verbose),
           >>                             WARNING (default) or ERROR (--no-verbose).
           >>   --help                    Show this message and exit.
           >> 
           >> Commands:
           >>   (…)
           >>   dict-load-json     Load json file into a dictionary that is labelled...
           >>   (…)
           >>   dict-set-json      Set a DICTIONARY provided as as an argument as an...
           >>   (…)
           >>   mx-sp-dh           MUREX: Enrich the Service Presale pipeline: - Loads...
           >>   mx-sp-pl           MUREX: Produces and distributes reports on service...
           >>   (…)
```

## Commands

| Building Blocks         | Command                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:------------------------|:-------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Data Handler`          | `mx-sp-dh`                     | To prepare data<ul><li>As an input, data extracted from Qlik</li><li>Command verifies/ cleanses/ enriches data<ul><li>Configuration file is under: enov\murex\presale\mx_sp_dh_data_handler\DataHandlerConfigurationFile.json</li></ul></li><li>As an output, verified/ cleansed/ enriched data that can be used to produce reports</li></ul>                                                                                                                                                                                                       |
| `Pipelinizer`           | `mx-sp-pl`                     | To produce Excel dashboard<ul><li>As an input, data extracted from Qlik verified/ cleansed/ enriched</li><li>Library selects data, produces excel dashboard and persists into file system<ul><li>configuration file is under: enov\murex\presale\mx_sp_pl_pipelinizer\DistributionConfigurationFile.json</li></ul></li><li>As an output, excel reports produced and persisted in file system</li></ul>Limitations: performance is poor. A possible optimization is identified that could reduce the timing by 10 times, but is not yet implemented. |
| `Documentation Manager` | `mx-sp-dm-bd`<br>`mx-sp-dm-pp` | To report on documentations stored in SharePoints<ul><li>Business Development Document Repository: for materials produced across opportunities</li><li>Positioning and Promotion: for Tools, Templates and Accelerators</li></ul>                                                                                                                                                                                                                                                                                                                   |



---

# The technicalities

## Versions

* 0.1.0, as of 02-Jul-2023: workable version
* 0.1.1, as of 08-Jul-2023: added SPLC and predictability data. No KPI nor digest yet.
* 0.1.2, as of 26-Aug-2023: added documentation management for SharePoint Positioning and Promotion
* 0.1.3, as of 10-Sep-2023: resynchronized with com-enovation.0.0.40: adaptation to latest version for pandas.dataframe and to_datetime function which becomes stricter, packaging setup.cfg to project.toml, tests refactoring

## Dependencies

| Dependencies    | Description                                                                                                            |
|:----------------|:-----------------------------------------------------------------------------------------------------------------------|
| `com-enovation` | The seed toolbox that we use to initialize this toolbox. To decommission as commands are being re-instantiated here... |
| `typer`         | Library for building CLI applications, based on Click                                                                  |

## Upgrade package `enov-murex`

* Upgrade the `com-enovation-murex` tool-box:
  * `pip uninstall com-enovation-murex`
  * `pip install ./com-enovation-murex-0.0.1.tar.gz`

## Contribute

### Generate the distribution

* build the distribution files and directories: `python3 -m build`
  * Directories `build` and `dist` should be generated

### Pycharm configuration

* Unit test configuration, from menu `Run > Edit Configurations...`
  * `Configuration > Target > Script path: ~/PycharmProjects/com_enovation.murex/tests`
  * `Configuration > Working directory: ~/PycharmProjects/com_enovation.murex/`
  * `Configuration > Add content roots to PYTHONPATH: checked`
  * `Configuration > Add source roots to PYTHONPATH: checked`

### Python stuff

* Check we have latest versions:
  * pip: `python3 -m pip install --upgrade pip`
  * build to generate the distribution: `python3 -m pip install --upgrade build`

* Update packages using pip
  * Check all packages are fine: `pip check`
  * List all packages outdated: `pip list --outdated`
  * Update all packages outdated:
    * On Mac: `pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U`
    * On Windows: `pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}`
* A simple example package. You can use [Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/) to write your content.

### PERSO
rm -rf dist;rm -rf src/enov_murex.egg-info;python3 -m build;pip uninstall -y enov-murex

# CHEAT SHEET

## TYPER

* To get emojis that can be printed by `rich.print()`: run `python -m rich.emoji` in console