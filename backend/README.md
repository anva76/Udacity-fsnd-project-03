# Coffee Shop Backend

## Setting up the Backend

### Prerequisites

* **Python 3.7 or higher** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

* **Virtual Environment** - It is recommended to use a python virtual environment for running the backend Flask code. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### Installing PIP Dependencies

In your terminal, navigate to the `/backend` directory and create a virtual environment by executing:

```bash
virtualenv venv
```
Then activate the newly created environment:

```bash
source venv/bin/activate
```
Install PIP dependencies:

```bash
pip install -r requirements.txt
```
## Running the server

Before running the backend server, please ensure that you are in the `/backend` folder and your virtual environment is activated as described above. Also, please specify the necessary parameters in the config.py.

To run the backend Flask server, execute:

```bash
python app.py
```
## Running tests in Postman

Before running tests in Postman, please restart the backend server to recreate tables and insert some example data.

