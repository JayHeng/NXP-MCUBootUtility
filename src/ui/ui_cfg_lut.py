#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
import os
import array
import struct
import shutil
import uidef
import uivar
import uilang
import uidef_fdcb
sys.path.append(os.path.abspath(".."))
from win import bootDeviceWin_LUT
from mem import memdef

kAccessType_Set = 0
kAccessType_Get = 1

kLutGroup_Members = 16

class secBootUiCfgLut(bootDeviceWin_LUT.bootDeviceWin_LUT):

    def __init__(self, parent):
        bootDeviceWin_LUT.bootDeviceWin_LUT.__init__(self, parent)
        self.cfgFdcbBinFilename = None
        self.fdcbBuffer = array.array('c', [chr(0x00)]) * memdef.kMemBlockSize_FDCB
        self.lutGroup = 0

    def setNecessaryInfo( self, cfgFdcbBinFilename ):
        self.cfgFdcbBinFilename = cfgFdcbBinFilename
        if os.path.isfile(self.cfgFdcbBinFilename):
            with open(self.cfgFdcbBinFilename, 'rb+') as fileObj:
                fdcbBytes = fileObj.read()
                for i in range(memdef.kMemBlockSize_FDCB):
                    self.fdcbBuffer[i] = fdcbBytes[i]
                fileObj.close()
            self._recoverLastSettings()

    def _convertPackFmt( self, byteNum ):
        fmt = '<B'
        if byteNum == 4:
            fmt = '<I'
        elif byteNum == 2:
            fmt = '<H'
        #elif byteNum == 1:
        else:
            pass
        return fmt

    def _getMemberFromFdcb( self, buf, offset, byteNum ):
        return struct.unpack_from(self._convertPackFmt(byteNum), buf[offset:offset+byteNum], 0)

    def _setMemberForFdcb( self, offset, byteNum, data ):
        struct.pack_into(self._convertPackFmt(byteNum), self.fdcbBuffer, offset, data)

    def _getLookupTableItem( self, index ):
        lookupTable = self._getMemberFromFdcb(self.fdcbBuffer, uidef_fdcb.kFlexspiFdcbOffset_lookupTable + index * 4, 4)
        op0 = (lookupTable[0] & uidef_fdcb.kFlexspiLutRegMask_Op0) >> uidef_fdcb.kFlexspiLutRegShift_Op0
        pad0 = (lookupTable[0] & uidef_fdcb.kFlexspiLutRegMask_Pad0) >> uidef_fdcb.kFlexspiLutRegShift_Pad0
        cmd0 = int(((lookupTable[0] & uidef_fdcb.kFlexspiLutRegMask_Cmd0) >> uidef_fdcb.kFlexspiLutRegShift_Cmd0))
        op1 = (lookupTable[0] & uidef_fdcb.kFlexspiLutRegMask_Op1) >> uidef_fdcb.kFlexspiLutRegShift_Op1
        pad1 = (lookupTable[0] & uidef_fdcb.kFlexspiLutRegMask_Pad1) >> uidef_fdcb.kFlexspiLutRegShift_Pad1
        cmd1 = int((lookupTable[0] & uidef_fdcb.kFlexspiLutRegMask_Cmd1) >> uidef_fdcb.kFlexspiLutRegShift_Cmd1)
        return (op0, pad0, cmd0, op1, pad1, cmd1)

    def _findMatchedOpSelection( self, choiceObj, op ):
        count = choiceObj.GetCount()
        for i in range(count):
            content = choiceObj.GetString(i)
            value = int(content[0:4], 16)
            if value == op:
                return i
        return 0

    def _setLookupTableItem( self, index, op0, pad0, cmd0, op1, pad1, cmd1 ):
        lookupTable = 0
        lookupTable = lookupTable | (op0 << uidef_fdcb.kFlexspiLutRegShift_Op0)
        lookupTable = lookupTable | (pad0 << uidef_fdcb.kFlexspiLutRegShift_Pad0)
        lookupTable = lookupTable | (cmd0 << uidef_fdcb.kFlexspiLutRegShift_Cmd0)
        lookupTable = lookupTable | (op1 << uidef_fdcb.kFlexspiLutRegShift_Op1)
        lookupTable = lookupTable | (pad1 << uidef_fdcb.kFlexspiLutRegShift_Pad1)
        lookupTable = lookupTable | (cmd1 << uidef_fdcb.kFlexspiLutRegShift_Cmd1)
        self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lookupTable + index * 4, 4, lookupTable)

    def _accessLut16n( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members)
            self.m_choice_cmd0_16n.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n, cmd0))
            self.m_choice_pad0_16n.SetSelection(pad0)
            self.m_textCtrl_op0_16n.Clear()
            self.m_textCtrl_op0_16n.write(str(hex(op0)))
            self.m_choice_cmd1_16n.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n, cmd1))
            self.m_choice_pad1_16n.SetSelection(pad1)
            self.m_textCtrl_op1_16n.Clear()
            self.m_textCtrl_op1_16n.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n.GetString(self.m_choice_cmd0_16n.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n.GetSelection()
            op0= int(self.m_textCtrl_op0_16n.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n.GetString(self.m_choice_cmd1_16n.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n1( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 1)
            self.m_choice_cmd0_16n1.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n1, cmd0))
            self.m_choice_pad0_16n1.SetSelection(pad0)
            self.m_textCtrl_op0_16n1.Clear()
            self.m_textCtrl_op0_16n1.write(str(hex(op0)))
            self.m_choice_cmd1_16n1.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n1, cmd1))
            self.m_choice_pad1_16n1.SetSelection(pad1)
            self.m_textCtrl_op1_16n1.Clear()
            self.m_textCtrl_op1_16n1.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n1.GetString(self.m_choice_cmd0_16n1.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n1.GetSelection()
            op0= int(self.m_textCtrl_op0_16n1.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n1.GetString(self.m_choice_cmd1_16n1.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n1.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n1.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 1, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n2( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 2)
            self.m_choice_cmd0_16n2.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n2, cmd0))
            self.m_choice_pad0_16n2.SetSelection(pad0)
            self.m_textCtrl_op0_16n2.Clear()
            self.m_textCtrl_op0_16n2.write(str(hex(op0)))
            self.m_choice_cmd1_16n2.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n2, cmd1))
            self.m_choice_pad1_16n2.SetSelection(pad1)
            self.m_textCtrl_op1_16n2.Clear()
            self.m_textCtrl_op1_16n2.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n2.GetString(self.m_choice_cmd0_16n2.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n2.GetSelection()
            op0= int(self.m_textCtrl_op0_16n2.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n2.GetString(self.m_choice_cmd1_16n2.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n2.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n2.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 2, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n3( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 3)
            self.m_choice_cmd0_16n3.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n3, cmd0))
            self.m_choice_pad0_16n3.SetSelection(pad0)
            self.m_textCtrl_op0_16n3.Clear()
            self.m_textCtrl_op0_16n3.write(str(hex(op0)))
            self.m_choice_cmd1_16n3.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n3, cmd1))
            self.m_choice_pad1_16n3.SetSelection(pad1)
            self.m_textCtrl_op1_16n3.Clear()
            self.m_textCtrl_op1_16n3.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n3.GetString(self.m_choice_cmd0_16n3.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n3.GetSelection()
            op0= int(self.m_textCtrl_op0_16n3.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n3.GetString(self.m_choice_cmd1_16n3.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n3.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n3.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 3, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n4( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 4)
            self.m_choice_cmd0_16n4.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n4, cmd0))
            self.m_choice_pad0_16n4.SetSelection(pad0)
            self.m_textCtrl_op0_16n4.Clear()
            self.m_textCtrl_op0_16n4.write(str(hex(op0)))
            self.m_choice_cmd1_16n4.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n4, cmd1))
            self.m_choice_pad1_16n4.SetSelection(pad1)
            self.m_textCtrl_op1_16n4.Clear()
            self.m_textCtrl_op1_16n4.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n4.GetString(self.m_choice_cmd0_16n4.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n4.GetSelection()
            op0= int(self.m_textCtrl_op0_16n4.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n4.GetString(self.m_choice_cmd1_16n4.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n4.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n4.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 4, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n5( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 5)
            self.m_choice_cmd0_16n5.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n5, cmd0))
            self.m_choice_pad0_16n5.SetSelection(pad0)
            self.m_textCtrl_op0_16n5.Clear()
            self.m_textCtrl_op0_16n5.write(str(hex(op0)))
            self.m_choice_cmd1_16n5.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n5, cmd1))
            self.m_choice_pad1_16n5.SetSelection(pad1)
            self.m_textCtrl_op1_16n5.Clear()
            self.m_textCtrl_op1_16n5.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n5.GetString(self.m_choice_cmd0_16n5.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n5.GetSelection()
            op0= int(self.m_textCtrl_op0_16n5.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n5.GetString(self.m_choice_cmd1_16n5.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n5.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n5.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 5, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n6( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 6)
            self.m_choice_cmd0_16n6.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n6, cmd0))
            self.m_choice_pad0_16n6.SetSelection(pad0)
            self.m_textCtrl_op0_16n6.Clear()
            self.m_textCtrl_op0_16n6.write(str(hex(op0)))
            self.m_choice_cmd1_16n6.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n6, cmd1))
            self.m_choice_pad1_16n6.SetSelection(pad1)
            self.m_textCtrl_op1_16n6.Clear()
            self.m_textCtrl_op1_16n6.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n6.GetString(self.m_choice_cmd0_16n6.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n6.GetSelection()
            op0= int(self.m_textCtrl_op0_16n6.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n6.GetString(self.m_choice_cmd1_16n6.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n6.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n6.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 6, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n7( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 7)
            self.m_choice_cmd0_16n7.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n7, cmd0))
            self.m_choice_pad0_16n7.SetSelection(pad0)
            self.m_textCtrl_op0_16n7.Clear()
            self.m_textCtrl_op0_16n7.write(str(hex(op0)))
            self.m_choice_cmd1_16n7.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n7, cmd1))
            self.m_choice_pad1_16n7.SetSelection(pad1)
            self.m_textCtrl_op1_16n7.Clear()
            self.m_textCtrl_op1_16n7.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n7.GetString(self.m_choice_cmd0_16n7.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n7.GetSelection()
            op0= int(self.m_textCtrl_op0_16n7.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n7.GetString(self.m_choice_cmd1_16n7.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n7.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n7.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 7, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n8( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 8)
            self.m_choice_cmd0_16n8.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n8, cmd0))
            self.m_choice_pad0_16n8.SetSelection(pad0)
            self.m_textCtrl_op0_16n8.Clear()
            self.m_textCtrl_op0_16n8.write(str(hex(op0)))
            self.m_choice_cmd1_16n8.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n8, cmd1))
            self.m_choice_pad1_16n8.SetSelection(pad1)
            self.m_textCtrl_op1_16n8.Clear()
            self.m_textCtrl_op1_16n8.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n8.GetString(self.m_choice_cmd0_16n8.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n8.GetSelection()
            op0= int(self.m_textCtrl_op0_16n8.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n8.GetString(self.m_choice_cmd1_16n8.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n8.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n8.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 8, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n9( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 9)
            self.m_choice_cmd0_16n9.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n9, cmd0))
            self.m_choice_pad0_16n9.SetSelection(pad0)
            self.m_textCtrl_op0_16n9.Clear()
            self.m_textCtrl_op0_16n9.write(str(hex(op0)))
            self.m_choice_cmd1_16n9.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n9, cmd1))
            self.m_choice_pad1_16n9.SetSelection(pad1)
            self.m_textCtrl_op1_16n9.Clear()
            self.m_textCtrl_op1_16n9.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n9.GetString(self.m_choice_cmd0_16n9.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n9.GetSelection()
            op0= int(self.m_textCtrl_op0_16n9.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n9.GetString(self.m_choice_cmd1_16n9.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n9.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n9.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 9, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n10( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 10)
            self.m_choice_cmd0_16n10.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n10, cmd0))
            self.m_choice_pad0_16n10.SetSelection(pad0)
            self.m_textCtrl_op0_16n10.Clear()
            self.m_textCtrl_op0_16n10.write(str(hex(op0)))
            self.m_choice_cmd1_16n10.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n10, cmd1))
            self.m_choice_pad1_16n10.SetSelection(pad1)
            self.m_textCtrl_op1_16n10.Clear()
            self.m_textCtrl_op1_16n10.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n10.GetString(self.m_choice_cmd0_16n10.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n10.GetSelection()
            op0= int(self.m_textCtrl_op0_16n10.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n10.GetString(self.m_choice_cmd1_16n10.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n10.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n10.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 10, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n11( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 11)
            self.m_choice_cmd0_16n11.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n11, cmd0))
            self.m_choice_pad0_16n11.SetSelection(pad0)
            self.m_textCtrl_op0_16n11.Clear()
            self.m_textCtrl_op0_16n11.write(str(hex(op0)))
            self.m_choice_cmd1_16n11.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n11, cmd1))
            self.m_choice_pad1_16n11.SetSelection(pad1)
            self.m_textCtrl_op1_16n11.Clear()
            self.m_textCtrl_op1_16n11.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n11.GetString(self.m_choice_cmd0_16n11.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n11.GetSelection()
            op0= int(self.m_textCtrl_op0_16n11.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n11.GetString(self.m_choice_cmd1_16n11.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n11.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n11.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 11, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n12( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 12)
            self.m_choice_cmd0_16n12.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n12, cmd0))
            self.m_choice_pad0_16n12.SetSelection(pad0)
            self.m_textCtrl_op0_16n12.Clear()
            self.m_textCtrl_op0_16n12.write(str(hex(op0)))
            self.m_choice_cmd1_16n12.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n12, cmd1))
            self.m_choice_pad1_16n12.SetSelection(pad1)
            self.m_textCtrl_op1_16n12.Clear()
            self.m_textCtrl_op1_16n12.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n12.GetString(self.m_choice_cmd0_16n12.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n12.GetSelection()
            op0= int(self.m_textCtrl_op0_16n12.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n12.GetString(self.m_choice_cmd1_16n12.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n12.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n12.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 12, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n13( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 13)
            self.m_choice_cmd0_16n13.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n13, cmd0))
            self.m_choice_pad0_16n13.SetSelection(pad0)
            self.m_textCtrl_op0_16n13.Clear()
            self.m_textCtrl_op0_16n13.write(str(hex(op0)))
            self.m_choice_cmd1_16n13.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n13, cmd1))
            self.m_choice_pad1_16n13.SetSelection(pad1)
            self.m_textCtrl_op1_16n13.Clear()
            self.m_textCtrl_op1_16n13.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n13.GetString(self.m_choice_cmd0_16n13.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n13.GetSelection()
            op0= int(self.m_textCtrl_op0_16n13.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n13.GetString(self.m_choice_cmd1_16n13.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n13.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n13.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 13, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n14( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 14)
            self.m_choice_cmd0_16n14.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n14, cmd0))
            self.m_choice_pad0_16n14.SetSelection(pad0)
            self.m_textCtrl_op0_16n14.Clear()
            self.m_textCtrl_op0_16n14.write(str(hex(op0)))
            self.m_choice_cmd1_16n14.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n14, cmd1))
            self.m_choice_pad1_16n14.SetSelection(pad1)
            self.m_textCtrl_op1_16n14.Clear()
            self.m_textCtrl_op1_16n14.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n14.GetString(self.m_choice_cmd0_16n14.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n14.GetSelection()
            op0= int(self.m_textCtrl_op0_16n14.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n14.GetString(self.m_choice_cmd1_16n14.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n14.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n14.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 14, op0, pad0, cmd0, op1, pad1, cmd1)

    def _accessLut16n15( self, accessType=kAccessType_Get):
        if accessType == kAccessType_Set:
            op0, pad0, cmd0, op1, pad1, cmd1 = self._getLookupTableItem(self.lutGroup * kLutGroup_Members + 15)
            self.m_choice_cmd0_16n15.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd0_16n15, cmd0))
            self.m_choice_pad0_16n15.SetSelection(pad0)
            self.m_textCtrl_op0_16n15.Clear()
            self.m_textCtrl_op0_16n15.write(str(hex(op0)))
            self.m_choice_cmd1_16n15.SetSelection(self._findMatchedOpSelection(self.m_choice_cmd1_16n15, cmd1))
            self.m_choice_pad1_16n15.SetSelection(pad1)
            self.m_textCtrl_op1_16n15.Clear()
            self.m_textCtrl_op1_16n15.write(str(hex(op1)))
        else:
            content = self.m_choice_cmd0_16n15.GetString(self.m_choice_cmd0_16n15.GetSelection())
            cmd0 = int(content[0:4], 16)
            pad0 = self.m_choice_pad0_16n15.GetSelection()
            op0= int(self.m_textCtrl_op0_16n15.GetLineText(0), 16)
            content = self.m_choice_cmd1_16n15.GetString(self.m_choice_cmd1_16n15.GetSelection())
            cmd1 = int(content[0:4], 16)
            pad1 = self.m_choice_pad1_16n15.GetSelection()
            op1 = int(self.m_textCtrl_op1_16n15.GetLineText(0), 16)
            self._setLookupTableItem(self.lutGroup * kLutGroup_Members + 15, op0, pad0, cmd0, op1, pad1, cmd1)

    def _recoverLastSettings ( self ):
        self._accessLut16n(kAccessType_Set)
        self._accessLut16n1(kAccessType_Set)
        self._accessLut16n2(kAccessType_Set)
        self._accessLut16n3(kAccessType_Set)
        self._accessLut16n4(kAccessType_Set)
        self._accessLut16n5(kAccessType_Set)
        self._accessLut16n6(kAccessType_Set)
        self._accessLut16n7(kAccessType_Set)
        self._accessLut16n8(kAccessType_Set)
        self._accessLut16n9(kAccessType_Set)
        self._accessLut16n10(kAccessType_Set)
        self._accessLut16n11(kAccessType_Set)
        self._accessLut16n12(kAccessType_Set)
        self._accessLut16n13(kAccessType_Set)
        self._accessLut16n14(kAccessType_Set)
        self._accessLut16n15(kAccessType_Set)

    def _getLutx16( self ):
        self._accessLut16n(kAccessType_Get)
        self._accessLut16n1(kAccessType_Get)
        self._accessLut16n2(kAccessType_Get)
        self._accessLut16n3(kAccessType_Get)
        self._accessLut16n4(kAccessType_Get)
        self._accessLut16n5(kAccessType_Get)
        self._accessLut16n6(kAccessType_Get)
        self._accessLut16n7(kAccessType_Get)
        self._accessLut16n8(kAccessType_Get)
        self._accessLut16n9(kAccessType_Get)
        self._accessLut16n10(kAccessType_Get)
        self._accessLut16n11(kAccessType_Get)
        self._accessLut16n12(kAccessType_Get)
        self._accessLut16n13(kAccessType_Get)
        self._accessLut16n14(kAccessType_Get)
        self._accessLut16n15(kAccessType_Get)

    def callbackSetLutGroup( self, event ):
        self._getLutx16()
        self.lutGroup = self.m_choice_lutGroup.GetSelection()
        self.m_staticText_lutIndex16n.SetLabel(str(self.lutGroup * kLutGroup_Members))
        self.m_staticText_lutIndex16n1.SetLabel(str(self.lutGroup * kLutGroup_Members + 1))
        self.m_staticText_lutIndex16n2.SetLabel(str(self.lutGroup * kLutGroup_Members + 2))
        self.m_staticText_lutIndex16n3.SetLabel(str(self.lutGroup * kLutGroup_Members + 3))
        self.m_staticText_lutIndex16n4.SetLabel(str(self.lutGroup * kLutGroup_Members + 4))
        self.m_staticText_lutIndex16n5.SetLabel(str(self.lutGroup * kLutGroup_Members + 5))
        self.m_staticText_lutIndex16n6.SetLabel(str(self.lutGroup * kLutGroup_Members + 6))
        self.m_staticText_lutIndex16n7.SetLabel(str(self.lutGroup * kLutGroup_Members + 7))
        self.m_staticText_lutIndex16n8.SetLabel(str(self.lutGroup * kLutGroup_Members + 8))
        self.m_staticText_lutIndex16n9.SetLabel(str(self.lutGroup * kLutGroup_Members + 9))
        self.m_staticText_lutIndex16n10.SetLabel(str(self.lutGroup * kLutGroup_Members + 10))
        self.m_staticText_lutIndex16n11.SetLabel(str(self.lutGroup * kLutGroup_Members + 11))
        self.m_staticText_lutIndex16n12.SetLabel(str(self.lutGroup * kLutGroup_Members + 12))
        self.m_staticText_lutIndex16n13.SetLabel(str(self.lutGroup * kLutGroup_Members + 13))
        self.m_staticText_lutIndex16n14.SetLabel(str(self.lutGroup * kLutGroup_Members + 14))
        self.m_staticText_lutIndex16n15.SetLabel(str(self.lutGroup * kLutGroup_Members + 15))
        self._recoverLastSettings()

    def callbackOk( self, event ):
        self._getLutx16()
        with open(self.cfgFdcbBinFilename, 'wb') as fileObj:
            fileObj.write(self.fdcbBuffer)
            fileObj.close()
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)

    def callbackClose( self, event ):
        self.Show(False)

