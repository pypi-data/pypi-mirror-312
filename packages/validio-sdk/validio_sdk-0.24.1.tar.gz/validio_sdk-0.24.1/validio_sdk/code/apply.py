"""Apply command implementation."""

from validio_sdk._api.api import APIClient
from validio_sdk.resource._diff import GraphDiff
from validio_sdk.resource._resource import DiffContext
from validio_sdk.resource._server_resources import apply_updates_on_server


async def apply(
    namespace: str,
    client: APIClient,
    ctx: DiffContext,
    diff: GraphDiff,
    show_secrets: bool,
) -> None:
    """Applies the provided diff operations on the server."""
    await apply_updates_on_server(namespace, ctx, diff, client, show_secrets)
