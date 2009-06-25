# -*- coding: utf-8 -*-

from seishub.config import Option, IntOption
from seishub.core import ERROR, WARN, INFO, DEBUG, DEBUGX
from twisted.python import log, logfile
import os
import traceback


LOG_LEVELS = {'OFF': 0,
              'ERROR': ERROR,
              'WARN': WARN,
              'INFO': INFO,
              'DEBUG': DEBUG,
              'DEBUGX': DEBUGX}


class Logger(object):
    """
    A log manager to handle all incoming log calls. 
    
    You still may use twisted.python.log.msg and twisted.python.log.err to 
    emit log messages.
    """

    Option('logging', 'log_file', 'seishub.log', "Name of the log file.")
    Option('logging', 'log_level', 'DEBUG',
        """Level of verbosity in log.

        Should be one of (`ERROR`, `WARN`, `INFO`, `DEBUG`).""")

    def __init__(self, env, log_file=None):
        self.env = env
        if isinstance(log_file, basestring):
            self.env.config.set('logging', 'log_file', log_file)
            self.env.config.save()
        self.start()

    def start(self):
        # log level
        log_level = self.env.config.get('logging', 'log_level').upper()
        self.log_level = LOG_LEVELS.get(log_level, ERROR)
        if not self.log_level:
            return
        # log file
        log_file = self.env.config.get('logging', 'log_file')
        log_dir = os.path.join(self.env.config.path, 'logs')
        lh = logfile.LogFile(log_file, log_dir)
        # rotate after each new start-up
        lh.rotate()
        # start logging
        log.FileLogObserver(lh).start()

    def stop(self):
        for l in log.theLogPublisher:
            log.removeObserver(l)

    def _formatMessage(self, level, msg, showTraceback):
        msg = '%6s  %s' % (level + ':', msg)
        log.msg(msg, isError=True)
        if showTraceback:
            log.msg(traceback.format_exc(), isError=True)

    def http(self, code, msg, showTraceback=False):
        if code < 400:
            self.debug(msg, showTraceback)
        elif code < 500:
            self.info(msg, showTraceback)
        else:
            self.error(msg, showTraceback)

    def error(self, msg, showTraceback=False):
        if self.log_level < ERROR:
            return
        self._formatMessage('ERROR', msg, showTraceback)

    def warn(self, msg, showTraceback=False):
        if self.log_level < WARN:
            return
        self._formatMessage('WARN', msg, showTraceback)

    def info(self, msg, showTraceback=False):
        if self.log_level < INFO:
            return
        self._formatMessage('INFO', msg, showTraceback)

    def debug(self, msg, showTraceback=False):
        if self.log_level < DEBUG:
            return
        self._formatMessage('DEBUG', msg, showTraceback)

    def debugx(self, msg, showTraceback=False):
        if self.log_level < DEBUGX:
            return
        self._formatMessage('XXX', msg, showTraceback)
