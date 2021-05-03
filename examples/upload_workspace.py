#!/usr/bin/env python3

# Copyright (c) 2020, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a command line tool for uploading workspace examples."""


import logging
import sys
from importlib import import_module

from structurizr import StructurizrClient, StructurizrClientSettings


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    example = import_module(sys.argv[1])
    workspace = example.main()
    settings = StructurizrClientSettings()
    workspace.id = settings.workspace_id
    client = StructurizrClient(settings=settings)
    with client.lock():
        client.put_workspace(workspace)
