# 6. Code Testing

Date: 2019-02-15

## Status

Accepted

## Context

Setting up different testing environments and configurations can be a painful
and error prone process.

## Decision

We use tox to define, configure, and run different test scenarios.

## Consequences

Using tox means every developer will have reproducible test scenarios even
though it causes a slight burden in proper configuration.
