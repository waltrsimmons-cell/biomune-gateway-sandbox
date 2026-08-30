# BIOMUNE gateway sandbox

This public repository is a deliberately harmless live integration target for the
BIOMUNE privileged deployment gateway.

The workflow does not check out code, read secrets, receive repository permissions,
or call external services. It validates BIOMUNE's three reserved dispatch inputs and
records a successful GitHub Actions run. It must never contain production code or
credentials.
