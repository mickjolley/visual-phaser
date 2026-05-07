#Boa:Frame:VPConfigBoaFrame
# -*- coding: utf-8 -*-
"""Boa-managed configuration editor for Visual_Phaser.V1.0.py"""

import os
import re
import glob
import subprocess
import sys
import threading

import wx

from VP_Config_Resources import FIELD_DEFINITIONS


TOOLTIPS = {
    'FILES_PATH': 'Path to folder where the DNA files are stored.',
    'WORKING_DIRECTORY': 'Folder where the .xlsx and .py files will be stored.',
    'MAP_PATH': 'Path to folder containing min_map.txt.',
    'SIBLINGS': 'Two minimum. Make sure that the DNA files are in the PixelChromosomeView (PCV) format.',
    'PHASED_FILES': 'Enter names of phased files to be compared to each other. They will not be compared to siblings. The default assignment for no calls is "X".',
    'EVIL_TWINS': 'Evil Twin files to be compared to SIBLINGS.',
    'COUSINS': 'Enter names of individuals to be compared with all SIBLINGS in a pre-existing file. Leave blank ([]) when creating a new file.',
    'CHROMOSOMES': 'Chromosome selected (1-23). More than one chromosome may be entered if comma-separated. Leave empty for all chromosomes.',
    'EXCEL_FILE_NAME': 'Name of the .xlsx file. Do not include the ".xlsx", This is added automatically.',
    'SHOW_NO_MATCHES': 'Set to False if the display of match pairs with no matching segments is not desired.',
    'CHROM_TRUE_SIZE': 'Set to True for true size. Set to False for normalized size.',
    'LINEAR_CHROMOSOME': 'Set to True if you want to see the linearized chromosomes.',
    'MERGE_FILES': 'Set to True if merging of DNA files is desired. If it is desired to treat match pairs separately, set to False.',
    'RESOLUTION': 'Default value = 1. For normalized size it is advised to keep it under 10.',
    'AUTO_REC_PNTS': 'Set AUTO_REC_PNTS to True if calculation of RPs is desired.',
    'ARP_TOLERANCE': 'When AUTO_REC_PNTS is activated, columns with pixel size less than this value will be deleted.',
    'AUTO_RP_ASSIGN': 'Set AUTO_RP_ASSIGN to True if automatic assignment of recombination points is desired.',
    'REPAIR_FILES': 'Converts isolated NIR and HIR SNPs to FIR. Converts isolated NIR SNPs to HIR.',
    'SCALE_FACTOR': 'The column width per pixel factor.',
    'HIR_CUTOFF': 'Default value = 7 cM',
    'FIR_CUTOFF': 'Default value = 1 cM.',
    'X_HIR_CUTOFF': 'X chromosome cutoff (cM). The default is 15.',
    'X_FIR_CUTOFF': 'X chromosome FIR cutoff (cM). The default 15.',
    'FIR_TABLES': 'Set to True if display of FIR tables is desired.',
    'SCALE_ON': 'Turn scale on and off. Set to False if not required.',
    'FREEZE_COLUMN': 'Set to "A" if freezing not desired. Default = "A".',
    'LINUX_FONT_STRING': 'Linux users only. Enter the path to your font.',
    'SHOW_TIMES': 'Elapsed times are shown for each step. Default =True',
    'SHOW_MATCH_PAIR_PROGRESS': "Notifies the completion of each step. Set to False if you don't want to see this. Default = True",
    'HIR_SNP_MIN': 'Minimum number of HIR SNPs. Default value = 200',
    'FIR_SNP_MIN': 'Minimum number of FIR SNPs. Default value = 75',
    'MM_DIST': 'Number of Kbs between mismatches to end segment. Default = 1000.',
    'NO_CALL': 'Character assigned to a no-call IN PHASED FILES.',
}


LIST_FIELDS = ('SIBLINGS', 'COUSINS', 'CHROMOSOMES')
LINE_LIST_FIELDS = ('PHASED_FILES', 'EVIL_TWINS')
BOOLEAN_FIELDS = (
    'SHOW_NO_MATCHES', 'CHROM_TRUE_SIZE', 'LINEAR_CHROMOSOME', 'MERGE_FILES',
    'AUTO_REC_PNTS', 'AUTO_RP_ASSIGN', 'REPAIR_FILES', 'FIR_TABLES',
    'SCALE_ON', 'SHOW_TIMES', 'SHOW_MATCH_PAIR_PROGRESS'
)
INTEGER_FIELDS = (
    'RESOLUTION', 'ARP_TOLERANCE', 'HIR_CUTOFF', 'FIR_CUTOFF', 'X_HIR_CUTOFF',
    'X_FIR_CUTOFF', 'HIR_SNP_MIN', 'FIR_SNP_MIN', 'MM_DIST'
)
FLOAT_FIELDS = ('SCALE_FACTOR',)
RAW_STRING_FIELDS = ('FILES_PATH', 'WORKING_DIRECTORY', 'MAP_PATH', 'LINUX_FONT_STRING')


def create(parent):
    return VPConfigBoaFrame(parent)


[wxID_VPCONFIGBOAFRAME, wxID_VPCONFIGBOAFRAMEACTIONSSPACERPANEL,
 wxID_VPCONFIGBOAFRAMEARPTOLERANCELABEL,
 wxID_VPCONFIGBOAFRAMEARPTOLERANCESPIN, wxID_VPCONFIGBOAFRAMEAUTORECPNTSCOMBO,
 wxID_VPCONFIGBOAFRAMEAUTORECPNTSLABEL,
 wxID_VPCONFIGBOAFRAMEAUTORPASSIGNCOMBO,
 wxID_VPCONFIGBOAFRAMEAUTORPASSIGNLABEL, wxID_VPCONFIGBOAFRAMEBOOLPANEL,
 wxID_VPCONFIGBOAFRAMEBROWSEFILESPATHBUTTON,
 wxID_VPCONFIGBOAFRAMEBROWSEMAPPATHBUTTON,
 wxID_VPCONFIGBOAFRAMEBROWSEWORKINGDIRBUTTON,
 wxID_VPCONFIGBOAFRAMECHROMOSOMESLABEL, wxID_VPCONFIGBOAFRAMECHROMOSOMESTEXT,
 wxID_VPCONFIGBOAFRAMECHROMTRUESIZECOMBO,
 wxID_VPCONFIGBOAFRAMECHROMTRUESIZELABEL, wxID_VPCONFIGBOAFRAMECLOSEBUTTON,
 wxID_VPCONFIGBOAFRAMECONFIGBOOK, wxID_VPCONFIGBOAFRAMECOUSINSLABEL,
 wxID_VPCONFIGBOAFRAMECOUSINSTEXT, wxID_VPCONFIGBOAFRAMEEVILTWINSLABEL,
 wxID_VPCONFIGBOAFRAMEEVILTWINSTEXT, wxID_VPCONFIGBOAFRAMEEXCELFILENAMELABEL,
 wxID_VPCONFIGBOAFRAMEEXCELFILENAMETEXT, wxID_VPCONFIGBOAFRAMEFILESPANEL,
 wxID_VPCONFIGBOAFRAMEFILESPATHLABEL, wxID_VPCONFIGBOAFRAMEFILESPATHTEXT,
 wxID_VPCONFIGBOAFRAMEFIRCUTOFFLABEL, wxID_VPCONFIGBOAFRAMEFIRCUTOFFSPIN,
 wxID_VPCONFIGBOAFRAMEFIRSNPMINLABEL, wxID_VPCONFIGBOAFRAMEFIRSNPMINSPIN,
 wxID_VPCONFIGBOAFRAMEFIRTABLESCOMBO, wxID_VPCONFIGBOAFRAMEFIRTABLESLABEL,
 wxID_VPCONFIGBOAFRAMEFREEZECOLUMNLABEL,
 wxID_VPCONFIGBOAFRAMEFREEZECOLUMNTEXT, wxID_VPCONFIGBOAFRAMEHIRCUTOFFLABEL,
 wxID_VPCONFIGBOAFRAMEHIRCUTOFFSPIN, wxID_VPCONFIGBOAFRAMEHIRSNPMINLABEL,
 wxID_VPCONFIGBOAFRAMEHIRSNPMINSPIN, wxID_VPCONFIGBOAFRAMELINEARCHROMCOMBO,
 wxID_VPCONFIGBOAFRAMELINEARCHROMLABEL, wxID_VPCONFIGBOAFRAMELINUXFONTLABEL,
 wxID_VPCONFIGBOAFRAMELINUXFONTTEXT, wxID_VPCONFIGBOAFRAMELOADBUTTON,
 wxID_VPCONFIGBOAFRAMEMAPPATHLABEL, wxID_VPCONFIGBOAFRAMEMAPPATHTEXT,
 wxID_VPCONFIGBOAFRAMEMERGEFILESCOMBO, wxID_VPCONFIGBOAFRAMEMERGEFILESLABEL,
 wxID_VPCONFIGBOAFRAMEMMDISTLABEL, wxID_VPCONFIGBOAFRAMEMMDISTSPIN,
 wxID_VPCONFIGBOAFRAMENOCALLLABEL, wxID_VPCONFIGBOAFRAMENOCALLTEXT,
 wxID_VPCONFIGBOAFRAMENUMERICPANEL, wxID_VPCONFIGBOAFRAMEPATHSPANEL,
 wxID_VPCONFIGBOAFRAMEPHASEDFILESLABEL,
 wxID_VPCONFIGBOAFRAMEPHASEDFILESTEXT,
 wxID_VPCONFIGBOAFRAMEPROGRAMOUTPUTCLEARBUTTON,
 wxID_VPCONFIGBOAFRAMEPROGRAMOUTPUTLABEL,
 wxID_VPCONFIGBOAFRAMEPROGRAMOUTPUTTEXT,
 wxID_VPCONFIGBOAFRAMEREPAIRFILESCOMBO, wxID_VPCONFIGBOAFRAMEREPAIRFILESLABEL,
 wxID_VPCONFIGBOAFRAMERESETBUTTON, wxID_VPCONFIGBOAFRAMERESOLUTIONLABEL,
 wxID_VPCONFIGBOAFRAMERESOLUTIONSPIN, wxID_VPCONFIGBOAFRAMERUNBUTTON,
 wxID_VPCONFIGBOAFRAMESAVEBUTTON, wxID_VPCONFIGBOAFRAMESCALEFACTORLABEL,
 wxID_VPCONFIGBOAFRAMESCALEFACTORTEXT, wxID_VPCONFIGBOAFRAMESCALEONCOMBO,
 wxID_VPCONFIGBOAFRAMESCALEONLABEL,
 wxID_VPCONFIGBOAFRAMESHOWMATCHPAIRPROGRESSCOMBO,
 wxID_VPCONFIGBOAFRAMESHOWMATCHPAIRPROGRESSLABEL,
 wxID_VPCONFIGBOAFRAMESHOWNOMATCHESCOMBO,
 wxID_VPCONFIGBOAFRAMESHOWNOMATCHESLABEL, wxID_VPCONFIGBOAFRAMESHOWTIMESCOMBO,
 wxID_VPCONFIGBOAFRAMESHOWTIMESLABEL, wxID_VPCONFIGBOAFRAMESIBLINGSLABEL,
 wxID_VPCONFIGBOAFRAMESIBLINGSTEXT, wxID_VPCONFIGBOAFRAMESTATICLINE1,
 wxID_VPCONFIGBOAFRAMESTATUSBAR, wxID_VPCONFIGBOAFRAMETITLETEXT,
 wxID_VPCONFIGBOAFRAMEWORKINGDIRECTORYLABEL,
 wxID_VPCONFIGBOAFRAMEWORKINGDIRTEXT, wxID_VPCONFIGBOAFRAMEXFIRCUTOFFLABEL,
 wxID_VPCONFIGBOAFRAMEXFIRCUTOFFSPIN, wxID_VPCONFIGBOAFRAMEXHIRCUTOFFLABEL,
 wxID_VPCONFIGBOAFRAMEXHIRCUTOFFSPIN,
] = [wx.NewIdRef() for _init_ctrls in range(87)]


[wxID_VPCONFIGBOAFRAMEEXITITEM, wxID_VPCONFIGBOAFRAMELOADITEM,
 wxID_VPCONFIGBOAFRAMESAVEITEM,
] = [wx.NewIdRef() for _init_coll_fileMenu_Items in range(3)]

[wxID_VPCONFIGBOAFRAMEABOUTITEM] = [wx.NewIdRef() for _init_coll_helpMenu_Items in range(1)]

class VPConfigBoaFrame(wx.Frame):
    def _init_coll_numericGridSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.resolutionLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.resolutionSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.arpToleranceLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.arpToleranceSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.hirCutoffLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.hirCutoffSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.firCutoffLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.firCutoffSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.xHirCutoffLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.xHirCutoffSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.xFirCutoffLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.xFirCutoffSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.hirSnpMinLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.hirSnpMinSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.firSnpMinLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.firSnpMinSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.mmDistLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.mmDistSpin, 0, border=5, flag=wx.ALL)
        parent.Add(self.scaleFactorLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.scaleFactorText, 0, border=5, flag=wx.ALL | wx.EXPAND)

    def _init_coll_boolGridSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.showNoMatchesLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.showNoMatchesCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.chromTrueSizeLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.chromTrueSizeCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.linearChromLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.linearChromCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.mergeFilesLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.mergeFilesCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.autoRecPntsLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.autoRecPntsCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.autoRpAssignLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.autoRpAssignCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.repairFilesLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.repairFilesCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.firTablesLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.firTablesCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.scaleOnLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.scaleOnCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.showTimesLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.showTimesCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.showMatchPairProgressLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.showMatchPairProgressCombo, 0, border=5, flag=wx.ALL)
        parent.Add(self.freezeColumnLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.freezeColumnText, 0, border=5, flag=wx.ALL)
        parent.Add(self.noCallLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.noCallText, 0, border=5, flag=wx.ALL)
        parent.Add(self.linuxFontLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        parent.Add(self.linuxFontText, 0, border=5, flag=wx.ALL | wx.EXPAND)

    def _init_coll_actionsSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.loadButton, 0, border=0, flag=0)
        parent.Add(self.saveButton, 0, border=8, flag=wx.LEFT)
        parent.Add(self.resetButton, 0, border=8, flag=wx.LEFT)
        parent.Add(self.actionsSpacerPanel, 1, border=0, flag=wx.EXPAND)
        parent.Add(self.runButton, 0, border=0, flag=wx.RIGHT)
        parent.Add(self.closeButton, 0, border=8, flag=wx.LEFT)

    def _init_coll_numericSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.numericGridSizer, 0, border=8, flag=wx.ALL | wx.EXPAND)

    def _init_coll_boolSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.boolGridSizer, 0, border=8, flag=wx.ALL | wx.EXPAND)

    def _init_coll_filesSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.siblingsSizer, 0, border=8,
              flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND)
        parent.Add(self.cousinsSizer, 0, border=8,
              flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND)
        parent.Add(self.phasedFilesSizer, 0, border=8,
              flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND)
        parent.Add(self.evilTwinsSizer, 0, border=8,
              flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND)
        parent.Add(self.chromosomesSizer, 0, border=8, flag=wx.ALL | wx.EXPAND)

    def _init_coll_mainSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.configBook, 1, border=8, flag=wx.ALL | wx.EXPAND)
        parent.Add(self.staticLine1, 0, border=0, flag=wx.EXPAND)
        parent.Add(self.actionsSizer, 0, border=8, flag=wx.ALL | wx.EXPAND)

    def _init_coll_helpMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='About this application',
              id=wxID_VPCONFIGBOAFRAMEABOUTITEM, item='&About')

    def _init_coll_fileMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='Load configuration file',
              id=wxID_VPCONFIGBOAFRAMELOADITEM, item='&Load Config\tCtrl+O')
        parent.Append(helpString='Save configuration file',
              id=wxID_VPCONFIGBOAFRAMESAVEITEM, item='&Save Config\tCtrl+S')
        parent.AppendSeparator()
        parent.Append(helpString='Exit application',
              id=wxID_VPCONFIGBOAFRAMEEXITITEM, item='E&xit')

    def _init_coll_menuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.fileMenu, title='&File')
        parent.Append(menu=self.helpMenu, title='&Help')

    def _init_coll_configBook_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.pathsPanel, select=True,
              text='Paths')
        parent.AddPage(imageId=-1, page=self.filesPanel, select=False,
              text='Input Files')
        parent.AddPage(imageId=-1, page=self.boolPanel, select=False,
              text='Generation Options')
        parent.AddPage(imageId=-1, page=self.numericPanel, select=False,
              text='Algorithm Factors')

    def _init_coll_statusBar_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(3)

        parent.SetFieldsCount(1)
        parent.SetStatusText(i=0, text='Ready')
        parent.SetStatusWidths([-1])

        parent.SetStatusWidths([-1])

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar = wx.MenuBar()

        self.fileMenu = wx.Menu(title='')

        self.helpMenu = wx.Menu(title='')

        self._init_coll_menuBar_Menus(self.menuBar)
        self._init_coll_fileMenu_Items(self.fileMenu)
        self._init_coll_helpMenu_Items(self.helpMenu)

    def _init_sizers(self):
        # generated method, don't edit
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.filesSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.boolSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.numericSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.actionsSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.filesPathRowSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.filesPathRowSizer.Add(self.filesPathLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        self.filesPathRowSizer.Add(self.filesPathText, 0, border=5, flag=wx.ALL)
        self.filesPathRowSizer.Add(self.browseFilesPathButton, 0, border=5,
              flag=wx.ALL)

        self.workingDirectoryRowSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.workingDirectoryRowSizer.Add(self.workingDirectoryLabel, 0,
              border=5, flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        self.workingDirectoryRowSizer.Add(self.workingDirText, 0, border=5,
              flag=wx.ALL)
        self.workingDirectoryRowSizer.Add(self.browseWorkingDirButton, 0,
              border=5, flag=wx.ALL)

        self.mapPathRowSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.mapPathRowSizer.Add(self.mapPathLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        self.mapPathRowSizer.Add(self.mapPathText, 0, border=5, flag=wx.ALL)
        self.mapPathRowSizer.Add(self.browseMapPathButton, 0, border=5,
              flag=wx.ALL)

        self.siblingsSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.siblingsSizer.Add(self.siblingsLabel, 0, border=5, flag=wx.ALL)
        self.siblingsSizer.Add(self.siblingsText, 0, border=5,
              flag=int(wx.LEFT) | int(wx.RIGHT) | int(wx.BOTTOM) | int(wx.EXPAND))

        self.phasedFilesSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.phasedFilesSizer.Add(self.phasedFilesLabel, 0, border=5,
              flag=wx.ALL)
        self.phasedFilesSizer.Add(self.phasedFilesText, 0, border=5,
              flag=int(wx.LEFT) | int(wx.RIGHT) | int(wx.BOTTOM) | int(wx.EXPAND))

        self.evilTwinsSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.evilTwinsSizer.Add(self.evilTwinsLabel, 0, border=5,
              flag=wx.ALL)
        self.evilTwinsSizer.Add(self.evilTwinsText, 0, border=5,
              flag=int(wx.LEFT) | int(wx.RIGHT) | int(wx.BOTTOM) | int(wx.EXPAND))

        self.cousinsSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.cousinsSizer.Add(self.cousinsLabel, 0, border=5, flag=wx.ALL)
        self.cousinsSizer.Add(self.cousinsText, 0, border=5,
              flag=int(wx.LEFT) | int(wx.RIGHT) | int(wx.BOTTOM) | int(wx.EXPAND))

        self.chromosomesSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.chromosomesSizer.Add(self.chromosomesLabel, 0, border=5,
              flag=wx.ALL)
        self.chromosomesSizer.Add(self.chromosomesText, 0, border=5,
              flag=int(wx.LEFT) | int(wx.RIGHT) | int(wx.BOTTOM) | int(wx.EXPAND))

        self.boolGridSizer = wx.FlexGridSizer(cols=2, hgap=8, rows=14, vgap=0)

        self.numericGridSizer = wx.FlexGridSizer(cols=2, hgap=8, rows=10,
              vgap=0)

        self.excelFileSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.excelFileSizer.Add(self.excelFileNameLabel, 0, border=5,
              flag=int(wx.ALIGN_CENTER_VERTICAL) | int(wx.ALL))
        self.excelFileSizer.Add(self.excelFileNameText, 0, border=5,
              flag=wx.ALL)

        self._init_coll_mainSizer_Items(self.mainSizer)
        self._init_coll_filesSizer_Items(self.filesSizer)
        self._init_coll_boolSizer_Items(self.boolSizer)
        self._init_coll_numericSizer_Items(self.numericSizer)
        self._init_coll_actionsSizer_Items(self.actionsSizer)
        self._init_coll_boolGridSizer_Items(self.boolGridSizer)
        self._init_coll_numericGridSizer_Items(self.numericGridSizer)

        self.filesPanel.SetSizer(self.filesSizer)
        self.boolPanel.SetSizer(self.boolSizer)
        self.numericPanel.SetSizer(self.numericSizer)
        self.SetSizer(self.mainSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_VPCONFIGBOAFRAME,
              name='VPConfigBoaFrame', parent=prnt, pos=wx.Point(401, 98),
              size=wx.Size(771, 641), style=wx.DEFAULT_FRAME_STYLE,
              title='Visual Phaser Configuration Editor')
        self._init_utils()
        self.SetClientSize(wx.Size(755, 602))
        self.SetMenuBar(self.menuBar)
        self.Bind(wx.EVT_MENU, self.OnLoadConfigMenu,
              id=wxID_VPCONFIGBOAFRAMELOADITEM)
        self.Bind(wx.EVT_MENU, self.OnSaveConfigMenu,
              id=wxID_VPCONFIGBOAFRAMESAVEITEM)
        self.Bind(wx.EVT_MENU, self.OnExitMenu,
              id=wxID_VPCONFIGBOAFRAMEEXITITEM)
        self.Bind(wx.EVT_MENU, self.OnAboutMenu,
              id=wxID_VPCONFIGBOAFRAMEABOUTITEM)
        self.Bind(wx.EVT_CLOSE, self.OnWindowClose)

        self.statusBar = wx.StatusBar(id=wxID_VPCONFIGBOAFRAMESTATUSBAR,
              name='statusBar', parent=self, style=0)
        self.statusBar.SetPosition(wx.Point(0, 0))
        self.statusBar.SetSize(wx.Size(964, 20))
        self._init_coll_statusBar_Fields(self.statusBar)
        self.SetStatusBar(self.statusBar)

        self.configBook = wx.Notebook(id=wxID_VPCONFIGBOAFRAMECONFIGBOOK,
              name='configBook', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(739, 545), style=0)
        self.configBook.SetToolTip('configBook')

        self.pathsPanel = wx.Panel(id=wxID_VPCONFIGBOAFRAMEPATHSPANEL,
              name='pathsPanel', parent=self.configBook, pos=wx.Point(0, 0),
              size=wx.Size(731, 517), style=wx.TAB_TRAVERSAL)

        self.titleText = wx.StaticText(id=wxID_VPCONFIGBOAFRAMETITLETEXT,
              label='Visual Phaser Configuration Settings', name='titleText',
              parent=self.pathsPanel, pos=wx.Point(8, 8), size=wx.Size(208, 17),
              style=0)

        self.filesPathLabel = wx.StaticText(id=wx.ID_ANY,
              label='DNA Files Path', name='filesPathLabel',
              parent=self.pathsPanel, pos=wx.Point(8, 58), size=wx.Size(140,
              17), style=0)

        self.filesPathText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMEFILESPATHTEXT,
              name='filesPathText', parent=self.pathsPanel, pos=wx.Point(156,
              58), size=wx.Size(439, 21), style=0, value='')
        self.filesPathText.SetToolTip('Path to where the raw DNA files are.')

        self.browseFilesPathButton = wx.Button(id=wxID_VPCONFIGBOAFRAMEBROWSEFILESPATHBUTTON,
              label='Browse...', name='browseFilesPathButton',
              parent=self.pathsPanel, pos=wx.Point(603, 58), size=wx.Size(90,
              23), style=0)
        self.browseFilesPathButton.Bind(wx.EVT_BUTTON,
              self.OnBrowseFilesPathButton,
              id=wxID_VPCONFIGBOAFRAMEBROWSEFILESPATHBUTTON)

        self.workingDirectoryLabel = wx.StaticText(id=wx.ID_ANY,
              label='Working Directory', name='workingDirectoryLabel',
              parent=self.pathsPanel, pos=wx.Point(8, 89), size=wx.Size(140,
              17), style=0)

        self.workingDirText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMEWORKINGDIRTEXT,
              name='workingDirText', parent=self.pathsPanel, pos=wx.Point(156,
              89), size=wx.Size(439, 21), style=0, value='')
        self.workingDirText.SetToolTip('Path to where the Excel file will be created, or already exists.')

        self.browseWorkingDirButton = wx.Button(id=wxID_VPCONFIGBOAFRAMEBROWSEWORKINGDIRBUTTON,
              label='Browse...', name='browseWorkingDirButton',
              parent=self.pathsPanel, pos=wx.Point(603, 89), size=wx.Size(90,
              23), style=0)
        self.browseWorkingDirButton.Bind(wx.EVT_BUTTON,
              self.OnBrowseWorkingDirectoryButton,
              id=wxID_VPCONFIGBOAFRAMEBROWSEWORKINGDIRBUTTON)

        self.mapPathLabel = wx.StaticText(id=wx.ID_ANY, label='Map Path',
              name='mapPathLabel', parent=self.pathsPanel, pos=wx.Point(8, 120),
              size=wx.Size(140, 17), style=0)

        self.mapPathText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMEMAPPATHTEXT,
              name='mapPathText', parent=self.pathsPanel, pos=wx.Point(156,
              120), size=wx.Size(439, 21), style=0, value='')
        self.mapPathText.SetToolTip('Select the path to min_map.txt if not the default.')

        self.browseMapPathButton = wx.Button(id=wxID_VPCONFIGBOAFRAMEBROWSEMAPPATHBUTTON,
              label='Browse...', name='browseMapPathButton',
              parent=self.pathsPanel, pos=wx.Point(603, 120), size=wx.Size(90,
              23), style=0)
        self.browseMapPathButton.Bind(wx.EVT_BUTTON, self.OnBrowseMapPathButton,
              id=wxID_VPCONFIGBOAFRAMEBROWSEMAPPATHBUTTON)

        self.filesPanel = wx.Panel(id=wxID_VPCONFIGBOAFRAMEFILESPANEL,
              name='filesPanel', parent=self.configBook, pos=wx.Point(0, 0),
              size=wx.Size(731, 517), style=wx.TAB_TRAVERSAL)

        self.siblingsLabel = wx.StaticText(id=wx.ID_ANY,
              label='Siblings (comma-separated)', name='siblingsLabel',
              parent=self.filesPanel, pos=wx.Point(8, 8), size=wx.Size(187, 17),
              style=0)

        self.siblingsText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMESIBLINGSTEXT,
              name='siblingsText', parent=self.filesPanel, pos=wx.Point(8, 25),
              size=wx.Size(715, 21), style=0, value='')
        self.siblingsText.SetToolTip("Example: '****','****','****'")

        self.phasedFilesLabel = wx.StaticText(id=wx.ID_ANY,
              label='Phased Files  (comma-separated)', name='phasedFilesLabel',
              parent=self.filesPanel, pos=wx.Point(8, 54), size=wx.Size(187,
              17), style=0)

        self.phasedFilesText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMEPHASEDFILESTEXT,
              name='phasedFilesText', parent=self.filesPanel, pos=wx.Point(8,
              79), size=wx.Size(715, 21), style=0, value='')
        self.phasedFilesText.SetToolTip("Example: '****','****','****'")

        self.evilTwinsLabel = wx.StaticText(id=wx.ID_ANY,
              label='Evil Twins  (comma-separated)', name='evilTwinsLabel',
              parent=self.filesPanel, pos=wx.Point(8, 108), size=wx.Size(187,
              17), style=0)

        self.evilTwinsText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMEEVILTWINSTEXT,
              name='evilTwinsText', parent=self.filesPanel, pos=wx.Point(8,
              133), size=wx.Size(715, 21), style=0, value='')
        self.evilTwinsText.SetToolTip("Example: '****','****','****'")

        self.cousinsLabel = wx.StaticText(id=wx.ID_ANY,
              label='Cousins (comma-separated)', name='cousinsLabel',
              parent=self.filesPanel, pos=wx.Point(8, 162), size=wx.Size(187,
              17), style=0)

        self.cousinsText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMECOUSINSTEXT,
              name='cousinsText', parent=self.filesPanel, pos=wx.Point(8, 179),
              size=wx.Size(715, 21), style=0, value='')
        self.cousinsText.SetToolTip("Example: '****','****','****'")

        self.chromosomesLabel = wx.StaticText(id=wx.ID_ANY,
              label='Chromosomes (comma-separated, leave empty for all 23 chromosomes)',
              name='chromosomesLabel', parent=self.filesPanel, pos=wx.Point(8,
              208), size=wx.Size(300, 17), style=0)

        self.chromosomesText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMECHROMOSOMESTEXT,
              name='chromosomesText', parent=self.filesPanel, pos=wx.Point(8,
              225), size=wx.Size(715, 21), style=0, value='')
        self.chromosomesText.SetToolTip('If empty, all chromosomes will be analyzed.\\nOtherwise: 1,2,3')

        self.boolPanel = wx.Panel(id=wxID_VPCONFIGBOAFRAMEBOOLPANEL,
              name='boolPanel', parent=self.configBook, pos=wx.Point(0, 0),
              size=wx.Size(731, 517), style=wx.TAB_TRAVERSAL)

        self.showNoMatchesLabel = wx.StaticText(label='SHOW_NO_MATCHES',
              name='showNoMatchesLabel', parent=self.boolPanel, pos=wx.Point(13,
              15), size=wx.Size(118, 17), style=0)

        self.showNoMatchesCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMESHOWNOMATCHESCOMBO,
              name='showNoMatchesCombo', parent=self.boolPanel,
              pos=wx.Point(214, 13), size=wx.Size(100, 21),
              style=wx.CB_READONLY, value='True')

        self.chromTrueSizeLabel = wx.StaticText(label='CHROM_TRUE_SIZE',
              name='chromTrueSizeLabel', parent=self.boolPanel, pos=wx.Point(13,
              46), size=wx.Size(119, 17), style=0)

        self.chromTrueSizeCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMECHROMTRUESIZECOMBO,
              name='chromTrueSizeCombo', parent=self.boolPanel,
              pos=wx.Point(214, 44), size=wx.Size(100, 21),
              style=wx.CB_READONLY, value='True')

        self.linearChromLabel = wx.StaticText(label='LINEAR_CHROMOSOME',
              name='linearChromLabel', parent=self.boolPanel, pos=wx.Point(13,
              77), size=wx.Size(142, 17), style=0)

        self.linearChromCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMELINEARCHROMCOMBO, name='linearChromCombo',
              parent=self.boolPanel, pos=wx.Point(214, 75), size=wx.Size(100,
              21), style=wx.CB_READONLY, value='True')

        self.mergeFilesLabel = wx.StaticText(label='MERGE_FILES',
              name='mergeFilesLabel', parent=self.boolPanel, pos=wx.Point(13,
              108), size=wx.Size(85, 17), style=0)

        self.mergeFilesCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMEMERGEFILESCOMBO, name='mergeFilesCombo',
              parent=self.boolPanel, pos=wx.Point(214, 106), size=wx.Size(100,
              21), style=wx.CB_READONLY, value='True')

        self.autoRecPntsLabel = wx.StaticText(label='AUTO_REC_PNTS',
              name='autoRecPntsLabel', parent=self.boolPanel, pos=wx.Point(13,
              139), size=wx.Size(98, 17), style=0)

        self.autoRecPntsCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMEAUTORECPNTSCOMBO, name='autoRecPntsCombo',
              parent=self.boolPanel, pos=wx.Point(214, 137), size=wx.Size(100,
              21), style=wx.CB_READONLY, value='True')

        self.autoRpAssignLabel = wx.StaticText(label='AUTO_RP_ASSIGN',
              name='autoRpAssignLabel', parent=self.boolPanel, pos=wx.Point(13,
              170), size=wx.Size(103, 17), style=0)

        self.autoRpAssignCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMEAUTORPASSIGNCOMBO,
              name='autoRpAssignCombo', parent=self.boolPanel, pos=wx.Point(214,
              168), size=wx.Size(100, 21), style=wx.CB_READONLY, value='True')

        self.repairFilesLabel = wx.StaticText(label='REPAIR_FILES',
              name='repairFilesLabel', parent=self.boolPanel, pos=wx.Point(13,
              201), size=wx.Size(85, 17), style=0)

        self.repairFilesCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMEREPAIRFILESCOMBO, name='repairFilesCombo',
              parent=self.boolPanel, pos=wx.Point(214, 199), size=wx.Size(100,
              21), style=wx.CB_READONLY, value='True')

        self.firTablesLabel = wx.StaticText(label='FIR_TABLES',
              name='firTablesLabel', parent=self.boolPanel, pos=wx.Point(13,
              232), size=wx.Size(68, 17), style=0)

        self.firTablesCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMEFIRTABLESCOMBO, name='firTablesCombo',
              parent=self.boolPanel, pos=wx.Point(214, 230), size=wx.Size(100,
              21), style=wx.CB_READONLY, value='True')

        self.scaleOnLabel = wx.StaticText(label='SCALE_ON', name='scaleOnLabel',
              parent=self.boolPanel, pos=wx.Point(13, 263), size=wx.Size(63,
              17), style=0)

        self.scaleOnCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMESCALEONCOMBO, name='scaleOnCombo',
              parent=self.boolPanel, pos=wx.Point(214, 261), size=wx.Size(100,
              21), style=wx.CB_READONLY, value='True')

        self.showTimesLabel = wx.StaticText(label='SHOW_TIMES',
              name='showTimesLabel', parent=self.boolPanel, pos=wx.Point(13,
              294), size=wx.Size(79, 17), style=0)

        self.showTimesCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMESHOWTIMESCOMBO, name='showTimesCombo',
              parent=self.boolPanel, pos=wx.Point(214, 292), size=wx.Size(100,
              21), style=wx.CB_READONLY, value='True')

        self.showMatchPairProgressLabel = wx.StaticText(label='SHOW_MATCH_PAIR_PROGRESS',
              name='showMatchPairProgressLabel', parent=self.boolPanel,
              pos=wx.Point(13, 325), size=wx.Size(183, 17), style=0)

        self.showMatchPairProgressCombo = wx.ComboBox(choices=['True', 'False'],
              id=wxID_VPCONFIGBOAFRAMESHOWMATCHPAIRPROGRESSCOMBO,
              name='showMatchPairProgressCombo', parent=self.boolPanel,
              pos=wx.Point(214, 323), size=wx.Size(100, 21),
              style=wx.CB_READONLY, value='True')

        self.numericPanel = wx.Panel(id=wxID_VPCONFIGBOAFRAMENUMERICPANEL,
              name='numericPanel', parent=self.configBook, pos=wx.Point(0, 0),
              size=wx.Size(731, 517), style=wx.TAB_TRAVERSAL)

        self.resolutionLabel = wx.StaticText(label='RESOLUTION',
              name='resolutionLabel', parent=self.numericPanel, pos=wx.Point(13,
              15), size=wx.Size(76, 17), style=0)

        self.resolutionSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMERESOLUTIONSPIN,
              initial=1, max=1000, min=0, name='resolutionSpin',
              parent=self.numericPanel, pos=wx.Point(130, 13), size=wx.Size(100,
              21), style=wx.SP_ARROW_KEYS)

        self.arpToleranceLabel = wx.StaticText(label='ARP_TOLERANCE',
              name='arpToleranceLabel', parent=self.numericPanel,
              pos=wx.Point(13, 46), size=wx.Size(99, 17), style=0)

        self.arpToleranceSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEARPTOLERANCESPIN,
              initial=5, max=1000, min=0, name='arpToleranceSpin',
              parent=self.numericPanel, pos=wx.Point(130, 44), size=wx.Size(100,
              21), style=wx.SP_ARROW_KEYS)

        self.hirCutoffLabel = wx.StaticText(label='HIR_CUTOFF',
              name='hirCutoffLabel', parent=self.numericPanel, pos=wx.Point(13,
              77), size=wx.Size(73, 17), style=0)

        self.hirCutoffSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEHIRCUTOFFSPIN,
              initial=7, max=100000, min=0, name='hirCutoffSpin',
              parent=self.numericPanel, pos=wx.Point(130, 75), size=wx.Size(100,
              21), style=wx.SP_ARROW_KEYS)

        self.firCutoffLabel = wx.StaticText(label='FIR_CUTOFF',
              name='firCutoffLabel', parent=self.numericPanel, pos=wx.Point(13,
              108), size=wx.Size(70, 17), style=0)

        self.firCutoffSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEFIRCUTOFFSPIN,
              initial=1, max=100000, min=0, name='firCutoffSpin',
              parent=self.numericPanel, pos=wx.Point(130, 106),
              size=wx.Size(100, 21), style=wx.SP_ARROW_KEYS)

        self.xHirCutoffLabel = wx.StaticText(label='X_HIR_CUTOFF',
              name='xHirCutoffLabel', parent=self.numericPanel, pos=wx.Point(13,
              139), size=wx.Size(84, 17), style=0)

        self.xHirCutoffSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEXHIRCUTOFFSPIN,
              initial=15, max=100000, min=0, name='xHirCutoffSpin',
              parent=self.numericPanel, pos=wx.Point(130, 137),
              size=wx.Size(100, 21), style=wx.SP_ARROW_KEYS)

        self.xFirCutoffLabel = wx.StaticText(label='X_FIR_CUTOFF',
              name='xFirCutoffLabel', parent=self.numericPanel, pos=wx.Point(13,
              170), size=wx.Size(81, 17), style=0)

        self.xFirCutoffSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEXFIRCUTOFFSPIN,
              initial=15, max=100000, min=0, name='xFirCutoffSpin',
              parent=self.numericPanel, pos=wx.Point(130, 168),
              size=wx.Size(100, 21), style=wx.SP_ARROW_KEYS)

        self.hirSnpMinLabel = wx.StaticText(label='HIR_SNP_MIN',
              name='hirSnpMinLabel', parent=self.numericPanel, pos=wx.Point(13,
              201), size=wx.Size(77, 17), style=0)

        self.hirSnpMinSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEHIRSNPMINSPIN,
              initial=200, max=1000000, min=0, name='hirSnpMinSpin',
              parent=self.numericPanel, pos=wx.Point(130, 199),
              size=wx.Size(100, 21), style=wx.SP_ARROW_KEYS)

        self.firSnpMinLabel = wx.StaticText(label='FIR_SNP_MIN',
              name='firSnpMinLabel', parent=self.numericPanel, pos=wx.Point(13,
              232), size=wx.Size(74, 17), style=0)

        self.firSnpMinSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEFIRSNPMINSPIN,
              initial=75, max=1000000, min=0, name='firSnpMinSpin',
              parent=self.numericPanel, pos=wx.Point(130, 230),
              size=wx.Size(100, 21), style=wx.SP_ARROW_KEYS)

        self.mmDistLabel = wx.StaticText(label='MM_DIST', name='mmDistLabel',
              parent=self.numericPanel, pos=wx.Point(13, 263), size=wx.Size(54,
              17), style=0)

        self.mmDistSpin = wx.SpinCtrl(id=wxID_VPCONFIGBOAFRAMEMMDISTSPIN,
              initial=1000, max=1000000, min=0, name='mmDistSpin',
              parent=self.numericPanel, pos=wx.Point(130, 261),
              size=wx.Size(100, 21), style=wx.SP_ARROW_KEYS)

        self.scaleFactorLabel = wx.StaticText(label='SCALE_FACTOR',
              name='scaleFactorLabel', parent=self.numericPanel,
              pos=wx.Point(13, 294), size=wx.Size(89, 17), style=0)

        self.scaleFactorText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMESCALEFACTORTEXT,
              name='scaleFactorText', parent=self.numericPanel,
              pos=wx.Point(130, 292), size=wx.Size(120, 21), style=0,
              value='0.1355')

        self.excelFileNameLabel = wx.StaticText(label='EXCEL_FILE_NAME',
              name='excelFileNameLabel', parent=self.pathsPanel, pos=wx.Point(8,
              151), size=wx.Size(140, 17), style=0)

        self.excelFileNameText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMEEXCELFILENAMETEXT,
              name='excelFileNameText', parent=self.pathsPanel,
              pos=wx.Point(156, 149), size=wx.Size(439, 21), style=0, value='')
        self.excelFileNameText.SetToolTip('First part only: no ".xlsx"')

        self.programOutputLabel = wx.StaticText(id=wx.ID_ANY,
              label='Program output:', name='programOutputLabel',
              parent=self.pathsPanel, pos=wx.Point(8, 190), size=wx.Size(140,
              17), style=0)

        self.programOutputClearButton = wx.Button(id=wxID_VPCONFIGBOAFRAMEPROGRAMOUTPUTCLEARBUTTON,
              label='Clear Output', name='programOutputClearButton',
              parent=self.pathsPanel, pos=wx.Point(156, 186), size=wx.Size(75,
              21), style=0)
        self.programOutputClearButton.Bind(wx.EVT_BUTTON,
              self.OnClearProgramOutputButton,
              id=wxID_VPCONFIGBOAFRAMEPROGRAMOUTPUTCLEARBUTTON)

        self.programOutputText = wx.TextCtrl(id=wx.ID_ANY,
              name='programOutputText', parent=self.pathsPanel, pos=wx.Point(8,
              208), size=wx.Size(715, 260),
              style=wx.TE_MULTILINE | wx.TE_READONLY, value='')
        self.programOutputText.SetToolTip('Output of the main program will appear here after "Run" is clicked.')

        self.freezeColumnLabel = wx.StaticText(label='FREEZE_COLUMN',
              name='freezeColumnLabel', parent=self.boolPanel, pos=wx.Point(13,
              356), size=wx.Size(183, 17), style=0)

        self.freezeColumnText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMEFREEZECOLUMNTEXT,
              name='freezeColumnText', parent=self.boolPanel, pos=wx.Point(214,
              354), size=wx.Size(120, 21), style=0, value='A')

        self.noCallLabel = wx.StaticText(label='NO_CALL', name='noCallLabel',
              parent=self.boolPanel, pos=wx.Point(13, 387), size=wx.Size(183,
              17), style=0)

        self.noCallText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMENOCALLTEXT,
              name='noCallText', parent=self.boolPanel, pos=wx.Point(214, 385),
              size=wx.Size(120, 21), style=0, value='X')

        self.linuxFontLabel = wx.StaticText(label='LINUX_FONT_STRING',
              name='linuxFontLabel', parent=self.boolPanel, pos=wx.Point(13,
              418), size=wx.Size(183, 17), style=0)

        self.linuxFontText = wx.TextCtrl(id=wxID_VPCONFIGBOAFRAMELINUXFONTTEXT,
              name='linuxFontText', parent=self.boolPanel, pos=wx.Point(214,
              416), size=wx.Size(500, 21), style=0, value='')

        self.staticLine1 = wx.StaticLine(id=wxID_VPCONFIGBOAFRAMESTATICLINE1,
              name='staticLine1', parent=self, pos=wx.Point(0, 561),
              size=wx.Size(755, 2), style=0)

        self.loadButton = wx.Button(id=wxID_VPCONFIGBOAFRAMELOADBUTTON,
              label='Load Configuration', name='loadButton', parent=self,
              pos=wx.Point(8, 571), size=wx.Size(110, 23), style=0)
        self.loadButton.Bind(wx.EVT_BUTTON, self.OnLoadButton,
              id=wxID_VPCONFIGBOAFRAMELOADBUTTON)

        self.saveButton = wx.Button(id=wxID_VPCONFIGBOAFRAMESAVEBUTTON,
              label='Save Configuration', name='saveButton', parent=self,
              pos=wx.Point(126, 571), size=wx.Size(110, 23), style=0)
        self.saveButton.Bind(wx.EVT_BUTTON, self.OnSaveButton,
              id=wxID_VPCONFIGBOAFRAMESAVEBUTTON)

        self.resetButton = wx.Button(id=wxID_VPCONFIGBOAFRAMERESETBUTTON,
              label='Reload Defaults', name='resetButton', parent=self,
              pos=wx.Point(244, 571), size=wx.Size(110, 23), style=0)
        self.resetButton.Bind(wx.EVT_BUTTON, self.OnResetButton,
              id=wxID_VPCONFIGBOAFRAMERESETBUTTON)

        self.actionsSpacerPanel = wx.Panel(id=wxID_VPCONFIGBOAFRAMEACTIONSSPACERPANEL,
              name='actionsSpacerPanel', parent=self, pos=wx.Point(354, 571),
              size=wx.Size(165, 23), style=wx.NO_BORDER)

        self.runButton = wx.Button(id=wxID_VPCONFIGBOAFRAMERUNBUTTON,
              label='Run', name='runButton', parent=self, pos=wx.Point(519,
              571), size=wx.Size(110, 23), style=0)
        self.runButton.SetToolTip('Click "Save Configuration" button if modifications have been made!')
        self.runButton.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.runButton.Bind(wx.EVT_BUTTON, self.OnRunButton,
              id=wxID_VPCONFIGBOAFRAMERUNBUTTON)

        self.closeButton = wx.Button(id=wxID_VPCONFIGBOAFRAMECLOSEBUTTON,
              label='Close', name='closeButton', parent=self, pos=wx.Point(637,
              571), size=wx.Size(110, 23), style=0)
        self.closeButton.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnCloseButton,
              id=wxID_VPCONFIGBOAFRAMECLOSEBUTTON)

        self._init_coll_configBook_Pages(self.configBook)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        bg = self.GetBackgroundColour()
        self.actionsSpacerPanel.SetBackgroundColour(bg)
        self._base_title = self.GetTitle()
        self.config_path = self._resolve_startup_config_path()
        self.controls = self._build_controls_map()
        self.data_changed = False
        self._suppress_change_tracking = False
        self._bind_change_tracking()
        self._apply_tooltips()
        self._refresh_dirty_state_ui()
        self.Centre(wx.BOTH)
        self.LoadConfig()

    def _resolve_startup_config_path(self):
        local_config = os.path.join(os.getcwd(), 'VP_configV1.py')
        if os.path.exists(local_config):
            return local_config

        return os.path.join(os.path.dirname(__file__), 'VP_configV1.py')

    def _build_controls_map(self):
        return {
            'FILES_PATH': self.filesPathText,
            'WORKING_DIRECTORY': self.workingDirText,
            'MAP_PATH': self.mapPathText,
            'SIBLINGS': self.siblingsText,
            'PHASED_FILES': self.phasedFilesText,
            'EVIL_TWINS': self.evilTwinsText,
            'COUSINS': self.cousinsText,
            'CHROMOSOMES': self.chromosomesText,
            'EXCEL_FILE_NAME': self.excelFileNameText,
            'SHOW_NO_MATCHES': self.showNoMatchesCombo,
            'CHROM_TRUE_SIZE': self.chromTrueSizeCombo,
            'LINEAR_CHROMOSOME': self.linearChromCombo,
            'MERGE_FILES': self.mergeFilesCombo,
            'RESOLUTION': self.resolutionSpin,
            'AUTO_REC_PNTS': self.autoRecPntsCombo,
            'ARP_TOLERANCE': self.arpToleranceSpin,
            'AUTO_RP_ASSIGN': self.autoRpAssignCombo,
            'REPAIR_FILES': self.repairFilesCombo,
            'SCALE_FACTOR': self.scaleFactorText,
            'HIR_CUTOFF': self.hirCutoffSpin,
            'FIR_CUTOFF': self.firCutoffSpin,
            'X_HIR_CUTOFF': self.xHirCutoffSpin,
            'X_FIR_CUTOFF': self.xFirCutoffSpin,
            'FIR_TABLES': self.firTablesCombo,
            'SCALE_ON': self.scaleOnCombo,
            'FREEZE_COLUMN': self.freezeColumnText,
            'LINUX_FONT_STRING': self.linuxFontText,
            'SHOW_TIMES': self.showTimesCombo,
            'SHOW_MATCH_PAIR_PROGRESS': self.showMatchPairProgressCombo,
            'HIR_SNP_MIN': self.hirSnpMinSpin,
            'FIR_SNP_MIN': self.firSnpMinSpin,
            'MM_DIST': self.mmDistSpin,
            'NO_CALL': self.noCallText,
        }

    def _apply_tooltips(self):
        for var_name, ctrl in self.controls.items():
            tooltip = TOOLTIPS.get(var_name, '')
            if tooltip:
                ctrl.SetToolTip(tooltip)

    def _bind_change_tracking(self):
        for ctrl in self.controls.values():
            if isinstance(ctrl, wx.ComboBox):
                ctrl.Bind(wx.EVT_COMBOBOX, self._on_input_widget_changed)
            elif isinstance(ctrl, wx.SpinCtrl):
                ctrl.Bind(wx.EVT_SPINCTRL, self._on_input_widget_changed)
                ctrl.Bind(wx.EVT_TEXT, self._on_input_widget_changed)
            elif isinstance(ctrl, wx.TextCtrl):
                ctrl.Bind(wx.EVT_TEXT, self._on_input_widget_changed)

    def _on_input_widget_changed(self, event):
        if not self._suppress_change_tracking:
            self.data_changed = True
            self._refresh_dirty_state_ui()
        event.Skip()

    def _refresh_dirty_state_ui(self):
        title = self._base_title + (' *' if self.data_changed else '')
        self.SetTitle(title)
        self.runButton.Enable(not self.data_changed)
        if self.data_changed:
            self.statusBar.SetStatusText('Input data has changed, save config before running!', 0)

    def _set_status(self, message):
        self.statusBar.SetStatusText(message, 0)

    def _choose_directory(self, title, control):
        dialog = wx.DirDialog(self, title)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                control.SetValue(dialog.GetPath())
        finally:
            dialog.Destroy()

    def _strip_wrapping_quotes(self, item):
        cleaned = item.strip()
        while len(cleaned) >= 2 and (
              (cleaned[0] == '"' and cleaned[-1] == '"') or
              (cleaned[0] == "'" and cleaned[-1] == "'")
        ):
              cleaned = cleaned[1:-1].strip()
        return cleaned

    def _split_comma_list(self, value):
        result = []
        for item in value.replace('\n', ',').split(','):
              cleaned = self._strip_wrapping_quotes(item)
              if cleaned:
                    result.append(cleaned)
        return result

    def _split_line_list(self, value):
        # Accept either one-item-per-line or comma-separated input (or a mix).
        normalized = value.replace('\r', '\n').replace(',', '\n')
        result = []
        for line in normalized.splitlines():
              cleaned = self._strip_wrapping_quotes(line)
              if cleaned:
                    result.append(cleaned)
        return result

    def _parse_chromosomes(self, value):
        chrom_tokens = self._split_comma_list(value)
        chromosomes = []
        for token in chrom_tokens:
            try:
                chrom = int(token)
            except ValueError:
                raise ValueError('CHROMOSOMES must be comma-separated integers (for example: 1,2,3).')

            if chrom < 1 or chrom > 23:
                raise ValueError('CHROMOSOMES values must be between 1 and 23. Invalid value: %s' % chrom)

            chromosomes.append(chrom)
        return chromosomes

    def _format_value(self, var_name, value):
        if var_name in RAW_STRING_FIELDS:
            return repr(str(value))
        if var_name in LIST_FIELDS or var_name in LINE_LIST_FIELDS:
            return repr(list(value))
        if var_name in BOOLEAN_FIELDS:
            return 'True' if value else 'False'
        if var_name in INTEGER_FIELDS:
            return str(int(value))
        if var_name in FLOAT_FIELDS:
            return str(float(value))
        return repr(str(value))

    def _collect_control_value(self, var_name, control):
        if var_name in LIST_FIELDS:
            if var_name == 'CHROMOSOMES':
                return self._parse_chromosomes(control.GetValue())
            return self._split_comma_list(control.GetValue())
        if var_name in LINE_LIST_FIELDS:
            return self._split_line_list(control.GetValue())
        if var_name in BOOLEAN_FIELDS:
            return control.GetValue() == 'True'
        if var_name in INTEGER_FIELDS:
            return control.GetValue()
        if var_name in FLOAT_FIELDS:
            return float(control.GetValue())
        return control.GetValue()

    def _populate_control(self, var_name, control, value):
        if var_name in LIST_FIELDS:
            control.SetValue(', '.join(str(item) for item in value))
        elif var_name in LINE_LIST_FIELDS:
            control.SetValue('\n'.join(str(item) for item in value))
        elif var_name in BOOLEAN_FIELDS:
            control.SetValue('True' if value else 'False')
        elif var_name in INTEGER_FIELDS:
            control.SetValue(int(value))
        else:
            control.SetValue(str(value))

    def _update_config_lines(self, lines):
        updated_lines = []
        pattern = re.compile(r'^([A-Z_]+)\s*=')
        for line in lines:
            match = pattern.match(line)
            if not match:
                updated_lines.append(line)
                continue

            var_name = match.group(1)
            control = self.controls.get(var_name)
            if control is None:
                updated_lines.append(line)
                continue

            value = self._collect_control_value(var_name, control)
            updated_lines.append('%s = %s\n' % (var_name, self._format_value(var_name, value)))
        return updated_lines

    def LoadConfig(self):
        try:
            if not os.path.exists(self.config_path):
                self._set_status('No configuration file found')
                self.data_changed = False
                self._refresh_dirty_state_ui()
                return

            local_dict = {}
            with open(self.config_path, 'r') as config_file:
                exec(config_file.read(), {}, local_dict)

            self._suppress_change_tracking = True
            for var_name, control in self.controls.items():
                if var_name in local_dict:
                    self._populate_control(var_name, control, local_dict[var_name])
            self._suppress_change_tracking = False
            self.data_changed = False
            self._refresh_dirty_state_ui()

            self._set_status('Configuration loaded successfully')
        except Exception as error:
            self._suppress_change_tracking = False
            self._set_status('Error loading configuration: %s' % error)

    def SaveConfig(self):
        try:
            with open(self.config_path, 'r') as config_file:
                lines = config_file.readlines()

            updated_lines = self._update_config_lines(lines)

            with open(self.config_path, 'w') as config_file:
                config_file.writelines(updated_lines)

            self.data_changed = False
            self._refresh_dirty_state_ui()
            self._set_status('Configuration saved')
            wx.MessageBox('Configuration saved successfully.', 'Success',
                  wx.OK | wx.ICON_INFORMATION)
            return True
        except Exception as error:
            wx.MessageBox('Error saving configuration: %s' % error, 'Error',
                  wx.OK | wx.ICON_ERROR)
            return False

    def OnBrowseFilesPathButton(self, event):
        self._choose_directory('Select DNA files folder', self.filesPathText)

    def OnBrowseWorkingDirectoryButton(self, event):
        self._choose_directory('Select working directory', self.workingDirText)

    def OnBrowseMapPathButton(self, event):
        self._choose_directory('Select folder containing min_map.txt', self.mapPathText)

    def OnLoadConfigMenu(self, event):
        self.OnLoadButton(event)

    def OnSaveConfigMenu(self, event):
        self.OnSaveButton(event)

    def OnExitMenu(self, event):
      self.Close()

    def OnAboutMenu(self, event):
        dialog = wx.MessageDialog(self,
              'Visual Phaser Config Editor',
              'About VP Config GUI', wx.OK | wx.ICON_INFORMATION)
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()

    def OnLoadButton(self, event):
        dialog = wx.FileDialog(self, 'Load Configuration File',
              wildcard='Python files (*.py)|*.py',
              style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.config_path = dialog.GetPath()
                self.LoadConfig()
        finally:
            dialog.Destroy()

    def OnSaveButton(self, event):
        default_dir = os.path.dirname(self.config_path) if self.config_path else os.getcwd()
        default_file = os.path.basename(self.config_path) if self.config_path else 'VP_configV1.py'
        dialog = wx.FileDialog(
            self,
            'Save Configuration File',
            defaultDir=default_dir,
            defaultFile=default_file,
            wildcard='Python files (*.py)|*.py',
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.config_path = dialog.GetPath()
                self.SaveConfig()
        finally:
            dialog.Destroy()

    def OnResetButton(self, event):
        try:
            self._suppress_change_tracking = True

            # Preserve requested behavior for Paths/Input tabs.
            for panel in (self.pathsPanel, self.filesPanel):
                for child in panel.GetChildren():
                        if isinstance(child, wx.TextCtrl):
                            child.SetValue('')

            # Reload defaults for controls outside Paths/Input tabs.
            for var_name, control in self.controls.items():
                if control.GetParent() in (self.pathsPanel, self.filesPanel):
                        continue

                field_definition = FIELD_DEFINITIONS.get(var_name, {})
                if 'default' in field_definition:
                        self._populate_control(var_name, control, field_definition['default'])

            self.data_changed = True
            self._refresh_dirty_state_ui()
            self._set_status('Defaults reloaded for Generation Options and Algorithm Factors; Paths/Input text fields cleared')
            self.filesPathText.SetFocus()
        except Exception as error:
            self._set_status('Error resetting defaults: %s' % error)
        finally:
            self._suppress_change_tracking = False

    def OnClearProgramOutputButton(self, event):
        self.programOutputText.SetValue('')

    def OnCloseButton(self, event):
        self.Close()

    def OnWindowClose(self, event):
        if self.data_changed:
            dialog = wx.MessageDialog(
                  self,
                  'You have unsaved changes. Close without saving?',
                  'Unsaved Changes',
                  wx.YES_NO | wx.CANCEL | wx.ICON_WARNING)
            try:
                result = dialog.ShowModal()
            finally:
                dialog.Destroy()

            if result != wx.ID_YES:
                event.Veto()
                return
        event.Skip()

    def _stream_process_output(self, process, script_name):
        try:
            for line in iter(process.stdout.readline, ''):
                wx.CallAfter(self.programOutputText.AppendText, line)
            process.stdout.close()
            return_code = process.wait()
            wx.CallAfter(self._set_status,
                  'Finished %s (exit code %s)' % (script_name, return_code))
        except Exception as error:
            wx.CallAfter(self.programOutputText.AppendText,
                  '\n[Output stream error] %s\n' % error)
            wx.CallAfter(self._set_status, 'Run failed: %s' % error)

    def OnRunButton(self, event):
        if self.data_changed:
            self._set_status('Run disabled: save configuration changes first')
            return
        self.configBook.SetSelection(0)
        script_dir = os.path.dirname(__file__)
        pattern = os.path.join(script_dir, 'Visual_Phaser.V*.py')
        candidates = sorted(glob.glob(pattern))
        if not candidates:
            wx.MessageBox('Could not find Visual_Phaser.V*.py in %s' % script_dir,
                  'Run Error', wx.OK | wx.ICON_ERROR)
            self._set_status('Run failed: Visual_Phaser.V*.py not found')
            return

        target_script = candidates[-1]
        running_process = getattr(self, '_run_process', None)
        if running_process and running_process.poll() is None:
            wx.MessageBox('A Visual Phaser run is already in progress.',
                  'Run In Progress', wx.OK | wx.ICON_INFORMATION)
            return

        try:
            self.programOutputText.SetValue('')
            self.programOutputText.AppendText('Starting %s...\n\n' %
                  os.path.basename(target_script))
            self._run_process = subprocess.Popen(
                  [sys.executable, target_script],
                  cwd=script_dir,
                  stdin=subprocess.DEVNULL,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.STDOUT,
                  text=True,
                  bufsize=1)
            output_thread = threading.Thread(target=self._stream_process_output,
                  args=(self._run_process, os.path.basename(target_script)),
                  daemon=True)
            output_thread.start()
            self._set_status('Running %s' % os.path.basename(target_script))
        except Exception as error:
            wx.MessageBox('Error launching script: %s' % error,
                  'Run Error', wx.OK | wx.ICON_ERROR)
            self._set_status('Run failed: %s' % error)


class VPConfigBoaApp(wx.App):
    def OnInit(self):
        self.frame = VPConfigBoaFrame(None)
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        if os.path.exists(config_path):
          frame.config_path = config_path
          frame.LoadConfig()
    frame.Show(True)
    app.MainLoop()
