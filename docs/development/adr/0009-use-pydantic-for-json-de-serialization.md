# 9. Use pydantic for JSON (de-)serialization

Date: 2020-06-09

## Status

Accepted

## Context

In order to interact with a remote workspace, for example, at structurizr.com.
The remote or local workspace has to be (de-)serialized from or to JSON.

## Decision

In order to perform these operations we choose
[pydantic](https://pydantic-docs.helpmanual.io/) which has a nice API, active
community, good data validation, helpful documentation, and good performance.

## Consequences

We separate the models representing Structurizr entities and their business
logic from how those models are (de-)serialized. That means that for each model
we have a corresponding IO pydantic model describing the JSON data model.

