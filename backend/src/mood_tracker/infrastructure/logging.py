import logging
from typing import TYPE_CHECKING, Literal, assert_never

import structlog

if TYPE_CHECKING:
    from structlog.typing import Processor


def setup_logging(env: Literal["dev", "prod"]) -> None:
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    processors: list[Processor] = [
        *shared_processors,
    ]

    if env == "dev":
        processors.extend(
            [
                structlog.processors.CallsiteParameterAdder(
                    [
                        structlog.processors.CallsiteParameter.MODULE,
                        structlog.processors.CallsiteParameter.FILENAME,
                        structlog.processors.CallsiteParameter.FUNC_NAME,
                        structlog.processors.CallsiteParameter.LINENO,
                    ],
                ),
                structlog.dev.ConsoleRenderer(),
            ],
        )
    elif env == "prod":
        processors.extend(
            [
                structlog.processors.ExceptionRenderer(),
                structlog.processors.JSONRenderer(),
            ],
        )
    else:
        assert_never(env)

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer()
            if env == "dev"
            else structlog.processors.JSONRenderer(),
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
