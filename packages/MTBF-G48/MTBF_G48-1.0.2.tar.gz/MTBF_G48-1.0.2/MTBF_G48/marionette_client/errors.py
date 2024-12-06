# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import traceback


class InstallGeckoError(Exception):
    pass


class KaiOSMarionetteException(Exception):

    """Raised when a generic non-recoverable exception has occured."""

    code = (500,)
    status = "webdriver error"

    def __init__(self, message=None, cause=None, stacktrace=None):
        """Construct new KaiOSMarionetteException instance.

        :param message: An optional exception message.

        :param cause: An optional tuple of three values giving
            information about the root exception cause.  Expected
            tuple values are (type, value, traceback).

        :param stacktrace: Optional string containing a stacktrace
            (typically from a failed JavaScript execution) that will
            be displayed in the exception's string representation.

        """

        self.msg = message
        self.cause = cause
        self.stacktrace = stacktrace

    def __str__(self):
        msg = str(self.msg)
        tb = None

        if self.cause:
            if type(self.cause) is tuple:
                msg += ", caused by %r" % self.cause[0]
                tb = self.cause[2]
            else:
                msg += ", caused by %s" % self.cause
        if self.stacktrace:
            st = "".join(["\t%s\n" % x for x in self.stacktrace.splitlines()])
            msg += "\nstacktrace:\n%s" % st

        return "".join(traceback.format_exception(self.__class__, msg, tb))


class ElementNotSelectableException(KaiOSMarionetteException):
    status = "element not selectable"


class InvalidArgumentException(KaiOSMarionetteException):
    status = "invalid argument"


class InvalidSessionIdException(KaiOSMarionetteException):
    status = "invalid session id"

class TimeoutException(KaiOSMarionetteException):
    code = (21,)
    status = "timeout"


class JavascriptException(KaiOSMarionetteException):
    code = (17,)
    status = "javascript error"


class NoSuchElementException(KaiOSMarionetteException):
    code = (7,)
    status = "no such element"


class NoSuchWindowException(KaiOSMarionetteException):
    code = (23,)
    status = "no such window"


class StaleElementException(KaiOSMarionetteException):
    code = (10,)
    status = "stale element reference"


class ScriptTimeoutException(KaiOSMarionetteException):
    code = (28,)
    status = "script timeout"


class ElementNotVisibleException(KaiOSMarionetteException):
    code = (11,)
    status = "element not visible"

    def __init__(
        self, message="Element is not currently visible and may not be manipulated",
                 stacktrace=None, cause=None):
        super(ElementNotVisibleException, self).__init__(
            message, cause=cause, stacktrace=stacktrace)


class ElementNotAccessibleException(KaiOSMarionetteException):
    code = (56,)
    status = "element not accessible"


class NoSuchFrameException(KaiOSMarionetteException):
    code = (8,)
    status = "no such frame"


class InvalidElementStateException(KaiOSMarionetteException):
    code = (12,)
    status = "invalid element state"


class NoAlertPresentException(KaiOSMarionetteException):
    code = (27,)
    status = "no such alert"


class InvalidCookieDomainException(KaiOSMarionetteException):
    code = (24,)
    status = "invalid cookie domain"


class UnableToSetCookieException(KaiOSMarionetteException):
    code = (25,)
    status = "unable to set cookie"


class InvalidElementCoordinates(KaiOSMarionetteException):
    code = (29,)
    status = "invalid element coordinates"


class InvalidSelectorException(KaiOSMarionetteException):
    code = (32, 51, 52)
    status = "invalid selector"


class MoveTargetOutOfBoundsException(KaiOSMarionetteException):
    code = (34,)
    status = "move target out of bounds"


class SessionNotCreatedException(KaiOSMarionetteException):
    code = (33, 71)
    status = "session not created"


class UnexpectedAlertOpen(KaiOSMarionetteException):
    code = (26,)
    status = "unexpected alert open"


class UnknownCommandException(KaiOSMarionetteException):
    code = (9,)
    status = "unknown command"


class UnknownException(KaiOSMarionetteException):
    code = (13,)
    status = "unknown error"


class UnsupportedOperationException(KaiOSMarionetteException):
    code = (405,)
    status = "unsupported operation"


es_ = [e for e in locals().values() if type(e) == type and issubclass(e, KaiOSMarionetteException)]
by_string = {e.status: e for e in es_}
by_number = {c: e for e in es_ for c in e.code}


def lookup(identifier):
    """Finds error exception class by associated Selenium JSON wire
    protocol number code, or W3C WebDriver protocol string."""
    lookup = by_string
    if isinstance(identifier, int):
        lookup = by_number
    return lookup.get(identifier, KaiOSMarionetteException)
