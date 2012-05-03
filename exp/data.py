#!/usr/bin/python
# coding=utf8

__author__ = "zhangchitc@gmail.com"


class Paper:

    def __init__ (self, title):
        self.title = title
        self.authors = []

    def add_author (self, author):
        self.authors.append (author)

    def __str__ (self):
        ret = "Title:\n     %s\n" % self.title
        ret += "Authors:\n"
        for author in self.authors:
            ret += "     %s\n" % author
        ret += "\n\n"
        return ret


class Author:

    def __init__ (self, name, affn):
        self.name = name
        self.affn = affn

    def __str__ (self):
        ret = "%s (%s)" % (self.name, self.affn)
        return unicode (ret).encode ('utf-8')


if __name__ == '__main__':
    print Paper ('abc')
    print Author ('abc', 'def')
