# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2024 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the strip extension interface.
"""

from PyQt6.QtWidgets import QDialog

from ..HgDialog import HgDialog
from ..HgExtension import HgExtension


class Strip(HgExtension):
    """
    Class implementing the strip extension interface.
    """

    def __init__(self, vcs, ui=None):
        """
        Constructor

        @param vcs reference to the Mercurial vcs object
        @type Hg
        @param ui reference to a UI widget (defaults to None)
        @type QWidget
        """
        super().__init__(vcs, ui=ui)

    def hgStrip(self, rev=""):
        """
        Public method to strip revisions from a repository.

        @param rev revision to strip from
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        from .HgStripDialog import HgStripDialog

        res = False
        dlg = HgStripDialog(
            self.vcs.hgGetTagsList(),
            self.vcs.hgGetBranchesList(),
            self.vcs.hgGetBookmarksList(),
            rev,
            parent=self.ui,
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            rev, bookmark, force, noBackup, keep = dlg.getData()

            args = self.vcs.initCommand("strip")
            if bookmark:
                args.append("--bookmark")
                args.append(bookmark)
            if force:
                args.append("--force")
            if noBackup:
                args.append("--no-backup")
            if keep:
                args.append("--keep")
            args.append("-v")
            args.append(rev)

            dia = HgDialog(
                self.tr("Stripping changesets from repository"),
                hg=self.vcs,
                parent=self.ui,
            )
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.vcs.checkVCSStatus()
        return res
