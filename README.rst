==================
DataGym Python API
==================

Python API Wrapper for DataGym (https://www.datagym.ai) - the AI-assisted image annotation tool.
You can easily access your Projects, Datasets, Images and labeled data
from the DATAGYM backend through this package.

DATAGYM enables data scientists and machine learning experts to label images up to 10x faster.
AI-assisted annotation tools reduce manual labeling effort, give you more time to finetune ML models and speed up your go to market of new products.

* Free software: BSD license
* Documentation: https://docs.datagym.ai/documentation/python-api/
* GitHub: https://github.com/datagym-ai/datagym-python



First Steps
-----------

Install the package via pip:

.. code-block:: bash

    user@machine:~$ pip install datagym

Create your first DATAGYM API Client:

.. code-block:: python

    from datagym import Client

    client = Client(api_key="<YOUR_API_KEY>")



Features
--------

* Fetch Project, Datasets, Images
* Export labeled data from Projects
* Create Datasets
* Add Datasets to Projects
* Upload/Download images