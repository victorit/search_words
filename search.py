# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
script which searches for a pattern using a regular expression in lines of text,
and prints the lines which contain matching text.
The script's output format: "file_name line_number line"

The script accepts the following parameters:

-r, --regex       mandatory - the regular expression to search for.
-f, --files       optional - a list of files to search in. If this parameter is omitted,
                  the script expects text input from STDIN.

These extra parameters are mutually exclusive:

-u, --underline   optional - "^" is printed underneath the matched text.
-c, --color       optional - the matched text is highlighted in color [1].
-m, --machine     optional - print the output in the format: "file_name:line_number:start_position:matched_text".
"""

import sys
import getopt
import re


def getColor(colour, text):
    """
    # Colourise - colours text in shell. Returns plain if colour doesn't exist.
    :param colour:
    :param text:
    :return:
    """
    if colour == "black":
        return "\033[1;30m" + str(text) + "\033[1;m"
    if colour == "red":
        return "\033[1;31m" + str(text) + "\033[1;m"
    if colour == "green":
        return "\033[1;32m" + str(text) + "\033[1;m"
    if colour == "yellow":
        return "\033[1;33m" + str(text) + "\033[1;m"
    if colour == "blue":
        return "\033[1;34m" + str(text) + "\033[1;m"
    if colour == "magenta":
        return "\033[1;35m" + str(text) + "\033[1;m"
    if colour == "cyan":
        return "\033[1;36m" + str(text) + "\033[1;m"
    if colour == "gray":
        return "\033[1;37m" + str(text) + "\033[1;m"
    return str(text)


class SearchWords:
    """
    Base Class
    """
    def __init__(self, exp, num, line, filename=""):
        """
        Constructor of base class
        :param exp: regular expression
        :param filename: Name of file
        :param num: number of line in file
        :param line: line in file
        :param found: flag is True if regular expression is found in line

        """
        self._exp = exp
        self._filename = filename
        self._num = num
        self._line = line
        self._found = False

    def findPatterns(self):
        """
        Set flag found to True if regular expression is found in line
        :return: True or False
        """
        if re.search(self._exp, self._line):
            self._found = True

    def regexFound(self):
        """
        Returns found
        :return: self._found
        """
        return self._found

    def __str__(self):
        """
        returns string "file_name line_number line"
        :return:
        """
        return f"{self._filename} {str(self._num)} {self._line}"


class searchWordsWithColor(SearchWords):
    """
    Class searchWordsWithColor change color of found regular expressions in text
    """
    def __init__(self, exp, num, line, filename, color):
        """
        Class Constructor
        :param exp: regular expression
        :param filename: Name of file
        :param num: number of line in file
        :param line: line in file
        :param color: color to change
        """
        super().__init__(exp, num, line, filename)
        self._color = color

    def findPatterns(self):
        """
        Find all regular expressions and changes color in line
        :return:
        """
        for i in re.findall(self._exp, self._line):
            # change color
            colored_str = getColor(self._color, i)
            # set line with color
            self._line = re.sub(i, colored_str, self._line)


class searchWordWithUnderlined(SearchWords):
    """
    Find all regular expressions in line and add ^ before
    """
    def __init__(self, exp, num, line, filename):
        """
        Class Constructor
        :param exp: regular expression
        :param filename: Name of file
        :param num: number of line in file
        :param line: line in file
        """
        super().__init__(exp, num, line, filename)
        self._underlined = '\033[4m'
        # self._underlined = '^'
        self._end = '\033[0m'

    def findPatterns(self):
        """
        Find all regular expressions and add ^ before
        :return:
        """
        for i in re.findall(self._exp, self._line):
            # add ^ before found
            underlined_str = self._underlined + i + self._end
            # update line
            self._line = re.sub(i, underlined_str, self._line)


class searchWordWithMachine(SearchWords):
    """
    Class prints found lines in texts in format
    "file_name:line_number:start_position:matched_text"
    """
    def __init__(self, exp, num, line, filename):
        """
        Class constructor
        :param exp: regular expression
        :param filename: Name of file
        :param num: number of line in file
        :param line: line in file
        """
        super().__init__(exp, num, line, filename)
        self._start = 0

    def findPatterns(self):
        """
        Find start position of regular expression in line
        :return:
        """
        super().findPatterns()
        # find start position
        if re.search(self._exp, self._line):
            self._start = re.search(self._exp, self._line).span()[0]

    def __str__(self):
        """
        returns "file_name:line_number:start_position:matched_text"
        :return:
        """
        return f"{self._filename }:{str(self._num)}:{str(self._start)}:{self._line}"


class compositeSearch(searchWordsWithColor, searchWordWithUnderlined, searchWordWithMachine):
    """
    Composite class for managing command line options and invokes appropriate class
    """
    def __init__(self, exp, num, line, filename, color, underline, machine):
        """
        Class constructor
        :param exp: regular expression
        :param filename: Name of file
        :param num: number of line in file
        :param line: line in file
        :param color: option for change color
        :param underline: option for add ^
        :param machine: option for print in format
        "file_name:line_number:start_position:matched_text"
        """
        SearchWords.__init__(self, exp, num, line, filename)
        self._color = color
        self._underline = underline
        self._machine = machine
        # if color option invoke searchWordsWithColor class
        if self._color:
            searchWordsWithColor.__init__(self, exp, num, line, filename, color)
        # if underline option invoke searchWordWithUnderlined class
        if self._underline:
            searchWordWithUnderlined.__init__(self, exp, num, line, filename)
        # if machine option invoke searchWordWithMachine class
        if self._machine:
            searchWordWithMachine(exp, num, line, filename)

    def findPatterns(self):
        """
        Find patterns according to options
        :return:
        """
        SearchWords.findPatterns(self)
        # if option color update color
        if self._color:
            searchWordsWithColor.findPatterns(self)
        # if option underline update add underline
        if self._underline:
            searchWordWithUnderlined.findPatterns(self)
        # if option machine update update start position
        if self._machine:
            searchWordWithMachine.findPatterns(self)

    def __str__(self):
        """
        Print in format according to option machine
        :return:
        """
        if self._machine:
            return searchWordWithMachine.__str__(self)
        return SearchWords.__str__(self)


def enter_text_from_cmd():
    """
    Enter text from command line. For exit print q
    :return:
    """
    # Enter description message in cmd
    input("Enter your text. For exit type 'q':\n")
    # init output list of lines
    line_list = list()
    # for each line in stdin add to line_list. On exit print q
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        line_list.append(line.rstrip("\n"))
    return line_list


def init_cmd_data(num, file_line, file_name):
    """
    Create dictionary with format:
    file_name
    num
    line
    :param num: number of line
    :param file_line: line in text
    :param file_name: name of file
    :return: returns dictionary with data
    """
    data_dict = dict()
    data_dict["file_name"] = file_name
    data_dict["line_number"] = num
    data_dict["line"] = file_line
    return data_dict


def main():
    """
    Main program
    :return:
    """
    # option regular expression
    regex = None
    # option list of files
    files = None
    # option color
    color = None
    # option underline
    underline = False
    # option machine
    machine = False
    # list of dictionary in format file_name, num, line
    data_list = list()

    # Input parsing

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:f:c:um",
                                   ["help", "regex=", "files=", "color=", "underline", "machine"])
    except getopt.GetoptError:
        print('search.py -h to help')
        exit(1)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('test.py -r <regex> -f <file1,file2,...> -u <underline> -c <color> -m <machine>')
            sys.exit(0)
        if opt in ("-r", "--regex"):
            regex = arg
        if opt in ("-f", "--files"):
            files = arg.split(',')
        if opt in ("-c", "--color"):
            color = arg
        if opt in ("-u", "--underline"):
            underline = True
        if opt in ("-m", "--machine"):
            machine = True

    # prepare input
    # If option -f is empty Read from Stdin
    if files is None:
        cmd_list = enter_text_from_cmd()
        # for each line save line in line dict with format
        # file_name - stdin Input
        # line_number
        # line
        for i in range(len(cmd_list)):
            line_dict = init_cmd_data(i, cmd_list[i], "stdin Input")
            data_list.append(line_dict)
    else:
        # read text from files
        try:
            for file in files:
                # open file
                f = open(file, 'r')
                # read text
                text_lines = f.readlines()
                # for each line save line in line dict with format
                # file_name
                # line_number
                # line
                for i in range(len(text_lines) - 1):
                    line_dict = init_cmd_data(i, text_lines[i].strip("\n"), file)
                    data_list.append(line_dict)
                # close file
                f.close()
        # if file not found raise File not found exception
        except FileNotFoundError:
            print(f"Error file {file} not found")

    # commands processed
    # for each line in text create object compositeSearch
    # with parameters:
    # file_name
    # line_number
    # line
    # color
    # underline
    # machine
    for line in data_list:
        search_words = compositeSearch(regex, line["line_number"], line["line"], line["file_name"], color, underline,
                                       machine)
        # find regular expression in line
        search_words.findPatterns()
        # If found print line
        if search_words.regexFound():
            print(search_words)


if __name__ == "__main__":
    main()
