#!/usr/bin/env python
"""
:mod:`sar`
"""

PART_CPU = 0
"""Indicates CPU part of SAR file"""

PART_MEM = 1
"""Indicates RAM memory usage part of SAR file"""

PART_SWP = 2
"""Indicates swap memory usage part of SAR file"""

PART_IO = 3
"""I/O usage part of SAR file"""

PATTERN_CPU = ".*CPU.*(usr|user).*nice.*sys.*"
"""CPU regexp pattern for detecting SAR section header"""

FIELDS_CPU = [
    '\%(usr|user)', '\%nice', '\%sys', '\%iowait', '\%idle'
]
"""Regexp terms for finding fields in SAR parts for CPU"""

FIELD_PAIRS_CPU = {
    'usr': FIELDS_CPU[0], 'nice': FIELDS_CPU[1], 'sys': FIELDS_CPU[2],
    'iowait': FIELDS_CPU[3], 'idle': FIELDS_CPU[4]
}
"""Pair regexp terms with field names in CPU output dictionary"""

PATTERN_MEM = ".*kbmemfree.*kbmemused.*memused.*kbbuffers.*kbcached.*"
"""Mem usage regexp pattern for detecting SAR section header"""

FIELDS_MEM = [
    'kbmemfree', 'kbmemused', '\%memused', 'kbbuffers', 'kbcached'
]
"""Regexp terms for finding fields in SAR parts for memory usage"""

FIELD_PAIRS_MEM = {
    'memfree': FIELDS_MEM[0], 'memused': FIELDS_MEM[1],
    'memusedpercent': FIELDS_MEM[2], 'membuffer': FIELDS_MEM[3],
    'memcache': FIELDS_MEM[4]
}
"""Pair regexp terms with field names in memory usage output dictionary"""

PATTERN_SWP = ".*kbswpfree.*kbswpused.*swpused.*"
"""Swap usage regexp pattern for detecting SAR section header"""

FIELDS_SWP = [
    'kbswpfree', 'kbswpused', '\%swpused'
]
"""Regexp terms for finding fields in SAR parts for swap usage"""

FIELD_PAIRS_SWP = {
    'swapfree': FIELDS_SWP[0], 'swapused': FIELDS_SWP[1],
    'swapusedpercent': FIELDS_SWP[2]
}
"""Pair regexp terms with field names in swap usage output dictionary"""

PATTERN_IO = ".*tps.*rtps.*wtps.*bread\/s.*bwrtn\/s.*"
"""I/O usage regexp pattern for detecting SAR section header"""

FIELDS_IO = [
    '^tps', '^rtps', '^wtps', 'bread\/s', 'bwrtn\/s'
]
"""Regexp terms for finding fields in SAR parts for swap usage"""

FIELD_PAIRS_IO = {
    'tps': FIELDS_IO[0], 'rtps': FIELDS_IO[1], 'wtps': FIELDS_IO[2],
    'bread': FIELDS_IO[3], 'bwrite': FIELDS_IO[4],

}
"""Pair regexp terms with field names in swap usage output dictionary"""

PATTERN_RESTART = ".*LINUX\ RESTART.*"
"""Restart time regexp pattern for detecting SAR restart notices"""

PATTERN_MULTISPLIT = "Linux"
"""Pattern for splitting multiple combined SAR file"""

PATTERN_DATE = "[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]"
"""Split by date in multiday SAR file"""

__all__ = [
    "PART_CPU", "PART_MEM", "PART_SWP", "PART_IO",
    "PATTERN_CPU", "PATTERN_MEM", "PATTERN_SWP", "PATTERN_IO",
    "PATTERN_RESTART", "PATTERN_MULTISPLIT", "PATTERN_DATE"
]
