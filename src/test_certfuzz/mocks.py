'''
Created on Oct 24, 2012

@organization: cert.org
'''
import hashlib
import logging
import string
import tempfile
import os
from certfuzz.file_handlers.basicfile import BasicFile

class Mock(object):
    def __init__(self, *args, **kwargs):
        pass

class MockCrasher(Mock):
    def __init__(self):
        fd, f = tempfile.mkstemp(suffix='.ext', prefix='fileroot')
        os.close(fd)
        self.fuzzedfile = BasicFile(f)
        self.debugger_template = 'foo'

    def set_debugger_template(self, dummy):
        pass

class MockRange(Mock):
    def __init__(self):
        self.min = 0.01
        self.max = 0.10

    def __str__(self):
        return '{}-{}'.format(self.min, self.max)

class MockRangefinder(Mock):
    def next_item(self):
        return MockRange()

class MockSeedfile(Mock):
    basename = 'basename'
    root = 'root'
    ext = '.ext'
    tries = 0
    rangefinder = MockRangefinder()

    def __init__(self, sz=1000):
        self.value = 'A' * sz
        self.md5 = hashlib.md5(self.value).hexdigest()
        self.len = len(self.value)

    def read(self):
        return self.value

class MockFuzzedFile(Mock):
    path = u'foo'

class MockFuzzer(Mock):
    is_minimizable = False

class MockTestcase(Mock):
    signature = 'ABCDEFGHIJK'
    logger = logging.getLogger('mocktestcaselogger')
    seedfile = MockSeedfile()
    seednum = 123456789
    range = MockRange()
    fuzzedfile = MockFuzzedFile()
    pc = u'dummyPCstring'

class MockDbgOut(Mock):
    is_crash = False
    total_stack_corruption = False

    def get_crash_signature(self, *dummyargs):
        return 'AAAAA'

class MockDebugger(Mock):
    def get(self):
        return MockDebugger

    def go(self):
        return MockDbgOut()

class MockCfg(dict):
    def __init__(self):
        self['timeouts']={'debugger_timeout': 1}
        self['target']={'cmdline_template': string.Template('a b c d'),
                        'killprocname': 'a'}
        self['verifier']={'exclude_unmapped_frames': False,
                          'backtracelevels': 5}

    def get_command_args_list(self, dummy):
        return tuple('abcd')
