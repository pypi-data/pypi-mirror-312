from __future__ import annotations

import logging
import sys
from typing import Any, List

from lsrestclient import LsRestClient

from eventix.contexts import (
    delay_tasks_context_var,
    namespace_context,
    namespace_context_var,
)
from eventix.functions.errors import raise_errors
from eventix.pydantic.event import TEventixEvent
from eventix.pydantic.settings import EventixSettings
from eventix.pydantic.task import TEventixTask

log = logging.getLogger(__name__)


# class EventixClientSession(LsRestClient):
#     def __init__(self, base_url: str = None) -> None:
#         self.client = LsRestClient(base_url, name="")
#         self.base_url = base_url
#         super().__init__()
#
#     def request(
#         self,
#         method,
#         url,
#         *args,
#         **kwargs
#     ) -> Response:  # pragma: no cover
#         return requests.request(
#             method,
#             f"{self.base_url}{url}",
#             *args,
#             **kwargs
#         )


def get_client():
    s = LsRestClient(base_url="nohost://", name="eventix_client")
    # s.headers["Connection"] = "close"
    return s


class EventixClient:
    # interface: Any | None = EventixClientSession()
    interface: Any | None = get_client()
    namespace: str | None = None

    @classmethod
    def set_base_url(cls, base_url):
        if isinstance(cls.interface, LsRestClient):
            log.info(f"Setting EventixClient base_url: {base_url}")
            cls.interface.base_url = base_url

    @classmethod
    def config(cls, config: dict):
        # Be aware that the namespace context is set direct through
        # the context variable.... so no reset possible

        settings = EventixSettings()
        base_url = settings.eventix_url
        if base_url == "":
            log.error("No EVENTIX_URL set.")
            sys.exit()

        cls.set_base_url(base_url)

        namespace = ""
        if "namespace" in config:
            namespace = config["namespace"]

        if namespace == "":
            namespace = settings.eventix_namespace

        if namespace == "":
            log.error("No EVENTIX_NAMESPACE set.")
            sys.exit()

        namespace_context_var.set(namespace)
        if not settings.eventix_delay_tasks:
            log.info(
                "ATTENTION!!!: Delay tasks disabled. All tasks are run directly. No delay."
            )
        delay_tasks_context_var.set(settings.eventix_delay_tasks)

    @classmethod
    def post_event(cls, event: TEventixEvent) -> List[TEventixTask]:
        with namespace_context() as namespace:
            event.namespace = namespace
            r = cls.interface.post(f"/event", body=event.model_dump())
            with raise_errors(r, []):
                json = r.json()
                assert isinstance(json, list)
                return [TEventixTask(**t) for t in json]

    @classmethod
    def ping(cls) -> bool:
        try:
            r = cls.interface.get(f"/healthz")
            return r.status_code == 200
        except Exception as e:
            log.exception("Error while pinging Eventix server.")
            log.error(e)
            return False
