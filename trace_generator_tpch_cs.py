# coding=utf-8
## 1MB => 262144
## 2MB => 524288
## 4MB => 1048576
## 8MB => 2097152
## 16MB => 4194304
## 32MB => 8388608
## 64MB => 16777216
## 1GB => 268435456

##HEADER | TotalNumberOFAttributes | NumberOfPredicates |

import subprocess
import os
import sys

ADDR_R = 1024 * 1024 * 1024
ADDR_W = 1024 * 1024 * 4096
REG_SIZE = 4
BASEDIR = "/Users/diegogomestome/Dropbox/UFPR/Mestrado_Diego_Tome/EXPERIMENTOS/"

input_file = BASEDIR + "bitmap_files/result.txt"
dynamic_trace = BASEDIR + "columnStore/traços/x86/output_trace.out.tid0.dyn.out"
memory_trace = BASEDIR + "columnStore/traços/x86/output_trace.out.tid0.mem.out"
static_trace = BASEDIR + "columnStore/traços/x86/output_trace.out.tid0.stat.out"

FILE_INPUT = open(input_file, 'r')
FILE_DYN = open(dynamic_trace, 'w')
FILE_MEM = open(memory_trace, 'w')
FILE_STAT = open(static_trace, 'w')

header = FILE_INPUT.readline()
header = header.split("|")
totalAttributes = int(header[0])
numberPredicates = int(header[1])
instructionAddress = 1024
tuples = FILE_INPUT.readlines()
qtdTuples = len(tuples)
w, h = qtdTuples, numberPredicates
dynamic_block = [[0 for x in range(w)] for y in range(h)]
memory_block = [[0 for x in range(w)] for y in range(h)]

AttributesByStage = [totalAttributes, totalAttributes, totalAttributes]
address_base = [1024, 1024, 1024]
address_target = [111024, 121024, 131024]

FILE_DYN.write("# SiNUCA Trace Dynamic\n")
FILE_MEM.write("# SiNUCA Trace Memory\n")
FILE_STAT.write("# SiNUCA Trace Static\n")

basicBlock = 0
#################### STATIC FILE #########################
print "Generating Static File..."
for i in range(numberPredicates):
    basicBlock += 1
    FILE_STAT.write("@" + str(basicBlock) + "\n")  #COLUMN-AT-A-TIME#
    FILE_STAT.write("ADD 1 " + str(instructionAddress) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
    instructionAddress += 4
    FILE_STAT.write("CMP 1 " + str(instructionAddress) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
    instructionAddress += 3
    FILE_STAT.write("JNE 7 " + str(instructionAddress) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
    basicBlock += 1
    instructionAddress += 2
    FILE_STAT.write("@" + str(basicBlock) + "\n")  #APPLY PREDICATE)#
    FILE_STAT.write("MOVDQU 8 " + str(instructionAddress) + " 6 1 8 1 9 0 0 1 0 0 3 0 0 0\n")
    instructionAddress += 6
    FILE_STAT.write("CMP 1 " + str(instructionAddress) + " 3 1 9 1 10 0 0 0 0 0 3 0 0 0\n")
    instructionAddress += 3
    FILE_STAT.write("JNBE 7 " + str(instructionAddress) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
    basicBlock += 1
    instructionAddress += 2
    FILE_STAT.write("@" + str(basicBlock) + "\n")  #BITMAP (STORE)#
    FILE_STAT.write("MOVDQU 9 " + str(instructionAddress) + " 6 1 12 1 13 0 0 0 0 1 3 0 0 0\n")
    instructionAddress += 6
    FILE_STAT.write("ADD 1 " + str(instructionAddress) + " 4 1 1 1 1 0 0 0 0 0 3 0 0 0\n")
    instructionAddress += 4
    FILE_STAT.write("CMP 1 " + str(instructionAddress) + " 3 1 1 1 2 0 0 0 0 0 3 0 0 0\n")
    instructionAddress += 3
    FILE_STAT.write("JNBE 7 " + str(instructionAddress) + " 2 1 2 1 3 0 0 0 0 0 4 0 0 0\n")
    instructionAddress += 2

FILE_STAT.write("# eof")
FILE_STAT.close()
print "Static File Ok!"
#################### DYNAMIC AND MEMORY FILE #########################
print "Generating Data For Dynamic and Memory Files..."
for i in range(len(tuples)):
    elem = tuples[i]
    elem = elem.split()
    basicBlock = 0
    for j in range(numberPredicates):
        ########################################################################
        ##  PREDICATE MATCH
        ########################################################################
        if elem[j] == '1':
            dynamic_block[j][i] = str(str(basicBlock + 1) + "\n")
            dynamic_block[j][i] += str(str(basicBlock + 2) + "\n")
            memory_block[j][i] = ("R 4 " + str(ADDR_R) + " " + str(basicBlock + 2) + "\n")
            ADDR_R += REG_SIZE
            ############# CREATE THE BITMAP ###################################
            dynamic_block[j][i] += str(str(basicBlock + 3) + "\n")
            memory_block[j][i] += str("W 4 " + str(ADDR_W) + " " + str(basicBlock + 3) + "\n")
            ADDR_W += REG_SIZE
        else:
            dynamic_block[j][i] = str(str(basicBlock + 1) + "\n")
            dynamic_block[j][i] += str(str(basicBlock + 2) + "\n")
            memory_block[j][i] = ("R 4 " + str(ADDR_R) + " " + str(basicBlock + 2) + "\n")
            ADDR_R += REG_SIZE
        basicBlock += 3
print "Writing on Dynamic and Memory File..."
######### WRITES ON DYNAMIC AND MEMORY FILE ################3
for j in range(numberPredicates):
    for i in range(len(tuples)):
        FILE_DYN.write(dynamic_block[j][i])
        if memory_block[j][i] != 0:
            FILE_MEM.write(memory_block[j][i])

FILE_MEM.close()
FILE_DYN.close()
FILE_INPUT.close()
print "Dynamic and Memory Files Ok!"
print "Compressing Files..."
os.system("gzip " + BASEDIR + "columnStore/traços/x86/" + "*.out")
print "ALL Done!"
