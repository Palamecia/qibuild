## Copyright (c) 2012-2016 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

import qisrc.svn

from qisys.test.conftest import skip_on_win

def test_commit_all_adds_new_subfolders(svn_server, tmpdir):
    foo_url = svn_server.create_repo("foo")
    work = tmpdir.mkdir("work")
    foo = work.mkdir("foo")
    svn = qisrc.svn.Svn(foo.strpath)
    svn.call("checkout", foo_url, ".")
    foo.ensure("some/sub/folder", dir=True)
    foo.ensure("some/sub/folder/bar.txt")
    svn.commit_all("test message")
    work2 = tmpdir.mkdir("work2")
    foo2 = work2.mkdir("foo2")
    svn = qisrc.svn.Svn(foo2.strpath)
    svn.call("checkout", foo_url, ".")
    assert foo2.join("some", "sub", "folder").check(dir=True)
    assert foo2.join("some", "sub", "folder", "bar.txt").check(file=True)

def test_commit_all_removes_removed_files(svn_server, tmpdir):
    foo_url = svn_server.create_repo("foo")
    svn_server.commit_file("foo", "bar.txt", "this is bar")
    work = tmpdir.mkdir("work")
    foo = work.mkdir("foo")
    svn = qisrc.svn.Svn(foo.strpath)
    svn.call("checkout", foo_url, ".")
    foo.join("bar.txt").remove()
    svn.commit_all("test message")
    work2 = tmpdir.mkdir("work2")
    foo2 = work2.mkdir("foo2")
    svn = qisrc.svn.Svn(foo2.strpath)
    svn.call("checkout", foo_url, ".")
    assert not foo2.join("bar.txt").check(file=True)

def test_files_with_space(svn_server, tmpdir):
    foo_url = svn_server.create_repo("foo")
    svn_server.commit_file("foo", "file with space.txt", "some contents\n")
    work = tmpdir.mkdir("work")
    foo = work.mkdir("foo")
    svn = qisrc.svn.Svn(foo.strpath)
    svn.call("checkout", foo_url, ".")
    foo.join("file with space.txt").remove()
    svn.commit_all("test message")

@skip_on_win
def test_file_replaced_by_symlink(svn_server, tmpdir):
    foo_url = svn_server.create_repo("foo")
    svn_server.commit_file("foo", "a.txt", "this is a\n")
    work = tmpdir.mkdir("work")
    foo = work.mkdir("foo")
    svn = qisrc.svn.Svn(foo.strpath)
    svn.call("checkout", foo_url, ".")
    foo.join("a.txt").remove()
    foo.ensure("b.txt", file=True)
    foo.join("a.txt").mksymlinkto("b.txt")
    svn.commit_all("test message")
