#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import hashlib
sys.path.append(os.path.abspath(".."))
from gen import RTyyyy_gendef
from mem import RTyyyy_memdef

# Container header 
kCntHdr_Tag            = 0x87
kCntHdr_Version        = 0x00
kCntHdr_FuseVersion    = 0x00
kCntHdr_SwVersion      = 0x0000
kCntHdr_Flags          = 0x00000000 # Container not authenticated

kHashType_Sha256         = 0x0
kHashType_Sha384         = 0x1
kHashType_Sha512         = 0x2
kImgEntry_Flags          = 0x00000113 # Non-encrypted, SHA384, CM33, Executable

kSignBlock_Tag         = 0x90
kSignBlock_Version     = 0x00

kContainerBlockSize_CntHdr      = 0x0010
kContainerBlockSize_ImgEntry    = 0x0080
kContainerBlockSize_SignBlock   = 0x0010

class cntHdrStruct(object):

    def __init__( self, parent=None):
        #super(cntHdrStruct, self).__init__(parent)
        self.version = kCntHdr_Version
        self.length = None
        self.tag = kCntHdr_Tag
        self.flags = kCntHdr_Flags
        self.sw_ver = kCntHdr_SwVersion
        self.fuse_ver = kCntHdr_FuseVersion
        self.num_images = None
        self.sign_blk_offset = None
        self.reserved1 = 0x0000

    def set_members( self, num_images=1 ):
        self.num_images = num_images
        self.length = kContainerBlockSize_CntHdr + num_images * kContainerBlockSize_ImgEntry + kContainerBlockSize_SignBlock
        self.sign_blk_offset = kContainerBlockSize_CntHdr + num_images * kContainerBlockSize_ImgEntry

    def out_bytes_str( self ):
        mybytes = [self.version,
                   self.length & 0xFF,
                   (self.length & 0xFF00) >> 8,
                   self.tag,
                   self.flags & 0xFF,
                   (self.flags & 0xFF00) >> 8,
                   (self.flags & 0xFF0000) >> 16, 
                   (self.flags & 0xFF000000) >> 24,
                   self.sw_ver & 0xFF,
                   (self.sw_ver & 0xFF00) >> 8,
                   self.fuse_ver,
                   self.num_images,
                   self.sign_blk_offset & 0xFF,
                   (self.sign_blk_offset & 0xFF00) >> 8,
                   self.reserved1 & 0xFF,
                   (self.reserved1 & 0xFF00) >> 8
                    ]
        myByteStr = ''
        for i in range(len(mybytes)):
            myByteStr += chr(mybytes[i])
        return myByteStr

class imgEntryStruct(object):

    def __init__( self, parent=None):
        #super(imgEntryStruct, self).__init__(parent)
        self.offset = None
        self.size = None
        self.load_addr = None
        self.reserved1 = 0x00000000
        self.entry = None
        self.reserved2 = 0x00000000
        self.flags = kImgEntry_Flags
        self.metadata = 0x00000000
        self.hash = [0x0] * 64
        self.iv = [0x0] * 32

    def set_members( self, deviceMapStart, imageExecAddr, imageData, hasEdgelockFw=False ):
        if (deviceMapStart & 0xFF000000) == (imageExecAddr & 0xFF000000):
            cntrOffset = 0
            if hasEdgelockFw:
                cntrOffset = RTyyyy_gendef.kContainerOffset_NOR + RTyyyy_gendef.kContainerSize_Edgelock
            else:
                cntrOffset = RTyyyy_gendef.kContainerOffset_NOR
            self.offset = imageExecAddr - deviceMapStart - cntrOffset
        else:
            if hasEdgelockFw:
                self.offset = RTyyyy_memdef.kMemBlockSize_Container + RTyyyy_memdef.kMemBlockSize_Edgelock
            else:
                self.offset = RTyyyy_memdef.kMemBlockSize_Container
        self.size = len(imageData)
        self.load_addr = imageExecAddr
        self.entry = imageExecAddr
        hashType = (self.flags & 0x700) >> 8
        hashObj = None
        if hashType == kHashType_Sha256:
            hashObj = hashlib.sha256(imageData)
        elif hashType == kHashType_Sha384:
            hashObj = hashlib.sha384(imageData)
        elif hashType == kHashType_Sha512:
            hashObj = hashlib.sha512(imageData)
        else:
            pass
        digest = hashObj.digest()
        for i in range(len(digest)):
            self.hash[i] = ord(digest[i])

    def out_bytes_str( self ):
        mybytes = [self.offset & 0xFF,
                   (self.offset & 0xFF00) >> 8,
                   (self.offset & 0xFF0000) >> 16, 
                   (self.offset & 0xFF000000) >> 24,
                   self.size & 0xFF,
                   (self.size & 0xFF00) >> 8,
                   (self.size & 0xFF0000) >> 16, 
                   (self.size & 0xFF000000) >> 24,
                   self.load_addr & 0xFF,
                   (self.load_addr & 0xFF00) >> 8,
                   (self.load_addr & 0xFF0000) >> 16, 
                   (self.load_addr & 0xFF000000) >> 24,
                   self.reserved1 & 0xFF,
                   (self.reserved1 & 0xFF00) >> 8,
                   (self.reserved1 & 0xFF0000) >> 16, 
                   (self.reserved1 & 0xFF000000) >> 24,
                   self.entry & 0xFF,
                   (self.entry & 0xFF00) >> 8,
                   (self.entry & 0xFF0000) >> 16, 
                   (self.entry & 0xFF000000) >> 24,
                   self.reserved2 & 0xFF,
                   (self.reserved2 & 0xFF00) >> 8,
                   (self.reserved2 & 0xFF0000) >> 16, 
                   (self.reserved2 & 0xFF000000) >> 24,
                   self.flags & 0xFF,
                   (self.flags & 0xFF00) >> 8,
                   (self.flags & 0xFF0000) >> 16, 
                   (self.flags & 0xFF000000) >> 24,
                   self.metadata & 0xFF,
                   (self.metadata & 0xFF00) >> 8,
                   (self.metadata & 0xFF0000) >> 16, 
                   (self.metadata & 0xFF000000) >> 24
                        ]
        myByteStr = ''
        for i in range(len(mybytes)):
            myByteStr += chr(mybytes[i])
        for i in range(len(self.hash)):
            myByteStr += chr(self.hash[i])
        for i in range(len(self.iv)):
            myByteStr += chr(self.iv[i])
        return myByteStr

class signBlockStruct(object):

    def __init__( self, parent=None):
        #super(signBlockStruct, self).__init__(parent)
        self.version = kSignBlock_Version
        self.length = kContainerBlockSize_SignBlock
        self.tag = kSignBlock_Tag
        self.cert_offset = 0x0000
        self.srk_offset = 0x0000
        self.sign_offset = 0x0000
        self.blob_offset = 0x0000
        self.reserved1 = 0x00000000

    def set_members( self ):
        pass

    def out_bytes_str( self ):
        mybytes = [self.version,
                   self.length & 0xFF,
                   (self.length & 0xFF00) >> 8,
                   self.tag,
                   self.cert_offset & 0xFF,
                   (self.cert_offset & 0xFF00) >> 8,
                   self.srk_offset & 0xFF,
                   (self.srk_offset & 0xFF00) >> 8,
                   self.sign_offset & 0xFF,
                   (self.sign_offset & 0xFF00) >> 8,
                   self.blob_offset & 0xFF,
                   (self.blob_offset & 0xFF00) >> 8,
                   self.reserved1 & 0xFF,
                   (self.reserved1 & 0xFF00) >> 8,
                   (self.reserved1 & 0xFF0000) >> 16, 
                   (self.reserved1 & 0xFF000000) >> 24,
                    ]
        myByteStr = ''
        for i in range(len(mybytes)):
            myByteStr += chr(mybytes[i])
        return myByteStr

class containerStruct(object):

    def __init__( self, parent=None):
        #super(containerStruct, self).__init__(parent)
        self.cntHdrStruct = cntHdrStruct()
        self.imgEntryStruct = imgEntryStruct()
        self.signBlockStruct = signBlockStruct()
        self.hasEdgelockFw = False

    def set_members( self, deviceMapStart, imageExecAddr, imageData, hasEdgelockFw=False ):
        self.hasEdgelockFw = hasEdgelockFw
        self.cntHdrStruct.set_members(1)
        self.imgEntryStruct.set_members(deviceMapStart, imageExecAddr, imageData, hasEdgelockFw)
        self.signBlockStruct.set_members()

    def out_bytes_str( self ):
        edgelockCntrSize = 0
        if self.hasEdgelockFw:
            edgelockCntrSize = RTyyyy_gendef.kContainerSize_Edgelock
        paddingBytes = [0x00] * (RTyyyy_memdef.kMemBlockSize_Container - edgelockCntrSize - self.cntHdrStruct.length)
        paddingBytesStr = ''
        for i in range(len(paddingBytes)):
            paddingBytesStr += chr(paddingBytes[i])
        return self.cntHdrStruct.out_bytes_str() + self.imgEntryStruct.out_bytes_str() + self.signBlockStruct.out_bytes_str() + paddingBytesStr


