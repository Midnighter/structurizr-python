# 8. Package structure

Date: 2019-02-15

## Status

Accepted

## Context

We try to structure our package in logical sub-units but we want to maintain a
consistent public interface.

## Decision

We allow for arbitrarily nested sub-packages but export important classes and
functions to the top level thus exposing a public interface. Our unit tests
should reflect this package structure.

## Consequences

Creating many modules and sub-packages can increase complexity of dependencies
internally but will improve separation and use of clearly defined intefaces.
