# wtwco-igloo-cloud-api-client

A python client library for Igloo Cloud API v2.
Please note, for most use cases we recommend using the [wtwco-igloo](https://pypi.org/project/wtwco-igloo/) package as it provides many useful methods on top of the API.

## Installation

Note, we assume you have Python 3.9 or later already installed on your machine. If not, please download and install the latest version of Python from the [official website](https://www.python.org/downloads/).
Also note, we recommend that you perform the installation within a Python virtual environment. [See here for more info](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

Once created, please activate your virtual environment and install the Igloo Python Connector package using the following command:

```shell
pip install wtwco-igloo-cloud-api-client
```

You should now be able to import the package in your Python code:

```python
import wtwco_igloo_cloud_api_client
```

## Connecting to the API

First create an authenticated client:

```python
from wtwco_igloo_cloud_api_client import AuthenticatedClient

client = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")
```

View your projects:

```python
from wtwco_igloo_cloud_api_client.models import Project
from wtwco_igloo_cloud_api_client.api.projects import get_projects
from wtwco_igloo_cloud_api_client.types import Response

with client as client:
    my_data: Project = get_projects.sync(client=client)
    # or if you need more info (e.g. status_code)
    response: Response[Project] = get_projects.sync_detailed(client=client)
```

## Documentation and Examples

For documentation and examples please see [WTW Client Services](https://clientservices.insurancetechnology.com/).
