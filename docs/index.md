# Structurizr for Python

A Python client package for the [Structurizr](https://structurizr.com/) cloud
service and on-premises installation.

## Installation

For the moment, the main installation method is from PyPI, for example, using
`pip`.

```
pip install structurizr-python
```

## Getting Started

There are two starting points. Either you have no Structurizr workspace or you
have an existing workspace that you want to modify locally.

1. If you don't have a workspace yet, you can sign up for one at
   [Structurizr](https://structurizr.com/help/getting-started).  Once you have a
   workspace, take note of its ID, API key, and secret. In order to get started
   with creating a new workspace, take a look at [the
   examples](https://github.com/Midnighter/structurizr-python/tree/devel/examples).
   In particular the
   [getting-started](https://github.com/Midnighter/structurizr-python/blob/devel/examples/getting_started.py)
   script will be suitable.

    The `#!python main()` function in each example script creates a more or less
    involved workspace for you.  When you have created a workspace, it is time
    to upload it so that you can create diagrams for it.  You will need to
    create a
    [`StructurizrClient`][structurizr.api.structurizr_client.StructurizrClient]
    instance and its
    [settings][structurizr.api.structurizr_client_settings.StructurizrClientSettings].
    The settings can be provided as arguments, be read from environment
    variables, or be provided in a `.env` file.
 
    ```python
    from structurizr import StructurizrClient, StructurizrClientSettings
 
    workspace = main()
    settings = StructurizrClientSettings(
        workspace_id=1234,
        api_key='your api key',
        api_secret='your api secret',
    )
    client = StructurizrClient(settings=settings)
    client.put_workspace(workspace)
    ```
 
    The example should now be available in your online workspace.

2. In case you already have a comprehensive workspace online, the Python client
   can help with creating local copies and modifying it.

    ```python
    from structurizr import StructurizrClient, StructurizrClientSettings
 
    settings = StructurizrClientSettings(
        workspace_id=1234,
        api_key='your api key',
        api_secret='your api secret',
    )
    client = StructurizrClient(settings=settings)
    workspace = client.get_workspace()
    ```
 
    You can then modify the workspace as you please and upload your new version
    as shown above.

## Copyright

* Copyright © 2020, Moritz E. Beber.
* Free software distributed under the [Apache Software License
  2.0](https://www.apache.org/licenses/LICENSE-2.0).
