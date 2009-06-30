#!/usr/bin/env python
"""
pytme example
"""
import os.path
import pytme as T

## constructor accepts either filename or
## template string
template = T.Template('example.tpl')

## replace single tag
template.insert('DESC', 'Example.com Description')

## replace tag in repeater
template.insert('RESOURCE', 'resource 1')
## add repeater line
template.insert('RESOURCES')
template.insert('RESOURCE', 'resource 2')
template.insert('RESOURCES')
template.insert('RESOURCE', 'resource 3')
template.insert('RESOURCES')

template.insert('TITLE', 'Title 1')

## replace tag in nested repeater
template.insert('AUTHOR', 'Author 1')
## add nested repeater
template.insert('AUTHORS')
template.insert('AUTHOR', 'Author 2')
template.insert('AUTHORS')

template.insert('ITEM_DESC', 'Item number 1')
template.insert('ITEMS')

template.insert('ABOUT', 'About 2')
template.insert('TITLE', 'Title 2')
template.insert('LINK', 'link 2')
template.insert('ITEM_DESC', 'Item number 2')

template.insert('AUTHOR', 'Author 5')
template.insert('AUTHORS')
template.insert('AUTHOR', 'Author 6')
template.insert('AUTHORS')

template.insert('ITEMS')

## get processed template string
str = template.get()
print str

## save it to disk
template.write('example.xml')
