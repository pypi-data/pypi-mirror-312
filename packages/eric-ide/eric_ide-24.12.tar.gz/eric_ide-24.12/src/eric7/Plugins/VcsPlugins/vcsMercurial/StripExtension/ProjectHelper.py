# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2024 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the strip extension project helper.
"""

from PyQt6.QtWidgets import QMenu

from eric7.EricGui import EricPixmapCache
from eric7.EricGui.EricAction import EricAction
from eric7.EricWidgets import EricMessageBox

from ..HgExtensionProjectHelper import HgExtensionProjectHelper


class StripProjectHelper(HgExtensionProjectHelper):
    """
    Class implementing the strip extension project helper.
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

    def initActions(self):
        """
        Public method to generate the action objects.
        """
        self.hgStripAct = EricAction(
            self.tr("Strip changesets"),
            EricPixmapCache.getIcon("fileDelete"),
            self.tr("Strip changesets"),
            0,
            0,
            self,
            "mercurial_strip",
        )
        self.hgStripAct.setStatusTip(self.tr("Strip changesets from a repository"))
        self.hgStripAct.setWhatsThis(
            self.tr(
                """<b>Strip changesets</b>"""
                """<p>This deletes a changeset and all its descendants"""
                """ from a repository. Each removed changeset will be"""
                """ stored in .hg/strip-backup as a bundle file.</p>"""
            )
        )
        self.hgStripAct.triggered.connect(self.__hgStrip)
        self.actions.append(self.hgStripAct)

    def initMenu(self, mainMenu):
        """
        Public method to generate the extension menu.

        @param mainMenu reference to the main menu
        @type QMenu
        @return populated menu
        @rtype QMenu
        """
        menu = QMenu(self.menuTitle(), mainMenu)
        menu.setIcon(EricPixmapCache.getIcon("fileDelete"))
        menu.setTearOffEnabled(True)

        menu.addAction(self.hgStripAct)

        return menu

    def menuTitle(self):
        """
        Public method to get the menu title.

        @return title of the menu
        @rtype str
        """
        return self.tr("Strip")

    def __hgStrip(self):
        """
        Private slot used to strip revisions from a repository.
        """
        shouldReopen = self.vcs.getExtensionObject("strip").hgStrip(
            self.project.getProjectPath()
        )
        if shouldReopen:
            res = EricMessageBox.yesNo(
                None,
                self.tr("Strip"),
                self.tr("""The project should be reread. Do this now?"""),
                yesDefault=True,
            )
            if res:
                self.project.reopenProject()
