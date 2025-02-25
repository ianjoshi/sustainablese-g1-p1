# SustainableSE Group 1 Project 1
This repository is home to the Project 1 source code of Group 1, for the [Sustainable Software Engineering](https://studiegids.tudelft.nl/a101_displayCourse.do?course_id=70145) course at TU Delft. The core purpose of this source code is to analyse Eneregy Consumption of Regular Expression (RegEx) engines, commonly used by modern IDEs.

## Table of Contents
- [Setup Environment](#setup-environment)
  * [Using venv (Virtual Environment)](#using-venv-virtual-environment)
  * [Using Conda](#using-conda)
- [Get Data (TODO)](#get-data)
- [Verify the different RegEx Engines work](#verify-the-different-regex-engines-work)
  * [Find what is missing](#find-what-is-missing)
  * [Install Java Development Kit (JDK)](#install-java-development-kit-jdk)
  * [Install C++ compiler & Boost-Regex](#install-c-compiler--boost-regex)
  * [Install Node.js](#install-nodejs)
- [Run main.py](#run-mainpy)
- [Get Results](#get-results)
- [Visualise Results (TODO)](#visualise-results)
 

## Setup Environment
0. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

1. Set up Python environment (choose one method):

   ### Using venv (Virtual Environment)
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

   ### Using Conda
   ```bash
   # Create and activate conda environment
   conda env create -f environment.yml
   conda activate regex_energy_experiment
   ```


## Get Data
TODO

## Verify the different RegEx Engines work
Ensure you are able to run java, node.js, and c++ files from this directory on your computer with the following steps.

### Find what is missing
Run the test file to check if all engines are working:
```bash
python test_regex_engines.py
```

Note: You may notice in the `test_regex_engines.py` that the following code snippet has comments 'Depends on compiler' and 'Depends on vcpkg installation path'. 
```python
 def test_boost_engine_pipe_interaction(self):
        boost_path = "C:/dev/vcpkg/installed/x64-mingw-dynamic" # Depends on vcpkg installation path
        
        # Print the directory contents to debug
        print("Checking library directory:")
        subprocess.run(["dir", f"{boost_path}/lib"], shell=True)
        
        compile_result = subprocess.run([
            "g++", # Depends on compiler
            f"{self.factory.directory_to_store_engines}/regex_matcher.cpp",
            "-o", f"{self.factory.directory_to_store_engines}/regex_matcher.exe",
            f"-I{boost_path}/include",
            f"-L{boost_path}/lib",
            "-Wl,-rpath," + boost_path + "/bin",
            "-lboost_regex-gcc10-mt-x64-1_86",  # Depends on compiler
            "--verbose"
        ], capture_output=True, text=True)

        # Rest of function
```

These lines you might have to adjust based on the system you're running the script on.

### Install Java Development Kit (JDK)
* Windows: https://docs.oracle.com/en/java/javase/22/install/installation-jdk-microsoft-windows-platforms.html

* macOS: https://docs.oracle.com/en/java/javase/22/install/installation-jdk-macos.html

* Linux: https://docs.oracle.com/en/java/javase/22/install/installation-jdk-linux-platforms.html


### Install C++ compiler & Boost-Regex
You have a few options in terms of the compiler you choose to install here. And this will affect the exact install of the boost-regex library.

**Compilers:**

* TDM-GCC: https://jmeubank.github.io/tdm-gcc/download/

* MSVC: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170

* Others: TODO


**VCPKG:**

Install:
```bash
cd C:\dev
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
```

*For windows:* Add to path by running Powershell as Administrator:
```bash
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\path\to\vcpkg",
    "Machine"
)
```

*For Linux/macOS:* Add to path by adding this line to your shell configuration file (~/.bashrc, ~/.zshrc, etc.):
```bash
export PATH=$PATH:/path/to/vcpkg
```

Then reload your shell configuration:
```bash
source ~/.bashrc  # If using bash
# OR
source ~/.zshrc   # If using zsh
```

Test if it works in new terminal window:
```
vcpkg version
```

**Boost-Regex:**

If TDM-GCC is compiler: run 
```bash 
vcpkg install boost-regex:x64-mingw-dynamic
```

### Install Node.js
Go to: https://nodejs.org/en/download

## Run `main.py`
Finally you can run the experiment by running:
```bash
python main.py
```

## Get Results
When running `main.py`, results will be generated in the results directory.

## Visualise Results
TODO
