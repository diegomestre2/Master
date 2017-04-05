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

    DATA_ADDR_READ = 1024 * 1024 * 1024
    DATA_ADDR_WRITE = 1024 * 1024 * 4096
    REGISTER_SIZE = 4
    INSTRUCTION_ADDR = 1024
    BASE_DIRECTORY = "/Users/diegogomestome/Dropbox/UFPR/Mestrado_Diego_Tome/EXPERIMENTOS/"

    input_file = BASE_DIRECTORY + "bitmap_files/resultQ06.txt"
    dynamic_trace = BASE_DIRECTORY + "traces/HMC_NEW/Q06/columnStore/" + str(BLOCK_SIZE * REGISTER_SIZE) + "/output_trace.out.tid0.dyn.out"
    memory_trace = BASE_DIRECTORY + "traces/HMC_NEW/Q06/columnStore/" + str(BLOCK_SIZE * REGISTER_SIZE) + "/output_trace.out.tid0.mem.out"
    static_trace = BASE_DIRECTORY + "traces/HMC_NEW/Q06/columnStore/" + str(BLOCK_SIZE * REGISTER_SIZE) + "/output_trace.out.tid0.stat.out"

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
    address_base = [DATA_ADDR_READ, DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE),
                    DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 2)]
    address_target = [DATA_ADDR_WRITE, DATA_ADDR_WRITE + (qtdTuples * REGISTER_SIZE) + 1,
                      DATA_ADDR_WRITE + (qtdTuples * REGISTER_SIZE * 2) + 1]
    address_target_bitmap = [DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 3),
                             DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 3) + qtdTuples,
                             DATA_ADDR_READ + (qtdTuples * REGISTER_SIZE * 3) + (2 * qtdTuples)]

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
        FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 5 1 6 0 0 0 0 0 3 0 0 0\n")
        INSTRUCTION_ADDR += 3
        FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 6 1 7 0 0 0 0 0 4 0 0 0\n")
        basicBlock += 1
        INSTRUCTION_ADDR += 2
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE)#
        FILE_STAT.write("HMC_LOCK 14 " + str(INSTRUCTION_ADDR) + " 4 1 5 0 0 0 0 0 0 3 0 0 1 -1 -1 -1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_LD 16 " + str(INSTRUCTION_ADDR) + " 4 1 5 0 0 0 1 0 0 3 0 0 1 -1 -1 0\n")  # R
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_OP 18 " + str(INSTRUCTION_ADDR) + " 4 1 5 0 0 0 0 0 0 3 0 0 1 0 -1 0\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_ST 17 " + str(INSTRUCTION_ADDR) + " 4 1 5 0 0 0 0 0 1 3 0 0 1 0 -1 -1\n")  # W
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("HMC_UNLOCK 15 " + str(INSTRUCTION_ADDR) + " 4 1 9 0 0 0 0 0 0 3 0 0 1 -1 -1 -1\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 5 1 5 0 0 0 0 0 3 0 0 0\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 10 1 7 0 0 0 0 0 4 0 0 0\n")
        INSTRUCTION_ADDR += 2

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
            dynamic_block[column][tuple] += str(str(basicBlock + 1) + "\n")
            bitColSum[column] += int(elem[column])
            if fieldCount == 1:
                if bitColSum[column] > 0 or column == 0:
                    lastSum = bitColSum[column]
                    bitColSum[column] = 0
                    if column == numberOfPredicates - 1:
                        fieldCount = BLOCK_SIZE + 1
                    ########################################################################
                    ##  PREDICATE MATCH
                    ########################################################################
                    dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                    memory_block[column][tuple] += (
                        "R "
                        + str(BLOCK_SIZE * REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(basicBlock + 2) + "\n")
                    address_base[column] += (REGISTER_SIZE * BLOCK_SIZE)
                    ########################################################################
                    ## CREATE THE BITMAP
                    ########################################################################
                    memory_block[column][tuple] += str("W "+ str((REGISTER_SIZE * HMC_OPERATION_CAPACITY) / loadSize) + " " + str(address_target_bitmap) + " " + str(basicBlock + 2) + "\n")
                    address_target[column] += (REGISTER_SIZE * BLOCK_SIZE)
                elif column > 0:
                    if column == numberOfPredicates - 1:
                        fieldCount = BLOCK_SIZE + 1
                    if lastSum > 0:
                        dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                        memory_block[column][tuple] += (
                            "R " + str(BLOCK_SIZE * REGISTER_SIZE) + " " + str(address_base[column]) + " " + str(basicBlock + 2) + "\n")
                        address_base[column] += (REGISTER_SIZE * BLOCK_SIZE)
                        ########################################################################
                        ## CREATE THE BITMAP
                        ########################################################################
                        memory_block[column][tuple] += str("W 1" + " " + str(address_target_bitmap) + " " + str(basicBlock + 2) + "\n")
                        address_target[column] += (REGISTER_SIZE * BLOCK_SIZE)
            basicBlock += 2
        fieldCount -= 1

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
    os.system("rm -f " + BASE_DIRECTORY + "traces/HMC_NEW/Q06/columnStore/" + str(BLOCK_SIZE * REGISTER_SIZE) + "/" + "*gz")
    os.system("gzip " + BASE_DIRECTORY + "traces/HMC_NEW/Q06/columnStore/" + str(BLOCK_SIZE * REGISTER_SIZE) + "/" + "*.out")
    print "ALL Done!"
