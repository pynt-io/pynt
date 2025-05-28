"""
Write flow objects to a HAR file
    this file uses the same logic as the HAR export in mitmproxy (savehar.py)
    pynt additions:
        - saves the body of GET requests as well (not supported by mitmproxy)
        - buffered writes *as data comes in*
        - "done" marker written to a different file (`pynt_ready_marker`)
    pynt flags:
        - pynthar
        - pynt_ready_marker

    command:
        mitmdump -s custom_har.py --set pynthar=<path_to_save_har_file> --set pynt_ready_marker=<path_to_marker>

    to run the original mitmproxy har export:
    command:
        mitmdump --set hardump=<path_to_save_har_file>
"""

import base64
import json
from datetime import datetime
from datetime import timezone
from io import TextIOWrapper
from typing import Any

from mitmproxy import ctx
from mitmproxy import exceptions
from mitmproxy import flowfilter
from mitmproxy import http
from mitmproxy.addonmanager import Loader
from mitmproxy.connection import Server
from mitmproxy.coretypes.multidict import _MultiDict
from mitmproxy.utils import human
from mitmproxy.utils import strutils


class HARWriter:
    MAX_SIZE = 1073741824 # 1GB = 1024 * 1024 * 1024
    def __init__(self, har_file_path: str, ready_marker_path: str) -> None:
        self.ready_marker_path = ready_marker_path
        self.entries: list[dict] = []
        self.entries_written = 0
        self.entries_dropped = 0

        self.har_file: TextIOWrapper = open(har_file_path, "w", encoding="utf-8")
        self.bytes_written = self.har_file.write("""{"log":{"version":"1.2","pages":[],"entries":[""")

    def write(self, entry: dict) -> None:
        if self.bytes_written > HARWriter.MAX_SIZE:
            self.entries_dropped += 1
            return

        if self.entries_written > 0:
            self.bytes_written += self.har_file.write(",\n")
        self.bytes_written += self.har_file.write(json.dumps(entry))
        self.entries_written += 1

    def end(self) -> tuple[int, int, int]:
        self.bytes_written += self.har_file.write("]}}")
        self.har_file.flush()
        self.har_file.close()

        if self.ready_marker_path != "":
            with open(self.ready_marker_path, "w", encoding="utf-8") as marker:
                marker.write(json.dumps({
                    "bytes_written": self.bytes_written,
                    "entries_written": self.entries_written,
                    "entries_dropped": self.entries_dropped,
                }))

        return [self.bytes_written, self.entries_written, self.entries_dropped]


class PyntSaveHar:
    def __init__(self) -> None:
        self.filt: flowfilter.TFilter | None = None

        self.servers_seen: set[Server] = set()
        self.har_writer: HARWriter | None = None

    def load(self, loader: Loader):
        loader.add_option(
            name="pynthar",
            typespec=str,
            default=".",
            help="use this pynt script to save HAR file",
        )

        loader.add_option(
            name="pynt_ready_marker",
            typespec=str,
            default="",
            help="file path for a marker file indicating the HAR file is ready",
        )

    def configure(self, updated):
        if "save_stream_filter" in updated:
            if ctx.options.save_stream_filter:
                try:
                    self.filt = flowfilter.parse(ctx.options.save_stream_filter)
                except ValueError as e:
                    raise exceptions.OptionsError(str(e)) from e
            else:
                self.filt = None

    def response(self, flow: http.HTTPFlow) -> None:
        # websocket flows will receive a websocket_end,
        # we don't want to persist them here already
        if flow.websocket is None:
            self._save_flow(flow)

    def error(self, flow: http.HTTPFlow) -> None:
        self.response(flow)

    def websocket_end(self, flow: http.HTTPFlow) -> None:
        self._save_flow(flow)

    def _save_flow(self, flow: http.HTTPFlow) -> None:
        if self.har_writer and isinstance(flow, http.HTTPFlow):
            flow_matches = self.filt is None or self.filt(flow)
            if flow_matches and not hasattr(flow, 'pynt_skip_har'):
                self.har_writer.write(self.flow_entry(flow))

    def running(self):
        if ctx.options.pynthar:
            print(f"Writing to HAR file {ctx.options.pynthar}")
            self.har_writer = HARWriter(ctx.options.pynthar, ctx.options.pynt_ready_marker)

    def done(self):
        if self.har_writer:
            bytes_written, entries_written, entries_dropped = self.har_writer.end()
            print(f"HAR file saved with {entries_written} entries ({human.pretty_size(bytes_written)}).\n" +
                  f"{entries_dropped} entries dropped.")
            self.har_writer = None

    def flow_entry(self, flow: http.HTTPFlow) -> dict:
        """Creates HAR entry from flow"""

        if flow.server_conn in self.servers_seen:
            connect_time = -1.0
            ssl_time = -1.0
        elif flow.server_conn.timestamp_tcp_setup:
            assert flow.server_conn.timestamp_start
            connect_time = 1000 * (
                flow.server_conn.timestamp_tcp_setup - flow.server_conn.timestamp_start
            )

            if flow.server_conn.timestamp_tls_setup:
                ssl_time = 1000 * (
                    flow.server_conn.timestamp_tls_setup
                    - flow.server_conn.timestamp_tcp_setup
                )
            else:
                ssl_time = -1.0
            self.servers_seen.add(flow.server_conn)
        else:
            connect_time = -1.0
            ssl_time = -1.0

        if flow.request.timestamp_end:
            send = 1000 * (flow.request.timestamp_end - flow.request.timestamp_start)
        else:
            send = 0

        if flow.response and flow.request.timestamp_end:
            wait = 1000 * (flow.response.timestamp_start - flow.request.timestamp_end)
        else:
            wait = 0

        if flow.response and flow.response.timestamp_end:
            receive = 1000 * (
                flow.response.timestamp_end - flow.response.timestamp_start
            )

        else:
            receive = 0

        timings: dict[str, float | None] = {
            "connect": connect_time,
            "ssl": ssl_time,
            "send": send,
            "receive": receive,
            "wait": wait,
        }

        if flow.response:
            try:
                content = flow.response.content
            except ValueError:
                content = flow.response.raw_content
            response_body_size = (
                len(flow.response.raw_content) if flow.response.raw_content else 0
            )
            response_body_decoded_size = len(content) if content else 0
            response_body_compression = response_body_decoded_size - response_body_size
            response = {
                "status": flow.response.status_code,
                "statusText": flow.response.reason,
                "httpVersion": flow.response.http_version,
                "cookies": self.format_response_cookies(flow.response),
                "headers": self.format_multidict(flow.response.headers),
                "content": {
                    "size": response_body_size,
                    "compression": response_body_compression,
                    "mimeType": flow.response.headers.get("Content-Type", ""),
                },
                "redirectURL": flow.response.headers.get("Location", ""),
                "headersSize": len(str(flow.response.headers)),
                "bodySize": response_body_size,
            }
            if content and strutils.is_mostly_bin(content):
                response["content"]["text"] = base64.b64encode(content).decode()
                response["content"]["encoding"] = "base64"
            else:
                text_content = flow.response.get_text(strict=False)
                if text_content is None:
                    response["content"]["text"] = ""
                else:
                    response["content"]["text"] = text_content
        else:
            response = {
                "status": 0,
                "statusText": "",
                "httpVersion": "",
                "headers": [],
                "cookies": [],
                "content": {},
                "redirectURL": "",
                "headersSize": -1,
                "bodySize": -1,
                "_transferSize": 0,
                "_error": None,
            }
            if flow.error:
                response["_error"] = flow.error.msg

        if flow.request.method == "CONNECT":
            url = f"https://{flow.request.pretty_url}/"
        else:
            url = flow.request.pretty_url

        entry: dict[str, Any] = {
            "startedDateTime": datetime.fromtimestamp(
                flow.request.timestamp_start, timezone.utc
            ).isoformat(),
            "time": sum(v for v in timings.values() if v is not None and v >= 0),
            "request": {
                "method": flow.request.method,
                "url": url,
                "httpVersion": flow.request.http_version,
                "cookies": self.format_multidict(flow.request.cookies),
                "headers": self.format_multidict(flow.request.headers),
                "queryString": self.format_multidict(flow.request.query),
                "headersSize": len(str(flow.request.headers)),
                "bodySize": len(flow.request.content) if flow.request.content else 0,
            },
            "response": response,
            "cache": {},
            "timings": timings,
        }

        if flow.request.method in ["POST", "GET", "PUT", "PATCH"]:
            params = self.format_multidict(flow.request.urlencoded_form)
            entry["request"]["postData"] = {
                "mimeType": flow.request.headers.get("Content-Type", ""),
                "text": flow.request.get_text(strict=False),
                "params": params,
            }

        if flow.server_conn.peername:
            entry["serverIPAddress"] = str(flow.server_conn.peername[0])

        websocket_messages = []
        if flow.websocket:
            for message in flow.websocket.messages:
                if message.is_text:
                    data = message.text
                else:
                    data = base64.b64encode(message.content).decode()
                websocket_message = {
                    "type": "send" if message.from_client else "receive",
                    "time": message.timestamp,
                    "opcode": message.type.value,
                    "data": data,
                }
                websocket_messages.append(websocket_message)

            entry["_resourceType"] = "websocket"
            entry["_webSocketMessages"] = websocket_messages
        return entry

    def format_response_cookies(self, response: http.Response) -> list[dict]:
        """Formats the response's cookie header to list of cookies"""
        cookie_list = response.cookies.items(multi=True)
        rv = []
        for name, (value, attrs) in cookie_list:
            cookie = {
                "name": name,
                "value": value,
                "path": attrs.get("path", "/"),
                "domain": attrs.get("domain", ""),
                "httpOnly": "httpOnly" in attrs,
                "secure": "secure" in attrs,
            }
            # TODO: handle expires attribute here.
            # This is not quite trivial because we need to parse random date formats.
            # For now, we just ignore the attribute.

            if "sameSite" in attrs:
                cookie["sameSite"] = attrs["sameSite"]

            rv.append(cookie)
        return rv

    def format_multidict(self, obj: _MultiDict[str, str]) -> list[dict]:
        return [{"name": k, "value": v} for k, v in obj.items(multi=True)]


addons = [PyntSaveHar()]
