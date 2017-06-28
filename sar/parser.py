#!/usr/bin/env python
"""
:mod:`sar.parser` is a module containing class for parsing SAR output files.

.. WARNING::
   Parses SAR ASCII output only, not binary files!
"""

from sar import PATTERN_RESTART, ALL_PATTERNS
import mmap
import os
import re
import traceback
import platform


class Parser(object):
    """
    Parser for sar outputs. Uses SAR interpreter binary and parses out \
    its output
        :param filename: Name of the SAR output file
        :type filename: str.
    """

    def __init__(self, filename=''):

        self._sarinfo = {}
        """Hash with SAR info"""
        self.__file_date = ''
        """String which contains date of SAR file"""
        self.__restart_times = []
        """List with box restart times"""
        self.__filename = filename
        """SAR output filename to be parsed"""

        self.__fields = {}
        """Map of maps for fields values"""

    def load_file(self):
        """
        Loads SAR format logfile in ASCII format (sarXX).
            :return: ``True`` if loading and parsing of file went fine, \
            ``False`` if it failed (at any point)
        """

        # We first split file into pieces
        searchunks = self._split_file()

        if searchunks:

            # And then we parse pieces into meaningful data
            usage = self._parse_file(searchunks)

            if 'CPU' in usage:
                return False

            self._sarinfo = usage
            del usage
            return True

        else:
            return False

    def get_filedate(self):
        """
        Returns file date of SAR file
            :return: ISO format (YYYY-MM-DD) of a SAR file
        """
        if self.__file_date == '':
            # If not already parsed out, parse it.
            self.__get_filedate()

        return self.__file_date

    def get_sar_info(self):
        """
        Returns parsed sar info
            :return: ``Dictionary``-style list of SAR data
        """

        try:
            test = self._sarinfo["CPU"]
            del test

        except KeyError:
            file_parsed = self.load_file()
            if file_parsed:
                return self._sarinfo
            else:
                return False

        except:
            ### DEBUG
            traceback.print_exc()
            return False

        return self._sarinfo

    def _split_file(self, data=''):
        """
        Splits SAR output or SAR output file (in ASCII format) in order to
        extract info we need for it, in the format we want.
            :param data: Input data instead of file
            :type data: str.
            :return: ``List``-style of SAR file sections separated by
                the type of info they contain (SAR file sections) without
                parsing what is exactly what at this point
        """

        # Filename passed checks through __init__
        if ((self.__filename and os.access(self.__filename, os.R_OK))
                or data != ''):

            fhandle = None

            if data == '':
                try:
                    fhandle = os.open(self.__filename, os.O_RDONLY)
                except OSError:
                    print(("Couldn't open file %s" % self.__filename))
                    fhandle = None

            if fhandle or data != '':

                datalength = 0
                
                # Dealing with mmap difference on Windows and Linux
                if platform.system() == 'Windows':
                    dataprot = mmap.ACCESS_READ
                else:
                    dataprot = mmap.PROT_READ

                if data != '':
                    fhandle = -1
                    datalength = len(data)
                    
                    if platform.system() == 'Windows':    
                        dataprot = mmap.ACCESS_READ | mmap.ACCESS_WRITE
                    else:
                        dataprot = mmap.PROT_READ | mmap.PROT_WRITE                    

                try:
                    if platform.system() == 'Windows':
                        sarmap = mmap.mmap(
                            fhandle, length=datalength, access=dataprot
                        )
                    else:
                        sarmap = mmap.mmap(
                            fhandle, length=datalength, prot=dataprot
                        )
                    if data != '':

                        sarmap.write(data)
                        sarmap.flush()
                        sarmap.seek(0, os.SEEK_SET)

                except (TypeError, IndexError):
                    if data == '':
                        os.close(fhandle)
                    traceback.print_exc()
                    # sys.exit(-1)
                    return False

                # Here we'll store chunks of SAR file, unparsed
                searchunks = []
                oldchunkpos = 0
                dlpos = sarmap.find('\n\n', 0)
                size = 0

                if data == '':
                    # We can do mmap.size() only on read-only mmaps
                    size = sarmap.size()
                else:
                    # Otherwise, if data was passed to us,
                    # we measure its length
                    len(data)

                # oldchunkpos = dlpos

                while dlpos > -1:  # mmap.find() returns -1 on failure.

                    tempchunk = sarmap.read(dlpos - oldchunkpos)
                    searchunks.append(tempchunk.strip())

                    # We remember position, add 2 for 2 DD's
                    # (newspaces in production). We have to remember
                    # relative value
                    oldchunkpos += (dlpos - oldchunkpos) + 2

                    # We position to new place, to be behind \n\n
                    # we've looked for.
                    try:
                        sarmap.seek(2, os.SEEK_CUR)
                    except ValueError:
                        print(('Out of bounds (%s)!\n' % (sarmap.tell())))
                    # Now we repeat find.
                    dlpos = sarmap.find("\n\n")

                # If it wasn't the end of file, we want last piece of it
                if oldchunkpos < size:
                    tempchunk = sarmap[oldchunkpos:]
                    searchunks.append(tempchunk.strip())

                sarmap.close()

            if fhandle != -1:
                os.close(fhandle)

            if searchunks:
                return searchunks
            else:
                return False

        return False

    def _parse_file(self, sar_parts):
        """
        Parses splitted file to get proper information from split parts.
            :param sar_parts: Array of SAR file parts
            :return: ``Dictionary``-style info (but still non-parsed) \
                from SAR file, split into sections we want to check
        """
        usage = {}
        output = {}

        # If sar_parts is a list
        if type(sar_parts) is list:
            restart_pattern = re.compile(PATTERN_RESTART)

            """ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """
            """              ********** ATTENTION *******            """
            """ THERE CAN BE MORE THAN ONE SAME SECTION IN ONE FILE  """
            """ IF SYSTEM WAS REBOOTED DURING THE DAY                """
            """ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """

            for PATTERNSNAME in ALL_PATTERNS:
                patterns = ALL_PATTERNS[PATTERNSNAME]
                rgxpattern = re.compile(patterns['PATTERN'])

                for part in sar_parts:

                    if rgxpattern.search(part):

                        if PATTERNSNAME in usage:
                            usage[PATTERNSNAME] += '\n' + part
                        else:
                            usage[PATTERNSNAME] = part
                            try:
                                first_line = part.split('\n')[0]
                            except IndexError:
                                first_line = part

                            self.__fields[PATTERNSNAME] = self.__find_column(patterns['FIELDS'], first_line)

                    # Try to match restart time
                    if restart_pattern.search(part):
                        pieces = part.split()
                        self.__restart_times.append(pieces[0])
                        del pieces

            del sar_parts

            # Now we have parts pulled out and combined, do further
            # processing.
            for PATTERNSNAME in ALL_PATTERNS:
                patterns = ALL_PATTERNS[PATTERNSNAME]
                output[PATTERNSNAME] = self.__split_info(usage[PATTERNSNAME], PATTERNSNAME, patterns)
            del usage

            return output

        return output

    def __find_column(self, column_names, part_first_line):
        """
        Finds the column for the column_name in sar type definition,
        and returns its index.
            :param column_names: Names of the column we look for (regex) put in
                the list
            :param part_first_line: First line of the SAR part
            :return: ``Dictionary`` of names => position, None for not present
        """
        part_parts = part_first_line.split()

        ### DEBUG
        # print("Parts: %s" % (part_parts))

        return_dict = {}

        counter = 0
        for piece in part_parts:
            for colname in column_names:
                pattern_re = re.compile(colname)
                if pattern_re.search(piece):
                    return_dict[colname] = counter
                    break
            counter += 1

        # Verify the content of the return dictionary, fill the blanks
        # with -1s :-)
        for colver in column_names:
            try:
                tempval = return_dict[colver]
                del tempval
            except KeyError:
                return_dict[colver] = None

        return return_dict

    def __split_info(self, info_part, patternsname, patterns):
        """
        Splits info from SAR parts into logical stuff :-)
        :param info_part: Part of SAR output we want to split into usable data
        :param patternsname: ???
        :param patterns: ???
        :return: ``List``-style info from SAR files, now finally \
            completely parsed into meaningful data for further processing
        """

        pattern = patterns['PATTERN']
        if pattern == '':
            return False

        return_dict = {}

        pattern_re = re.compile(pattern)

        for part_line in info_part.split('\n'):

            if part_line.strip() != '' and not pattern_re.search(part_line):

                # Take care of AM/PM timestamps in SAR file
                is_24hr = True
                is_AM = False

                if part_line[9:11] == 'AM':
                    is_24hr = False
                    is_AM = True
                elif part_line[9:11] == 'PM':
                    is_24hr = False
                    is_AM = False

                if is_24hr is False:
                    part_line =  ('%s_%s XX %s' % (part_line[:8], part_line[9:11], part_line[12:]))

                # Line is not empty, nor it's header.
                # let's hit the road Jack!
                elems = part_line.split()
                full_time = elems[0].strip()

                if full_time != "Average:":

                    # Convert time to 24hr format if needed
                    if is_24hr is False:
                        full_time = full_time[:-3]

                        # 12 is a bitch in AM/PM notation
                        if full_time[:2] == '12':
                            if is_AM is True:
                                full_time = ('%s:%s' % ('00', full_time[3:]))
                            is_AM = not is_AM

                        if is_AM is False and full_time[0:2] != '00':
                            hours = int(full_time[:2]) + 12
                            hours = ('%02d' % (hours,))
                            full_time = ('%s:%s' % (hours, full_time[3:]))

                    try:
                        blah = return_dict[full_time]
                        del blah
                    except KeyError:
                        return_dict[full_time] = {}

                    fields = self.__fields[patternsname]
                    pairs = patterns["PAIRS"]

                    for sectionname in pairs.iterkeys():

                        value = elems[fields[pairs[sectionname]]]

                        if sectionname == 'membuffer' or \
                                sectionname == 'memcache' or \
                                sectionname == 'memfree' or \
                                sectionname == 'memused' or \
                                sectionname == 'swapfree' or \
                                sectionname == 'swapused':
                            value = int(value)
                        else:
                            value = float(value)

                        if patternsname == 'CPU':
                            cpuid = elems[(1 if is_24hr is True else 2)]
                            try:
                                blah = return_dict[full_time][cpuid]
                                del blah
                            except KeyError:
                                return_dict[full_time][cpuid] = {}
                            return_dict[full_time][cpuid][sectionname] = \
                                value
                        else:
                            return_dict[full_time][sectionname] = value

        return return_dict

    def __get_filedate(self):
        """
        Parses (extracts) date of SAR data, from the SAR output file itself.
            :return: ISO-style (YYYY-MM-DD) date from SAR file
        """

        if os.access(self.__filename, os.R_OK):

            # Read first line of the file
            try:
                sar_file = open(self.__filename, "r")

            except OSError:
                ### DEBUG
                traceback.print_exc()
                return False

            except:
                ### DEBUG
                traceback.print_exc()
                return False

            firstline = sar_file.readline()
            info = firstline.split()
            sar_file.close()

            try:
                self.__file_date = info[3]

            except KeyError:
                self.__file_date = ''
                return False

            except:
                ### DEBUG
                traceback.print_exc()
                return False

            return True

        return False
