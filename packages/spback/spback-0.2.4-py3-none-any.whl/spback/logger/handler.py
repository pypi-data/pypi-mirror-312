"""create customed logger"""

import logging

# customed logger, write jsonfield of task compute.


class ModelLogHandler(logging.Handler):
    """suitble for model has log attr.
    logger will save log to model.log, and save it after emit (when calling logger.info)."""

    def __init__(self, record):
        super().__init__()
        self.record = record

    def emit(self, record):
        log_entry = self.format(record)
        if self.record.log is None:
            self.record.log = ""
        self.record.log += log_entry + "\n"
        self.record.save(update_fields=["log"])
