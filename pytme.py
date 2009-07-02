#!/usr/bin/env python
# coding=utf8
"""
pytme - Tiny Template Engine

Copyright 2009 Mitja Ursic

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os.path


class Template:
    """
    String replacement class
    Atom token is a standalone template tag
    to be replaced by a value
    Repeater block is embraced by
    _START and _END markers which content is
    to be repeated multiple times
    """
    def __init__(self, input, tag_brace='##'):
        """
        Constructor accepts either file name
        or template string
        """
        if os.path.exists(input):
            self.template = open(input, 'r').read()
        else:
            self.template = input

        if not tag_brace or len(tag_brace) < 1:
            tag_brace = '##'

        self.token_brace = tag_brace
        self.token_brace_len = len(self.token_brace)
        self.token_rep_start = '_START' + self.token_brace
        self.token_rep_end = '_END' + self.token_brace
        self.rep_start_len = len(self.token_rep_start)
        self.rep_end_len = len(self.token_rep_end)

        self.tokenize(0, 0, [])

        if len(self.tokens):
            self.prepare(0, {}, [])

    def tag_name_get(self, token, type):
        """
        Append meta data to token and return it
        """
        if 'atom' == type:
            return self.token_brace + token + self.token_brace

        if 'start' == type:
            return self.token_brace + token + self.token_rep_start
        if 'end' == type:
            return self.token_brace + token + self.token_rep_end


    def token_name_get(self, tag, type):
        """
        Strip meta data from tag and return it
        """
        if 'atom' == type:
            return tag[self.token_brace_len:len(tag) -\
                             self.token_brace_len]
        if 'start' == type:
            return tag[self.token_brace_len:len(tag) -\
                            self.rep_start_len]
        if 'end' == type:
            return tag[self.token_brace_len:len(tag) -\
                            self.rep_end_len]
    

    def tokenize(self, start_pos=0, npass=0, tokens=[]):
        """
        Figure out where all template tags are
        and store their names, start and end positions in array
        """
        next_pos = self.template.find(self.token_brace, start_pos +\
                                          self.token_brace_len)
        if -1 == next_pos:
            self.tokens = tokens
            return

        ## find valid either start or end tag position
        ## start position
        if 0 == npass % 2:
            tokens.append([0,0,''])
            tokens[len(tokens) - 1][0] = next_pos
        ## end position
        else:
            pos_start = tokens[len(tokens) - 1][0]
            tokens[len(tokens) - 1][1] = pos_start
            pos_end = next_pos + self.token_brace_len
            tag = self.template[pos_start:pos_end]
            tokens[len(tokens) - 1][2] = tag

        self.tokenize(next_pos, npass + 1, tokens)


    def prepare(self,
                ntoken=0,
                tags={},
                curr_rep=[]):
        """
        Separate tokens into atoms
        and repeater blocks
        """
        curr_token = self.tokens[ntoken]
        curr_token_name = curr_token[2]
        rep_diff = len(curr_token_name) - self.rep_start_len
        start_maybe = curr_token_name[rep_diff:len(curr_token_name)]
        rep_diff = len(curr_token_name) - self.rep_end_len
        end_maybe = curr_token_name[rep_diff:len(curr_token_name)]

        ## we have start of the repeater
        if start_maybe == self.token_rep_start:
            token_name = self.token_name_get(curr_token_name, 'start')
            rep_last = curr_rep[-1] if len(curr_rep) else None
            tags[token_name] = ['r',
                                curr_token[0] +\
                                    len(curr_token_name),
                                '',
                                '',
                                rep_last]
            curr_rep.append(token_name)
        ## we have end of the repeater
        elif end_maybe == self.token_rep_end:
            token_name = self.token_name_get(curr_token_name, 'end')
            start = tags[token_name][1]
            end = curr_token[1]
            ## save blank repeater
            tags[token_name][2] = self.template[start:end]
            curr_rep.pop()
        ## we have single tag
        else:
            token_name = self.token_name_get(curr_token_name, 'atom')
            rep_last = curr_rep[-1] if len(curr_rep) else None
            tags[token_name] = ['a',
                                0,
                                curr_token_name,
                                '',
                                rep_last]
        ntoken += 1
        if (len(self.tokens) - 1) < ntoken:
            self.tags = tags
            return

        self.prepare(ntoken, tags, curr_rep)


    def atom_insert(self, token, content):
        """
        Add content to given token
        """
        for token_name in self.tags:
            if (token_name == token):
                self.tags[token][3] = content


    def block_insert(self, token, content):
        """
        Add content to given block
        """
        block = self.tags[token]
        blank = block[2]
        content = blank
        ## replace tags with atom content
        for atom in self.tags:
            if self.tags[atom][4] == token:
                content = content.replace(self.tags[atom][2],
                                          self.tags[atom][3])
                self.tags[atom][3] = ''

        ## append new content to repeater content
        self.tags[token][3] += content
        

    def insert(self, token, content=None):
        """
        Build content for given token
        """
        if not hasattr(self, 'tags'):
            return
        if not self.tags.has_key(token):
            return

        ## single tag
        if content:
            self.atom_insert(token, content)
        ## repeater block
        else:
            self.block_insert(token, content)


    def replace_atom(self, tag):
        """
        Replace template tag with its content
        """
        blank = self.tags[tag][2]
        content = self.tags[tag][3]
        self.template = self.template.replace(blank,
                                              content)


    def replace_block(self, tag):
        """
        Replace template block with its content
        """
        tag_start = self.tag_name_get(tag, 'start')
        tag_end = self.tag_name_get(tag, 'end')
        start = self.template.find(tag_start)
        end = self.template.find(tag_end) + len(tag_end)
        content = self.tags[tag][3]
        part_1 = self.template[:start]
        part_2 = self.template[end:]
        self.template = part_1 + content + part_2


    def replace(self):
        """
        Replace root tags and repeater blocks
        with their values
        """
        if not hasattr(self, 'tags'):
            return
        
        for tag in self.tags:
            ## process root tags
            if not self.tags[tag][4]:
                ## replace single tag (atom)
                if 'a' == self.tags[tag][0]:
                    self.replace_atom(tag)
                ## replace repeater block
                if 'r' == self.tags[tag][0]:
                    self.replace_block(tag)


    def clean(self):
        """
        Remove all blocks and template tags
        """
        for token in self.tokens:
            self.template = self.template.replace(token[2], '')


    def process(self):
        """
        Produce final output and
        clean it up
        """
        
        if hasattr(self, 'output'):
            return

        self.replace()
        self.clean()
        self.output = self.template


    def get(self):
        """
        Return processed template string
        """
        self.process()
        return self.output


    def write(self, filename):
        """
        Write processed template string into
        file with given filename
        """
        self.process()
        self.template = open(filename, 'w').write(self.output)
