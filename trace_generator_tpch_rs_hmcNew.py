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

hmc_size = 0
for hmc_size in (4, 8, 16, 32, 64):
    BLOCK_SIZE = hmc_size

    ADDR_R = 1024 * 1024 * 1024
    ADDR_W = 1024 * 1024 * 4096
    REG_SIZE = 4
    INST_ADDR = 1024
    BASEDIR = "/Users/diegogomestome/Dropbox/UFPR/Mestrado_Diego_Tome/EXPERIMENTOS/"

    input_file = BASEDIR + "bitmap_files/input_teste.txt"
    dynamic_trace = BASEDIR + "traces/HMC/Q06/rowStore/" + str(BLOCK_SIZE * REG_SIZE) + "/output_trace.out.tid0.dyn.out"
    memory_trace = BASEDIR + "traces/HMC/Q06/rowStore/" + str(BLOCK_SIZE * REG_SIZE) + "/output_trace.out.tid0.mem.out"
    static_trace = BASEDIR + "traces/HMC/Q06/rowStore/" + str(BLOCK_SIZE * REG_SIZE) + "/output_trace.out.tid0.stat.out"

    FILE_INPUT = open(input_file, 'r')
    FILE_DYN = open(dynamic_trace, 'w')
    FILE_MEM = open(memory_trace, 'w')
    FILE_STAT = open(static_trace, 'w')

    header = FILE_INPUT.readline()
    header = header.split("|")
    numberOfTables = int(header[0])
    numberOfPredicates = int(header[(numberOfTables * 2) + 1])
    instructionAddress = 1024
    basicBlock = 0

    tuples = FILE_INPUT.readlines()
    FILE_INPUT.close()

    qtdTuples = len(tuples)
    w, h = qtdTuples, numberOfPredicates
    dynamic_block = [["" for x in range(w)] for y in range(h)]
    memory_block = [["" for x in range(w)] for y in range(h)]
    bitColSum = [0 for y in range(numberOfPredicates)]
    tuplesByTable = [0 for y in range(qtdTuples)]
    totalAttributes = [0 for y in range(3)]

    for i in range(numberOfTables):
        tuplesByTable[i] = int(header[i + 1])
        totalAttributes[i] = int(header[i + numberOfTables + 1])

    AttributesByStage = [totalAttributes, totalAttributes, totalAttributes]
    address_base = [ADDR_R, ADDR_R * 2, ADDR_R * 3]
    address_target = [ADDR_W, int(ADDR_W * 1.5), ADDR_W * 2]

    FILE_DYN.write("# SiNUCA Trace Dynamic\n")
    FILE_MEM.write("# SiNUCA Trace Memory\n")
    FILE_STAT.write("# SiNUCA Trace Static\n")

    basicBlock = 0
    print("Generating Traces Files For HMC... " + str(hmc_size * 4) + " Bytes")
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
        FILE_STAT.write("JNE 7 " + str(INST_ADDR) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
        basicBlock += 1
        INST_ADDR += 2
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # MATERIALIZATION (STORE) #
        FILE_STAT.write("HMC_CPY 13 " + str(INST_ADDR) + " 4 1 10 1 11 0 0 0 0 1 3 0 0 0\n")  # W
        INST_ADDR += 4
        FILE_STAT.write("ADD 1 " + str(INST_ADDR) + " 4 1 1 1 1 0 0 0 0 0 3 0 0 0\n")
        INST_ADDR += 4
        FILE_STAT.write("CMP 1 " + str(INST_ADDR) + " 3 1 1 1 2 0 0 0 0 0 3 0 0 0\n")
        INST_ADDR += 3
        FILE_STAT.write("JNE 7 " + str(INST_ADDR) + " 2 1 2 1 3 0 0 0 0 0 4 0 0 0\n")
        INST_ADDR += 2

    FILE_STAT.write("# eof")
    FILE_STAT.close()
    print "Static File Ok!"
    fieldCount = BLOCK_SIZE
    lastSum = 0
    #################### DYNAMIC AND MEMORY FILE #########################
    print "Generating Data For Dynamic and Memory Files..."
    for tuple in range(len(tuples)):
        elem = tuples[tuple]
        elem = elem.split()
        basicBlock = 0
        for column in range(numberOfPredicates):
            ########################################################################
            ##  ITERATOR TUPLE-AT-A-TIME
            ########################################################################
            dynamic_block[column][tuple] += str(str(basicBlock + 1) + "\n")
            if fieldCount == 1:
                bitColSum[column] += int(elem[column])
                if bitColSum[column] > 0:
                    lastSum = bitColSum[column]
                    bitColSum[column] = 0
                    if column == numberOfPredicates - 1:
                        fieldCount = BLOCK_SIZE + 1
                    ########################################################################
                    ##  PREDICATE MATCH
                    ########################################################################
                    dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                    memory_block[column][tuple] += (
                        "R " + str(BLOCK_SIZE * REG_SIZE) + " " + str(address_base[column]) + " " + str(
                            basicBlock + 2) + "\n")
                    address_base[column] += (REG_SIZE * BLOCK_SIZE)
                    ########################################################################
                    ## MATERIALIZATION ALL TUPLES
                    ########################################################################
                    if totalAttributes[0] < BLOCK_SIZE:
                        sizeOfMaterialization = 1
                    else:
                        sizeOfMaterialization = (totalAttributes[0] * 4) / (REG_SIZE * BLOCK_SIZE)

                    for i in range(sizeOfMaterialization):
                        dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                        memory_block[column][tuple] += str(
                            "R " + str(BLOCK_SIZE * REG_SIZE) + " " + str(address_target[column]) + " " + str(
                                basicBlock + 3) + "\n")
                        address_target[column] += (REG_SIZE * 4)
                        memory_block[column][tuple] += str(
                            "W " + str(BLOCK_SIZE * REG_SIZE) + " " + str(address_target[column]) + " " + str(
                                basicBlock + 3) + "\n")
                        address_target[column] += (REG_SIZE * 4)
                elif column > 0:
                    if column == numberOfPredicates - 1:
                        fieldCount = BLOCK_SIZE + 1
                    if lastSum > 0:
                        ########################################################################
                        ##  PREDICATE MATCH
                        ########################################################################
                        dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                        memory_block[column][tuple] += (
                            "R " + str(BLOCK_SIZE * REG_SIZE) + " " + str(address_base[column]) + " " + str(
                                basicBlock + 2) + "\n")
                        address_base[column] += (REG_SIZE * BLOCK_SIZE)
                else:
                    if column == numberOfPredicates - 1:
                        fieldCount = BLOCK_SIZE + 1
                    ########################################################################
                    ##  PREDICATE MATCH
                    ########################################################################
                    dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                    memory_block[column][tuple] += (
                        "R " + str(BLOCK_SIZE * REG_SIZE) + " " + str(address_base[column]) + " " + str(
                            basicBlock + 2) + "\n")
                    address_base[column] += (REG_SIZE * BLOCK_SIZE)
            else:
                bitColSum[column] += int(elem[column])  # Controls the sum of bits in each column
            basicBlock += 3  # Controls the basicBlock way for each column
        fieldCount -= 1  # Counts the amount of tuples to process

    print "Writing on Dynamic and Memory File..."
    ######### WRITES ON DYNAMIC AND MEMORY FILE ################3
    for column in range(numberOfPredicates):
        for tuple in range(len(tuples)):
            FILE_DYN.write(dynamic_block[column][tuple])
            if memory_block[column][tuple] != 0:
                FILE_MEM.write(memory_block[column][tuple])

    FILE_MEM.close()
    FILE_DYN.close()
    print "Dynamic and Memory Files Ok!"
    print "Compressing Files..."
    os.system("rm -f " + BASEDIR + "traces/HMC_NEW/Q06/rowStore/" + str(BLOCK_SIZE * REG_SIZE) + "/" + "*gz")
    os.system("gzip " + BASEDIR + "traces/HMC_NEW/Q06/rowStore/" + str(BLOCK_SIZE * REG_SIZE) + "/" + "*.out")
    print "ALL Done!"
