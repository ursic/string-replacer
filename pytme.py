#!/usr/bin/env python
# coding=utf8
"""
String replacer for HTML templating

odtihmal@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Example usage:
t = pytme.Template(<TEMPLATE_FILE_PATH> or <TEMPLATE_STRING>)

# Insert single data point.
t.insert('TITLE', 'Article title')
# Insert repeater.
t.insert('ARTICLE')

# Write to file.
t.write(<SAVE_TO_PATH>)

# Get template string.
t.get()
"""
import os.path


# Return locations of all needles in given haystack.
def find_locs(needle, haystack):
    curr_loc = 0
    while True:
        loc = haystack.find(needle, curr_loc)
        if -1 == loc: return
        yield loc
        curr_loc = loc + len(needle)


class Template:
    """
    """
    def __init__(self, path_or_str, brace = '##'):
        """
        Constructor accepts either file name
        or template string
        """
        if os.path.exists(path_or_str):
            self.t = open(path_or_str, 'r').read()
        else:
            self.t = path_or_str

        if not brace or len(brace) < 1:
            brace = '##'

        self.brace = brace
        self.rep_start = '_START' + self.brace
        self.rep_end = '_END' + self.brace
        self.repeaters = {}

        self.repeaters = self.extract_reps(self.t)


    # Extract and return repeaters in haystack.
    def extract_reps(self, haystack):
        reps = {}
        # Find repeater names and their content.
        for rep in list(find_locs(self.rep_start, haystack)):
            min_pos = rep - 1
            i = 1
            m = None
            # Find its beginning.
            while (self.brace != m):
                m = haystack[min_pos - (i + len(self.brace)):min_pos - i]
                i += 1

            # Extract its name.
            start_pos = rep - (i + len(self.brace))
            start = haystack[start_pos:rep] + self.rep_start
            name = start[len(self.brace):-len(self.rep_start)]
            end = self.brace + name + self.rep_end
            # Look for matching end tag.
            if -1 == haystack.find(end): continue
            # Extract its content.
            reps[name] = haystack[(start_pos):(haystack.find(end) + len(end))]
                
        return reps


    # Remove repeaters in haystack.
    # Return haystack.
    def remove_reps(self, haystack):
        for name, block in self.extract_reps(haystack).items():
            haystack = haystack.replace(block, '')
        return haystack


    # Replace either single tag with given string.
    # Or a repeater.
    def insert(self, rep, replacement = None):
        # Replace single tags.
        if None != replacement:
            tag = self.brace + rep + self.brace
            self.t = self.t.replace(tag, str(replacement))

        # Fill blank repeater.
        # Insert filled block into the template.
        # Append blank repeater at the end of insertion.
        elif rep in self.repeaters:
            start = self.brace + rep + self.rep_start
            end = self.brace + rep + self.rep_end
            start_pos = self.t.find(start) + len(start)
            end_pos = self.t.find(end)
            content = self.remove_reps(self.t[start_pos:end_pos]) + self.repeaters[rep]
            start_pos -= len(start)
            end_pos += len(end)
            self.t = self.t[:start_pos] + content + self.t[end_pos:]


    def get(self):
        """
        Return clean template string.
        """
        output = self.remove_reps(self.t)
        return output


    def write(self, filename):
        """
        Write clean template string into
        filename.
        """
        open(filename, 'w').write(self.remove_reps(self.t))
