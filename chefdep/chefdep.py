#!/usr/bin/env python2.7

# Copyright (c) 2016, Brian Wiborg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import re
import sys
import logging
from collections import OrderedDict
from glob import glob

__author__ = 'Brian Wiborg <brian.wiborg@imagineeasy.com>'
__license__ = 'BSD/2-Clause'

# Setup logging interface.
logging.basicConfig(level=logging.DEBUG, format="%(msg)s")
logger = logging.getLogger()

# Global variables.
CMD = sys.argv[0]
ARGS = sys.argv[1:]
REGEX = re.compile(r"^\s*include_recipe\s'(?P<recipe>.*)'$")
ROOT = ''
DEPS = OrderedDict()


def set_root(path):
    """Find and set the root directory for all cookbooks based on a recipe path.

    :param path:    str     - Path of recipe.
    """

    global ROOT
    if not ROOT:
        ROOT = os.path.relpath(os.path.join(os.path.split(path)[0], '..', '..'))


def path_to_dep(path):
    """Convert a recipe path to a dependency string.

    :param path:    str     - Path to recipe.
    :return:        str     - <cookbook>::<recipe>
    """

    cookbook, _, recipe = path.split(os.path.sep)[-3:]
    return "{}::{}".format(cookbook, recipe.split('.')[0])


def dep_to_path(dep):
    """Convert a dependency string to a recipe path.

    :param dep:     str     - <cookbook>::<recipe>
    :return:        str     - ./<cookbook>/recipes/<recipe>.rb
    """

    if '::' in dep:
        recipe_path = os.path.sep + 'recipes' + os.path.sep
        return os.path.join(ROOT, dep.replace('::', recipe_path)) + '.rb'
    else:
        return os.path.join(ROOT, dep, 'recipes', 'default.rb')


def resolve_deps(path):
    """Resolve the dependencies of any given recipe.

    :param path:    str     - Path of root recipe.
    """

    global DEPS

    if not os.path.exists(path):
        logger.fatal("File not found: {}".format(path))
        sys.exit(1)

    set_root(path)

    try:
        fd = open(path, 'r')

    except IOError:
        logger.fatal('Can not read: {}'.format(path))
        sys.exit(1)

    recipe = path_to_dep(path)
    DEPS[recipe] = []
    for line in fd.readlines():
        match = REGEX.match(line)
        if match:
            dep = match.group(1)
            DEPS[recipe].append(dep)

    for dep in DEPS[recipe]:
        if dep not in DEPS:
            resolve_deps(dep_to_path(dep))


def resolve_revdeps(path):
    """Resolve the reverse dependencies of any given recipe.

    :param path:    str     - Path of dependency recipe.
    """

    global DEPS

    if not os.path.exists(path):
        logger.fatal("File not found: {}".format(path))

    set_root(path)

    dependency = path_to_dep(path)
    DEPS[dependency] = []
    for recipe in glob(os.path.join(ROOT, '*', 'recipes', '*.rb')):

        try:
            fd = open(recipe, 'r')

        except IOError:
            logger.fatal("Can not read: {}".format(recipe))
            sys.exit(1)

        for line in fd.readlines():
            match = REGEX.match(line)
            if match:
                dep = match.group(1)
                if dep == dependency:
                    DEPS[dependency].append(path_to_dep(recipe))


if __name__ == '__main__':
    if os.path.basename(CMD) == 'chefdep':
        for path in ARGS:
            resolve_deps(path)

        for cookbook, deps in DEPS.iteritems():
            print(cookbook)

    elif os.path.basename(CMD) == 'chefrevdep':
        for path in ARGS:
            resolve_revdeps(path)

        for cookbook, deps in DEPS.iteritems():
            for dep in deps:
                print(dep)
