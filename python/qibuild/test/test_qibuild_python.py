## Copyright (c) 2012-2016 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

""" Finding a Python qimodule from C++

This is higly libqi specific

"""
import os

import qisys.sh

from qipy.test.conftest import qipy_action
from qitest.test.conftest import qitest_action

def test_finding_qi_python_modules(qipy_action, qibuild_action, qitest_action):
    qipy_action.add_test_project("foomodules")
    # Need to have qibuild in the worktree so that it
    # gets installed in the virtualenv and
    # qipy run -- qitest works
    this_dir = os.path.dirname(__file__)
    top_dir = os.path.join(this_dir, "..", "..", "..")
    qipy_action.worktree.add_project(top_dir)

    # Hack to make the worktree inside qibuild_action aware
    # that there are python projects registered
    worktree = qibuild_action.build_worktree.worktree
    worktree.reload()

    project = qibuild_action.add_test_project("usefoopymodule")

    # Using --no-site-packages to make sure we're not using
    # an old qibuild already installed on the system:
    qipy_action("bootstrap", "--no-site-packages")
    with qisys.sh.change_cwd(project.path):
        qibuild_action("configure")
        qipy_action("run", "--no-exec", "--", "qitest", "run")
