from typing import Any

from camel_converter import to_snake

# We need to import the validio_sdk module due to the `eval`
# ruff: noqa: F401
from gql.transport.exceptions import TransportQueryError

import validio_sdk
from validio_sdk._api.api import APIClient
from validio_sdk.exception import ValidioBugError, ValidioError
from validio_sdk.resource._diff import (
    DiffContext,
    GraphDiff,
    ResourceUpdates,
    expand_validator_field_selectors,
    infer_schema_for_source,
)
from validio_sdk.resource._diff_util import (
    must_find_channel,
    must_find_credential,
    must_find_filter,
    must_find_segmentation,
    must_find_source,
    must_find_window,
)
from validio_sdk.resource._resource import Resource, ResourceGraph
from validio_sdk.resource._util import _rename_dict_key, _sanitize_error
from validio_sdk.resource.credentials import (
    AwsAthenaCredential,
    AwsCredential,
    AwsRedshiftCredential,
    AzureSynapseEntraIdCredential,
    AzureSynapseSqlCredential,
    ClickHouseCredential,
    Credential,
    DatabricksCredential,
    DbtCloudCredential,
    DbtCoreCredential,
    DemoCredential,
    GcpCredential,
    KafkaSaslSslPlainCredential,
    KafkaSslCredential,
    LookerCredential,
    MsPowerBiCredential,
    MsPowerBiCredentialAuth,
    MsPowerBiCredentialEntraId,
    PostgreSqlCredential,
    SnowflakeCredential,
    SnowflakeCredentialAuth,
    SnowflakeCredentialKeyPair,
    SnowflakeCredentialUserPassword,
    TableauConnectedAppCredential,
    TableauPersonalAccessTokenCredential,
)
from validio_sdk.resource.filters import Filter
from validio_sdk.resource.notification_rules import Conditions
from validio_sdk.resource.segmentations import Segmentation
from validio_sdk.resource.thresholds import Threshold
from validio_sdk.resource.validators import Reference

# Some credentials depend on other credentials, i.e. wrapping credentials. This
# list contains all of those and can be used when sorting to ensure they always
# end up where you want them.
CREDENTIALS_WITH_DEPENDENCIES = {"DbtCoreCredential", "DbtCloudCredential"}


async def load_resources(namespace: str, client: APIClient) -> DiffContext:
    g = ResourceGraph()
    ctx = DiffContext()

    # Ordering matters here - we need to load parent resources before children
    await load_credentials(namespace, client, g, ctx)
    await load_channels(namespace, client, g, ctx)
    await load_sources(namespace, client, ctx)
    await load_filters(namespace, client, ctx)
    await load_segmentations(namespace, client, ctx)
    await load_windows(namespace, client, ctx)
    await load_validators(namespace, client, ctx)
    await load_notification_rules(namespace, client, ctx)

    return ctx


# ruff: noqa: PLR0915
async def load_credentials(
    # ruff: noqa: ARG001
    namespace: str,
    client: APIClient,
    g: ResourceGraph,
    ctx: DiffContext,
) -> None:
    credentials = await client.get_credentials(
        namespace_id=namespace,
    )

    if not isinstance(credentials, list):
        raise ValidioError("failed to load credentials")

    # Ensure we sort the credentials so the ones that depend on other
    # credentials (wrapping credentials) always comes last.
    credentials.sort(key=lambda c: c["__typename"] in CREDENTIALS_WITH_DEPENDENCIES)

    for c in credentials:
        name = c["resourceName"]
        display_name = c["name"]

        # The 'secret' parts of a credential are left unset since they are not
        # provided by the API. We check for changes to them specially.
        match c["__typename"]:
            case "DemoCredential":
                credential: Credential = DemoCredential(
                    name=name,
                    display_name=display_name,
                    __internal__=g,
                )
            case "DbtCoreCredential":
                credential = DbtCoreCredential(
                    name=name,
                    warehouse_credential=must_find_credential(
                        ctx,
                        c["config"]["warehouseCredential"]["resourceName"],
                    ),
                    display_name=display_name,
                    __internal__=g,
                )
            case "DbtCloudCredential":
                credential = DbtCloudCredential(
                    name=name,
                    account_id=c["config"]["accountId"],
                    api_base_url=c["config"]["apiBaseUrl"],
                    token="UNSET",
                    warehouse_credential=must_find_credential(
                        ctx,
                        c["config"]["warehouseCredential"]["resourceName"],
                    ),
                    display_name=display_name,
                    __internal__=g,
                )
            case "GcpCredential":
                credential = GcpCredential(
                    name=name,
                    credential="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "AwsCredential":
                credential = AwsCredential(
                    name=name,
                    access_key=c["config"]["accessKey"],
                    secret_key="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "PostgreSqlCredential":
                credential = PostgreSqlCredential(
                    name=name,
                    host=c["config"]["host"],
                    port=c["config"]["port"],
                    user=c["config"]["user"],
                    password="UNSET",
                    default_database=c["config"]["defaultDatabase"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "AwsRedshiftCredential":
                credential = AwsRedshiftCredential(
                    name=name,
                    host=c["config"]["host"],
                    port=c["config"]["port"],
                    user=c["config"]["user"],
                    password="UNSET",
                    default_database=c["config"]["defaultDatabase"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "AwsAthenaCredential":
                credential = AwsAthenaCredential(
                    name=name,
                    access_key=c["config"]["accessKey"],
                    secret_key="UNSET",
                    region=c["config"]["region"],
                    query_result_location=c["config"]["queryResultLocation"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "AzureSynapseEntraIdCredential":
                credential = AzureSynapseEntraIdCredential(
                    name=name,
                    host=c["config"]["host"],
                    port=c["config"]["port"],
                    backend_type=c["config"]["backendType"],
                    client_id=c["config"]["clientId"],
                    client_secret="UNSET",
                    database=c["config"]["database"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "AzureSynapseSqlCredential":
                credential = AzureSynapseSqlCredential(
                    name=name,
                    host=c["config"]["host"],
                    port=c["config"]["port"],
                    backend_type=c["config"]["backendType"],
                    username=c["config"]["username"],
                    password="UNSET",
                    database=c["config"]["database"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "ClickHouseCredential":
                credential = ClickHouseCredential(
                    name=name,
                    protocol=c["config"]["protocol"],
                    host=c["config"]["host"],
                    port=int(c["config"]["port"]),
                    username=c["config"]["username"],
                    password="UNSET",
                    default_database=c["config"]["defaultDatabase"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "DatabricksCredential":
                credential = DatabricksCredential(
                    name=name,
                    host=c["config"]["host"],
                    port=c["config"]["port"],
                    access_token="UNSET",
                    http_path=c["config"]["httpPath"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "SnowflakeCredential":
                auth_type = c["config"]["auth"]["__typename"]

                if auth_type == "SnowflakeCredentialUserPassword":
                    auth: SnowflakeCredentialAuth = SnowflakeCredentialUserPassword(
                        user=c["config"]["auth"]["user"],
                        password="UNSET",
                    )
                elif auth_type == "SnowflakeCredentialKeyPair":
                    auth = SnowflakeCredentialKeyPair(
                        user=c["config"]["auth"]["user"],
                        private_key="UNSET",
                        private_key_passphrase="UNSET",
                    )
                else:
                    raise ValidioBugError(f"Unknown Snowflake auth type: '{auth_type}'")

                credential = SnowflakeCredential(
                    name=name,
                    account=c["config"]["account"],
                    auth=auth,
                    warehouse=c["config"]["warehouse"],
                    role=c["config"]["role"],
                    display_name=display_name,
                    __internal__=g,
                )
            case "KafkaSslCredential":
                credential = KafkaSslCredential(
                    name=name,
                    bootstrap_servers=c["config"]["bootstrapServers"],
                    ca_certificate=c["config"]["caCertificate"],
                    client_certificate="UNSET",
                    client_private_key="UNSET",
                    client_private_key_password="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "KafkaSaslSslPlainCredential":
                credential = KafkaSaslSslPlainCredential(
                    name=name,
                    bootstrap_servers=c["config"]["bootstrapServers"],
                    username="UNSET",
                    password="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "LookerCredential":
                credential = LookerCredential(
                    name=name,
                    base_url=c["config"]["baseUrl"],
                    client_id=c["config"]["clientId"],
                    client_secret="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "MsPowerBiCredential":
                entra_id_auth = MsPowerBiCredentialEntraId(
                    client_id=c["config"]["auth"]["clientId"],
                    client_secret="UNSET",
                    tenant_id=c["config"]["auth"]["tenantId"],
                )
                credential = MsPowerBiCredential(
                    name=name,
                    auth=entra_id_auth,
                    display_name=display_name,
                    __internal__=g,
                )
            case "TableauConnectedAppCredential":
                credential = TableauConnectedAppCredential(
                    name=name,
                    host=c["config"]["host"],
                    site=c["config"]["site"],
                    user=c["config"]["user"],
                    client_id=c["config"]["clientId"],
                    secret_id=c["config"]["secretId"],
                    secret_value="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "TableauPersonalAccessTokenCredential":
                credential = TableauPersonalAccessTokenCredential(
                    name=name,
                    host=c["config"]["host"],
                    site=c["config"]["site"],
                    token_name=c["config"]["tokenName"],
                    token_value="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case _:
                raise ValidioError(
                    f"unsupported credential '{name}' of type '{type(c)}'"
                )

        credential._id.value = c["id"]
        credential._namespace = c["namespace"]["id"]

        ctx.credentials[name] = credential


async def load_channels(
    namespace: str,
    client: APIClient,
    g: ResourceGraph,
    ctx: DiffContext,
) -> None:
    server_channels = await client.get_channels(namespace_id=namespace)

    if not isinstance(server_channels, list):
        raise ValidioError("failed to load channels")

    for ch in server_channels:
        name = ch["resourceName"]

        cls = eval(f'validio_sdk.resource.channels.{ch["__typename"]}')
        channel = cls(
            **{
                **{to_snake(k): v for k, v in ch["config"].items()},
                "name": name,
                "display_name": ch["name"],
                "__internal__": g,
            }
        )
        channel._id.value = ch["id"]
        channel._namespace = ch["namespace"]["id"]
        ctx.channels[name] = channel


async def load_notification_rules(
    namespace: str,
    client: APIClient,
    ctx: DiffContext,
) -> None:
    rules = await client.get_notification_rules(namespace_id=namespace)

    if not isinstance(rules, list):
        raise ValidioError("failed to load rules")

    for r in rules:
        name = r["resourceName"]

        cls = eval(f'validio_sdk.resource.notification_rules.{r["__typename"]}')

        rule = cls(
            name=name,
            channel=must_find_channel(ctx, r["channel"]["resourceName"]),
            conditions=Conditions._new_from_api(ctx, r["conditions"]),
            display_name=r["name"],
        )
        rule._id.value = r["id"]
        rule._namespace = r["namespace"]["id"]
        ctx.notification_rules[name] = rule


async def load_sources(
    namespace: str,
    client: APIClient,
    ctx: DiffContext,
) -> None:
    server_sources = await client.get_sources(namespace_id=namespace)

    if not isinstance(server_sources, list):
        raise ValidioError("failed to load sources")

    for s in server_sources:
        name = s["resourceName"]

        # Internally we call schema db_schema on our source objects but the API
        # calls them schema so change them before trying to construct the class.
        source_config = s.get("config", {})
        _rename_dict_key(source_config, "schema", "db_schema")
        _rename_dict_key(source_config.get("messageFormat", {}), "schema", "db_schema")

        cls = eval(f'validio_sdk.resource.sources.{s["__typename"]}')
        source = cls(
            **{
                **{to_snake(k): v for k, v in source_config.items()},
                "name": name,
                "display_name": s["name"],
                "credential": must_find_credential(
                    ctx, s["credential"]["resourceName"]
                ),
                "jtd_schema": s["jtdSchema"],
                "description": s["description"],
            }
        )
        source._id.value = s["id"]
        source._namespace = s["namespace"]["id"]
        ctx.sources[name] = source


async def load_segmentations(
    namespace: str,
    client: APIClient,
    ctx: DiffContext,
) -> None:
    server_segmentations = await client.get_segmentations(namespace_id=namespace)

    if not isinstance(server_segmentations, list):
        raise ValidioError("failed to load segmentations")

    for s in server_segmentations:
        name = s["resourceName"]

        filter_ = (
            must_find_filter(ctx, s["filter"]["resourceName"]) if s["filter"] else None
        )
        segmentation = Segmentation(
            name=name,
            source=must_find_source(ctx, s["source"]["resourceName"]),
            fields=s["fields"],
            filter=filter_,
            display_name=s["name"],
        )

        segmentation._id.value = s["id"]
        segmentation._namespace = s["namespace"]["id"]
        ctx.segmentations[name] = segmentation


async def load_windows(
    namespace: str,
    client: APIClient,
    ctx: DiffContext,
) -> None:
    server_windows = await client.get_windows(namespace_id=namespace)

    if not isinstance(server_windows, list):
        raise ValidioError("failed to load windows")

    for w in server_windows:
        name = w["resourceName"]

        cls = eval(f'validio_sdk.resource.windows.{w["__typename"]}')

        data_time_field = (
            {"data_time_field": w["dataTimeField"]} if "dataTimeField" in w else {}
        )

        window = cls(
            **{
                **{to_snake(k): v for k, v in w.get("config", {}).items()},
                "name": name,
                "display_name": w["name"],
                "source": must_find_source(ctx, w["source"]["resourceName"]),
                **data_time_field,
            }
        )

        window._id.value = w["id"]
        window._namespace = w["namespace"]["id"]
        ctx.windows[name] = window


async def load_filters(
    namespace: str,
    client: APIClient,
    ctx: DiffContext,
) -> None:
    server_filters = await client.get_filters(namespace_id=namespace)

    if not isinstance(server_filters, list):
        raise ValidioError("failed to load filters")

    for f in server_filters:
        name = f["resourceName"]

        cls = eval(f'validio_sdk.resource.filters.{f["__typename"]}')

        filter_ = cls(
            **{
                **{to_snake(k): v for k, v in f.get("config", {}).items()},
                "name": name,
                "source": must_find_source(ctx, f["source"]["resourceName"]),
                "display_name": f["name"],
            }
        )

        filter_._id.value = f["id"]
        filter_._namespace = f["namespace"]["id"]
        ctx.filters[name] = filter_


# Takes in a graphql Threshold type
def convert_threshold(t: dict[str, Any]) -> Threshold:
    cls = eval(f'validio_sdk.resource.thresholds.{t["__typename"]}')

    # Threshold parameters map 1-1 with resources, so
    # we call the constructor directly.
    return cls(**{to_snake(k): v for k, v in t.items() if k != "__typename"})


# Takes in a graphql ReferenceSourceConfig type
def convert_reference(ctx: DiffContext, r: dict[str, Any]) -> Reference:
    source = must_find_source(ctx, r["source"]["resourceName"])
    window = must_find_window(ctx, r["window"]["resourceName"])

    maybe_filter = (
        must_find_filter(ctx, r["sourceFilter"]["resourceName"])
        if "sourceFilter" in r and r["sourceFilter"]
        else None
    )

    return Reference(
        source=source,
        window=window,
        history=r["history"],
        offset=r["offset"],
        filter=maybe_filter,
    )


async def load_validators(
    namespace: str,
    client: APIClient,
    ctx: DiffContext,
) -> None:
    validators = await client.get_validators(
        namespace_id=namespace,
    )

    if not isinstance(validators, list):
        raise ValidioError("failed to load validators")

    for v in validators:
        name = v["resourceName"]
        display_name = v["name"]
        description = v["description"]
        config = v["config"]

        window = must_find_window(ctx, v["sourceConfig"]["window"]["resourceName"])
        segmentation = must_find_segmentation(
            ctx, v["sourceConfig"]["segmentation"]["resourceName"]
        )
        threshold = convert_threshold(config["threshold"])
        maybe_reference = (
            {"reference": convert_reference(ctx, v["referenceSourceConfig"])}
            if "referenceSourceConfig" in v
            else {}
        )
        maybe_filter = (
            {
                "filter": must_find_filter(
                    ctx,
                    v["sourceConfig"]["sourceFilter"]["resourceName"],
                )
            }
            if "sourceFilter" in v["sourceConfig"] and v["sourceConfig"]["sourceFilter"]
            else {}
        )

        # Volume validator still have a deprecated field that we use. It's
        # called sourceField in the API still but `optional_source_field` on
        # the resource class so we rename it here.
        if v["__typename"] == "VolumeValidator":
            _rename_dict_key(config, "sourceField", "optionalSourceField")

        config = {to_snake(k): v for k, v in config.items() if k != "threshold"}

        cls = eval(f'validio_sdk.resource.validators.{v["__typename"]}')

        validator = cls(
            **{
                **config,
                **maybe_reference,
                **maybe_filter,
                "threshold": threshold,
                "name": name,
                "window": window,
                "segmentation": segmentation,
                "display_name": display_name,
                "description": description,
            }
        )
        validator._id.value = v["id"]
        validator._namespace = v["namespace"]["id"]
        ctx.validators[name] = validator


async def apply_updates_on_server(
    namespace: str,
    ctx: DiffContext,
    diff: GraphDiff,
    client: APIClient,
    show_secrets: bool,
) -> None:
    try:
        await apply_deletes(namespace=namespace, deletes=diff.to_delete, client=client)

        # We perform create operations in two batches. First here creates top
        # level resources, then after performing updates, we create any remaining
        # resources. We do this due to a couple scenarios
        # - A resource potentially depends on the parent to be created first before
        #   it can be updated. Example is a notification rule that is being
        #   updated to reference a Source that is to be created. In such cases,
        #   we need to apply the create on parent resource before the update on
        #   child resource.
        # - Conversely, in some cases, a parent resource needs to be updated before
        #   the child resource can be created. e.g a validator that is referencing a
        #   new field in a schema needs the source to be updated first otherwise diver
        #   will reject the validator as invalid because the field does not yet exist.
        #
        # So, here we create the top level resources first - ensuring that any child
        # resource that relies on them are resolved properly.
        # We start with creating credentials only. Since sources need them to infer
        # schema.
        await apply_creates(
            namespace=namespace,
            manifest_ctx=ctx,
            creates=DiffContext(
                credentials=diff.to_create.credentials,
            ),
            client=client,
            show_secrets=show_secrets,
        )

        # Resolve any pending source schemas now that we have their credential.
        for source in diff.to_create.sources.values():
            if source.jtd_schema is None:
                await infer_schema_for_source(
                    manifest_ctx=ctx, source=source, client=client
                )

        # Create the remaining top level resources.
        await apply_creates(
            namespace=namespace,
            manifest_ctx=ctx,
            creates=DiffContext(
                sources=diff.to_create.sources,
                channels=diff.to_create.channels,
            ),
            client=client,
            show_secrets=show_secrets,
        )

        # Now we should have all source schemas available. We can expand
        # field selectors.
        expand_validator_field_selectors(ctx)

        # Then apply updates.
        await apply_updates(
            namespace=namespace, manifest_ctx=ctx, updates=diff.to_update, client=client
        )

        # Then apply remaining creates. Resources that have been created in
        # the previous steps are marked as _applied, so they will be skipped this
        # time around.
        await apply_creates(
            namespace=namespace,
            manifest_ctx=ctx,
            creates=diff.to_create,
            client=client,
            show_secrets=show_secrets,
        )
    except Exception as e:
        raise e


# ruff: noqa: PLR0912
async def apply_deletes(
    namespace: str, deletes: DiffContext, client: APIClient
) -> None:
    # Delete notification rules first These reference sources so we
    # remove them before removing the sources they reference.
    for r in deletes.notification_rules.values():
        await _delete_resource(r, client)

    # For pipeline resources, start with sources (This cascades deletes,
    # so we don't have to individually delete child resources).
    for s in deletes.sources.values():
        await _delete_resource(s, client)

    # For child resources, we only need to delete them if their parent
    # haven't been deleted.
    for w in deletes.windows.values():
        if w.source_name not in deletes.sources:
            await _delete_resource(w, client)

    for sg in deletes.segmentations.values():
        if sg.source_name not in deletes.sources:
            await _delete_resource(sg, client)

    for v in deletes.validators.values():
        if v.source_name not in deletes.sources:
            await _delete_resource(v, client)

    for f in deletes.filters.values():
        if f.source_name not in deletes.sources:
            await _delete_resource(f, client)

    # Finally delete credentials - these do not cascade so the api rejects any
    # delete requests if there are existing child resources attached to a credential.
    for c in deletes.credentials.values():
        await _delete_resource(c, client)

    for ch in deletes.channels.values():
        await _delete_resource(ch, client)


async def _delete_resource(resource: Resource, client: APIClient) -> None:
    if resource._applied:
        return
    resource._applied = True
    await resource._api_delete(client)


async def apply_creates(
    namespace: str,
    manifest_ctx: DiffContext,
    creates: DiffContext,
    client: APIClient,
    show_secrets: bool,
) -> None:
    # Creates must be applied top-down, parent first before child resources
    credentials = list(creates.credentials.values())

    # Ensure we sort the credentials so the ones that depend on other
    # credentials (wrapping credentials) always comes last.
    credentials.sort(key=lambda c: type(c) in CREDENTIALS_WITH_DEPENDENCIES)

    all_resources: list[list[Resource]] = [
        list(credentials),
        list(creates.sources.values()),
        list(creates.filters.values()),
        list(creates.segmentations.values()),
        list(creates.windows.values()),
        list(creates.validators.values()),
        list(creates.channels.values()),
        list(creates.notification_rules.values()),
    ]
    for resources in all_resources:
        for r in resources:
            if r._applied:
                continue

            try:
                await r._api_create(namespace, client, manifest_ctx)
                r._applied = True
            except TransportQueryError as e:
                raise (
                    _sanitize_error(e, show_secrets) if isinstance(r, Credential) else e
                )


async def apply_updates(
    namespace: str,
    manifest_ctx: DiffContext,
    updates: ResourceUpdates,
    client: APIClient,
) -> None:
    all_updates = [
        list(updates.credentials.values()),
        list(updates.sources.values()),
        list(updates.filters.values()),
        list(updates.segmentations.values()),
        list(updates.windows.values()),
        list(updates.validators.values()),
        list(updates.channels.values()),
        list(updates.notification_rules.values()),
    ]

    for up in all_updates:
        for u in up:
            if u.manifest._applied:
                continue
            u.manifest._applied = True

            await u.manifest._api_update(namespace, client, manifest_ctx)
