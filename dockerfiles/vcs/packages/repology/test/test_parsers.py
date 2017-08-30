#!/usr/bin/env python3
#
# Copyright (C) 2016 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import repology.config
from repology.package import Package
from repology.repoman import RepositoryManager


class TestParsers(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        repoman = RepositoryManager(repology.config.REPOS_DIR, 'testdata')
        self.packages = repoman.ParseMulti(reponames=['have_testdata'])

    def check_package(self, name, reference):
        reference_with_default = {
            # repo must be filled
            # family must be filled
            'subrepo': None,

            # name must be filled
            'effname': None,

            # version must be filled
            'origversion': None,
            'effversion': None,
            'versionclass': None,

            'maintainers': [],
            'category': None,
            'comment': None,
            'homepage': None,
            'licenses': [],
            'downloads': [],

            'ignore': False,
            'shadow': False,
            'ignoreversion': False,

            'extrafields': {},
        }

        reference_with_default.update(reference)

        def sort_lists(what):
            output = {}
            for key, value in what.items():
                if isinstance(value, list):
                    output[key] = sorted(value)
                else:
                    output[key] = value

            return output

        for package in self.packages:
            if package.name == name:
                self.assertEqual(
                    sort_lists(package.__dict__),
                    sort_lists(reference_with_default)
                )
                return

        self.assertFalse('package not found')

    def test_freebsd(self):
        self.check_package(
            'vorbis-tools',
            {
                'repo': 'freebsd',
                'family': 'freebsd',
                'name': 'vorbis-tools',
                'version': '1.4.0',
                'origversion': '1.4.0_10,3',
                'category': 'audio',
                'comment': 'Play, encode, and manage Ogg Vorbis files',
                'maintainers': ['naddy@freebsd.org'],
                'homepage': 'http://www.vorbis.com/',
                'extrafields': {
                    'portname': 'vorbis-tools',
                    'origin': 'audio/vorbis-tools',
                }
            }
        )

    def test_gentoo(self):
        self.check_package(
            'chromium-bsu',
            {
                'repo': 'gentoo',
                'family': 'gentoo',
                'name': 'chromium-bsu',
                'version': '0.9.15.1',
                'origversion': None,
                'category': 'games-action',
                'maintainers': ['games@gentoo.org'],
                'homepage': 'http://chromium-bsu.sourceforge.net/',
                'comment': 'Chromium B.S.U. - an arcade game',
                'downloads': ['mirror://sourceforge/chromium-bsu/chromium-bsu-0.9.15.1.tar.gz'],
                'licenses': ['Clarified-Artistic'],
            }
        )
        self.check_package(
            'asciinema',
            {
                'repo': 'gentoo',
                'family': 'gentoo',
                'name': 'asciinema',
                'version': '1.3.0',
                'origversion': None,
                'category': 'app-misc',
                'maintainers': ['kensington@gentoo.org'],
                'homepage': 'https://asciinema.org/',  # ['https://asciinema.org/', 'https://pypi.python.org/pypi/asciinema']
                'comment': 'Command line recorder for asciinema.org service',
                'downloads': ['https://github.com/asciinema/asciinema/archive/v1.3.0.tar.gz'],
                'licenses': ['GPL-3+'],
            }
        )
        self.check_package(
            'away',
            {
                'repo': 'gentoo',
                'family': 'gentoo',
                'name': 'away',
                'version': '0.9.5',
                'origversion': '0.9.5-r1',
                'category': 'app-misc',
                'maintainers': ['maintainer-needed@gentoo.org'],  # note this is generated by repoman form repo config
                'homepage': 'http://unbeatenpath.net/software/away/',
                'comment': 'Terminal locking program with few additional features',
                'downloads': ['http://unbeatenpath.net/software/away/away-0.9.5.tar.bz2'],
                'licenses': ['GPL-2'],
            }
        )
        self.check_package(
            'aspell',
            {
                'repo': 'gentoo',
                'family': 'gentoo',
                'name': 'aspell',
                'version': '0.60.7_rc1',
                'category': 'app-test',
                'maintainers': ['maintainer-needed@gentoo.org'],  # note this is generated by repoman form repo config
                'homepage': 'http://aspell.net/',
                'comment': 'A spell checker replacement for ispell',
                'downloads': ['mirror://gnu-alpha/aspell/aspell-0.60.7-rc1.tar.gz'],
                'licenses': ['LGPL-2'],
            }
        )

    def test_arch(self):
        self.check_package(
            'zlib',
            {
                'repo': 'arch',
                'family': 'arch',
                'subrepo': 'core',
                'name': 'zlib',
                'version': '1.2.8',
                'origversion': '1:1.2.8-7',
                'comment': 'Compression library implementing the deflate compression method found in gzip and PKZIP',
                'homepage': 'http://www.zlib.net/',
                'licenses': ['custom'],
                'maintainers': ['pierre@archlinux.de'],
            }
        )

    def test_cpan(self):
        self.check_package(
            'Acme-Brainfuck',
            {
                'repo': 'cpan',
                'family': 'cpan',
                'name': 'Acme-Brainfuck',
                'version': '1.1.1',
                'maintainers': ['jaldhar@cpan'],
                'homepage': 'http://search.cpan.org/dist/Acme-Brainfuck/',
                'shadow': True,
            }
        )

    def test_debian(self):
        self.check_package(
            'a52dec',
            {
                'repo': 'debian_unstable',
                'subrepo': 'main',
                'category': 'devel',
                'family': 'debuntu',
                'name': 'a52dec',
                'version': '0.7.4',
                'origversion': '0.7.4-18',
                'maintainers': [
                    'pkg-multimedia-maintainers@lists.alioth.debian.org',
                    'dmitrij.ledkov@ubuntu.com',
                    'sam+deb@zoy.org',
                    'siretart@tauware.de',
                ],
                'homepage': 'http://liba52.sourceforge.net/',
            }
        )

    def test_gobolinux(self):
        self.check_package(
            'AutoFS',
            {
                'repo': 'gobolinux',
                'family': 'gobolinux',
                'name': 'AutoFS',
                'version': '5.0.5',
                'comment': 'Automounting daemon',
                'homepage': 'ftp://ftp.kernel.org/pub/linux/daemons/autofs/',
                'downloads': [
                    'http://www.kernel.org/pub/linux/daemons/autofs/v5/autofs-5.0.5.tar.bz2'
                ],
                'licenses': ['GNU General Public License (GPL)'],
                'maintainers': ['fallback-mnt-gobolinux@repology']  # note this is generated by repoman
            }
        )

    def test_slackbuilds(self):
        # multiline DOWNLOAD
        self.check_package(
            'virtualbox',
            {
                'repo': 'slackbuilds',
                'family': 'slackbuilds',
                'name': 'virtualbox',
                'version': '5.0.30',
                'category': 'system',
                'homepage': 'http://www.virtualbox.org/',
                'downloads': [
                    'http://download.virtualbox.org/virtualbox/5.0.30/SDKRef.pdf',
                    'http://download.virtualbox.org/virtualbox/5.0.30/UserManual.pdf',
                    'http://download.virtualbox.org/virtualbox/5.0.30/VBoxGuestAdditions_5.0.30.iso',
                    'http://download.virtualbox.org/virtualbox/5.0.30/VirtualBox-5.0.30.tar.bz2',
                ],
                'maintainers': ['pprkut@liwjatan.at'],
            }
        )
        # different DOWNLOAD and DOWNLOAD_x86_64
        self.check_package(
            'baudline',
            {
                'repo': 'slackbuilds',
                'family': 'slackbuilds',
                'name': 'baudline',
                'version': '1.08',
                'category': 'ham',
                'homepage': 'http://www.baudline.com/',
                'downloads': [
                    'http://www.baudline.com/baudline_1.08_linux_i686.tar.gz',
                    'http://www.baudline.com/baudline_1.08_linux_x86_64.tar.gz',
                ],
                'maintainers': ['joshuakwood@gmail.com'],
            }
        )
        # DOWNLOAD_x86_64 is UNSUPPORTED
        self.check_package(
            'teamviewer',
            {
                'repo': 'slackbuilds',
                'family': 'slackbuilds',
                'name': 'teamviewer',
                'version': '12.0.76279',
                'category': 'network',
                'homepage': 'https://www.teamviewer.com/',
                'downloads': [
                    'https://download.teamviewer.com/download/teamviewer_i386.deb',
                ],
                'maintainers': ['willysr@slackbuilds.org'],
            }
        )
        # DOWNLOAD is UNSUPPORTED
        self.check_package(
            'oracle-xe',
            {
                'repo': 'slackbuilds',
                'family': 'slackbuilds',
                'name': 'oracle-xe',
                'version': '11.2.0',
                'category': 'system',
                'homepage': 'http://www.oracle.com/technetwork/database/database-technologies/express-edition/overview/index.html',
                'downloads': [
                    'http://download.oracle.com/otn/linux/oracle11g/xe/oracle-xe-11.2.0-1.0.x86_64.rpm.zip',
                ],
                'maintainers': ['slack.dhabyx@gmail.com'],
            }
        )
        # DOWNLOAD_x86_64 is UNTESTED
        self.check_package(
            'kforth',
            {
                'repo': 'slackbuilds',
                'family': 'slackbuilds',
                'name': 'kforth',
                'version': '1.5.2p1',
                'category': 'development',
                'homepage': 'http://ccreweb.org/software/kforth/kforth.html',
                'downloads': [
                    'ftp://ccreweb.org/software/kforth/linux/kforth-x86-linux-1.5.2.tar.gz',
                ],
                'maintainers': ['gschoen@iinet.net.au'],
            }
        )


if __name__ == '__main__':
    unittest.main()