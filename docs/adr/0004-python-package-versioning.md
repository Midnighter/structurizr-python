# 4. Python package versioning

Date: 2019-02-15

## Status

Accepted

## Context

We need a simple way to manage our package version.

## Decision

We use versioneer to do this for us.

## Consequences

We can create new release versions simply by creating a corresponding git tag.
Currently, if you want to do a local `pip install .`, this only works for
pip<19.
