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
INST_ADDR = 1024
BASEDIR = "/Users/diegogomestome/Dropbox/UFPR/Mestrado_Diego_Tome/EXPERIMENTOS/"

input_file = BASEDIR + "bitmap_files/resultQ06.txt"
dynamic_trace = BASEDIR + "columnStore/traços/HMC/Q06/output_trace.out.tid0.dyn.out"
memory_trace = BASEDIR + "columnStore/traços/HMC/Q06/output_trace.out.tid0.mem.out"
static_trace = BASEDIR + "columnStore/traços/HMC/Q06/output_trace.out.tid0.stat.out"

FILE_INPUT = open(input_file, 'r')
FILE_DYN = open(dynamic_trace, 'w')
FILE_MEM = open(memory_trace, 'w')
FILE_STAT = open(static_trace, 'w')


header = FILE_INPUT.readline()
header = header.split("|")
totalAttributes = int(header[0])
numberOfPredicates = int(header[1])

tuples = FILE_INPUT.readlines()
qtdTuples = len(tuples)
w, h = qtdTuples, numberOfPredicates
dynamic_block = [[0 for x in range(w)] for y in range(h)]
memory_block = [[0 for x in range(w)] for y in range(h)]

predicateMatch = [0 for y in range(numberOfPredicates)]
predicateNotMatch = [0 for y in range(numberOfPredicates)]

AttributesByStage = [totalAttributes, totalAttributes, totalAttributes]
address_base = [1024, 1024, 1024]
address_target = [111024, 121024, 131024]

FILE_DYN.write("# SiNUCA Trace Dynamic\n")
FILE_MEM.write("# SiNUCA Trace Memory\n")
FILE_STAT.write("# SiNUCA Trace Static\n")

basicBlock = 0
print "Generating Traces Files For HMC..."
#################### STATIC FILE #########################
print "Generating Static File..."
for i in range(numberOfPredicates):
    basicBlock += 1
    FILE_STAT.write("@" + str(basicBlock) + "\n")  # COLUMN-AT-A-TIME#
    FILE_STAT.write("ADD 1 " + str(INST_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
    INST_ADDR += 4
    FILE_STAT.write("CMP 1 " + str(INST_ADDR) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
    INST_ADDR += 3
    FILE_STAT.write("JNE 7 " + str(INST_ADDR) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
    basicBlock += 1
    INST_ADDR += 2
    FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE) (LOAD) #
    FILE_STAT.write("HMC_CMP 12 " + str(INST_ADDR) + " 4 1 9 1 10 0 0 1 0 0 3 0 0 0\n")   # R
    INST_ADDR += 4
    FILE_STAT.write("JNBE 7 " + str(INST_ADDR) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
    basicBlock += 1
    INST_ADDR += 2
    FILE_STAT.write("@" + str(basicBlock) + "\n")  # MATERIALIZATION (STORE) #
    FILE_STAT.write("HMC_CPY 13 " + str(INST_ADDR) + " 4 1 10 1 11 0 0 0 0 1 3 0 0 0\n")  # W
    INST_ADDR += 4
    FILE_STAT.write("ADD 1 " + str(INST_ADDR) + " 4 1 1 1 1 0 0 0 0 0 3 0 0 0\n")
    INST_ADDR += 4
    FILE_STAT.write("CMP 1 " + str(INST_ADDR) + " 3 1 1 1 2 0 0 0 0 0 3 0 0 0\n")
    INST_ADDR += 3
    FILE_STAT.write("JNBE 7 " + str(INST_ADDR) + " 2 1 2 1 3 0 0 0 0 0 4 0 0 0\n")
    INST_ADDR += 2

FILE_STAT.write("# eof")
FILE_STAT.close()
print "Static File Ok!"
#################### DYNAMIC AND MEMORY FILE #########################
print "Generating Data For Dynamic and Memory Files..."
for i in range(len(tuples)):
    elem = tuples[i]
    elem = elem.split()
    basicBlock = 0
    for column in range(numberOfPredicates):
        dynamic_block[column][i] = str(str(basicBlock + 1) + "\n")
        if elem[column] == '1':
            predicateMatch[column] += 1
        else:
            predicateNotMatch[column] += 1
        ########################################################################
        ##  PREDICATE MATCH
        ########################################################################
        if predicateMatch[column] == 4:
            predicateMatch[column] = 0
            dynamic_block[column][i] += str(str(basicBlock + 2) + "\n")
            memory_block[column][i] = ("R 16 " + str(ADDR_R) + " " + str(basicBlock + 2) + "\n")
            ADDR_R += (REG_SIZE * 4)
            ############# CREATE THE BITMAP ###################################
            dynamic_block[column][i] += str(str(basicBlock + 3) + "\n")
            memory_block[column][i] += str("W 16 " + str(ADDR_W) + " " + str(basicBlock + 3) + "\n")
            ADDR_W += (REG_SIZE * 4)
        if predicateNotMatch[column] == 4:
            predicateNotMatch[column] = 0
            dynamic_block[column][i] += str(str(basicBlock + 2) + "\n")
            memory_block[column][i] = ("R 16 " + str(ADDR_R) + " " + str(basicBlock + 2) + "\n")
            ADDR_R += (REG_SIZE * 4)

        basicBlock += 3

print "Writing on Dynamic and Memory File..."
######### WRITES ON DYNAMIC AND MEMORY FILE ################3
for column in range(numberOfPredicates):
    for i in range(len(tuples)):
        FILE_DYN.write(dynamic_block[column][i])
        if memory_block[column][i] != 0:
            FILE_MEM.write(memory_block[column][i])

FILE_MEM.close()
FILE_DYN.close()
FILE_INPUT.close()
print "Dynamic and Memory Files Ok!"
print "Compressing Files..."
os.system("gzip " + BASEDIR + "columnStore/traços/HMC/Q06/" + "*.out")
print "ALL Done!"
