# 3. Python 3.6+ only

Date: 2019-02-15

## Status

Accepted

## Context

Python 2 support will be discontinued in 2020. Python 3.6 is the first version
to natively support f-strings which are sweet.

## Decision

We make an early decision to only support Python 3.6 and above.

## Consequences

We have a single code base targetting only one major version. We can use
f-strings such as `f"Hello {name}!"`.
