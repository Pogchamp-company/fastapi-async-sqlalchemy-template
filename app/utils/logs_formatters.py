from logging import LogRecord

from json_logging import BaseJSONFormatter, util, JSONLogFormatter, _sanitize_log_msg
from json_logging.util import RequestUtil

from app.utils.colorize import bcolors


class JSONRequestLogFormatter(BaseJSONFormatter):
    """
       Formatter for HTTP request instrumentation logging
    """

    def _format_log_object(self, record: LogRecord, request_util: RequestUtil) -> dict[str, str | int]:
        request = record.request_info.request
        request_adapter = request_util.request_adapter

        length = request_adapter.get_content_length(request)
        json_log_object = {
            "request": request_adapter.get_path(request),
            "response_status": record.request_info.response_status,
            "method": request_adapter.get_method(request),
            "execution_time_ms": record.request_info.response_time_ms,

            "type": "request",
            "remote_ip": request_adapter.get_remote_ip(request),
            "request_size_b": util.parse_int(length, -1),
            "request_received_at": record.request_info.request_received_at,
            "response_sent_at": record.request_info.response_sent_at,
        }
        json_log_object.update(super(JSONRequestLogFormatter, self)._format_log_object(record, request_util))

        return json_log_object

    def format(self, record: LogRecord) -> str:
        http_status_to_color = {
            2: bcolors.OKCYAN,
            4: bcolors.WARNING,
            5: bcolors.FAIL
        }

        color = bcolors.OKCYAN
        for k, v in http_status_to_color.items():
            if int(record.request_info.response_status) // 100 == k:
                color = v

        result = super().format(record)
        return color.colorize(result)


class JSONLogWebFormatter(JSONLogFormatter):
    """
    Formatter for web application log
    """

    def _format_log_object(self, record: LogRecord, request_util: RequestUtil) -> dict[str, str | int]:
        json_log_object = {
            "msg": _sanitize_log_msg(record),
            "level": record.levelname,
            "module": record.module,
            "line_no": record.lineno,

            "type": "log",
            "logger": record.name,
            "thread": record.threadName,
        }
        json_log_object.update(super(JSONLogWebFormatter, self)._format_log_object(record, request_util))
        return json_log_object

    def format(self, record: LogRecord) -> str:
        level_to_color = {
            'INFO': bcolors.OKGREEN,
            'WARNING': bcolors.WARNING,
            'ERROR': bcolors.FAIL
        }
        color = level_to_color.get(record.levelname, bcolors.FAIL)

        log_object = super().format(record)
        return color.colorize(log_object)
