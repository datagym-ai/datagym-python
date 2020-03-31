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

============
Requirements
============

* **Python Version:** Python 3.6, 3.7, 3.8, or later
* **DataGym Account**: If you haven't got a DataGym account yet, please SignUp_:
    .. _SignUp: https://www.datagym.ai/pricing/
* **Initial Project:** `Setup your first Project`_ and/or label some images in your Dummy Project
    .. _`Setup your first Project`: https://www.datagym.ai/pricing/
* **API Token:** In order to access your Dummy Project via our Python API you need to `create an API Token`_
    .. _`create an API Token`: https://docs.datagym.ai/documentation/api-token/manage-api-token#create-tokens


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