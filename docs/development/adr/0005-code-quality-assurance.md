# 5. Code quality assurance

Date: 2019-02-15

## Status

Accepted

## Context

Writing code that adheres to style guides and other best practices can be
annoying. We want to standardize on some best-in-class tools.

## Decision

We will use isort, black, and flake8.

## Consequences

The tool isort creates well formatted imports. Black is a pedantic tool that
re-formats your code in a particular style. This removes burden from the
individual programmer once they relinquish control. We use flake8 to later check
all style guidelines.
