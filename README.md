# BIOMUNE gateway sandbox

This public repository is a deliberately harmless live integration target for the
BIOMUNE privileged deployment gateway.

The workflow does not check out code, read secrets, receive repository permissions,
or call external services. It validates BIOMUNE's three reserved dispatch inputs and
records a successful GitHub Actions run. It must never contain production code or
credentials.

## Render acceptance target

The repository also contains a credential-free HTTP service used to prove BIOMUNE's native Render
connector against a real, disposable provider target. It exposes only:

- `GET /healthz` — exact process health;
- `GET /version` — the `RENDER_GIT_COMMIT` value supplied by Render.

The Render service must have automatic deployments disabled. BIOMUNE then becomes the only normal
path that can request a deployment. The service contains no production code, customer data,
credentials, outbound integrations, or write endpoints.
