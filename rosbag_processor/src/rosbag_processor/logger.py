import logging


class Logger:
    def __init__(self, pname, plog_file, log_level=logging.INFO):
        handler = logging.FileHandler(plog_file)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

        self.vlogger = logging.getLogger(pname)
        self.vlogger.setLevel(log_level)
        self.vlogger.addHandler(handler)

    def get(self):
        return self.vlogger
