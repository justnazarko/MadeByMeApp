"""Main module to run from"""

import logging

from uvicorn import run

from core.config import config

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    for logger_name in ("sqlalchemy", "sqlalchemy.engine", "uvicorn.access"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = config.backend.logging_level == "DEBUG"
        logger.setLevel(
            logging.INFO
            if config.backend.logging_level == "DEBUG"
            else logging.CRITICAL
        )

    run(
        app="server.app:app",
        host=config.backend.host,
        port=config.backend.port,
        log_level=logging.WARNING,
    )
