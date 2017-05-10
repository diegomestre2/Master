# coding=utf-8
## 1MB => 262144
## 2MB => 524288
## 4MB => 1048576
## 8MB => 2097152
## 16MB => 4194304
## 32MB => 8388608
## 64MB => 16777216
## 1GB => 268435456

##HEADER | NumberOfTables | ...TuplesByTable ... | TotalNumberOfAttributes | NumberOfPredicates |

import os

VECTOR_SIZE = 1000
QUERY = "Query06"
QUERY_ENGINE = "vectorized"

def writeOnDynamicAndMemoryFilesVectorized():
    global column, tuple
    ######### WRITES ON DYNAMIC AND MEMORY FILE COLUMN-AT-A-TIME################3
    for tuple in range(len(tuples)):
        for column in range(numberOfPredicates):
            FILE_DYN.write(dynamic_block[column][tuple])
            if memory_block[column][tuple] != 0:
                FILE_MEM.write(memory_block[column][tuple])


for HMC_OPERATION_CAPACITY in (16, 256):

    DATA_ADDR_READ = 1024 * 1024 * 1024 #Bytes
    DATA_ADDR_WRITE = 1024 * 1024 * 4096 #Bytes
    DATA_SIZE = 4 #Bytes
    INSTRUCTION_ADDR = 1024 #Bytes

    BASEDIR = "/Users/diegogomestome/Dropbox/UFPR/Mestrado_Diego_Tome/EXPERIMENTOS/"
    input_file = BASEDIR + "bitmap_files/resultQ06.txt"
    dynamic_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC/" + str(
        HMC_OPERATION_CAPACITY) + "/output_trace.out.tid0.dyn.out"

    memory_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC/" + str(
        HMC_OPERATION_CAPACITY) + "/output_trace.out.tid0.mem.out"

    static_trace = BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC/" + str(
        HMC_OPERATION_CAPACITY) + "/output_trace.out.tid0.stat.out"

    ################### TREATING FILE INPUT ###################
    FILE_INPUT = open(input_file, 'r')

    header = FILE_INPUT.readline()
    header = header.split("|")
    numberOfTables = int(header[0])
    numberOfPredicates = int(header[(numberOfTables * 2) + 1])

    tuples = FILE_INPUT.readlines()
    FILE_INPUT.close()
    ##########################################################
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

    address_base = [DATA_ADDR_READ, DATA_ADDR_READ + (qtdTuples * DATA_SIZE),         #READ
                    DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 2)]

    address_target = [DATA_ADDR_WRITE, DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE) + 1, #WRITE
                      DATA_ADDR_WRITE + (qtdTuples * DATA_SIZE * 2) + 1]

    address_target_bitmap = [int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3)),            #BITMAP
                             int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + qtdTuples),
                             int(DATA_ADDR_READ + (qtdTuples * DATA_SIZE * 3) + (2 * qtdTuples))]

    FILE_STAT = open(static_trace, 'w')
    FILE_STAT.write("# SiNUCA Trace Static\n")

    basicBlock = 0
    print("Generating Traces Files For HMC... " + str(HMC_OPERATION_CAPACITY) + " Bytes")
    #################### STATIC FILE #########################
    print "Generating Static File..."
    for tuple in range(numberOfPredicates):
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # COLUMN-AT-A-TIME#
        FILE_STAT.write("ADD 1 " + str(INSTRUCTION_ADDR) + " 4 1 1 1 2 0 0 0 0 0 3 0 0 0\n")
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("CMP 1 " + str(INSTRUCTION_ADDR) + " 3 1 3 1 4 0 0 0 0 0 3 0 0 0\n")
        INSTRUCTION_ADDR += 3
        FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 2 1 5 0 0 0 0 0 4 0 0 0\n")
        INSTRUCTION_ADDR += 2
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY PREDICATE)#
        FILE_STAT.write("HMC_CMP 12 " + str(INSTRUCTION_ADDR) + " 4 1 12 1 9 0 0 1 0 0 3 0 0 0\n")  # R HMC_SIZE
        INSTRUCTION_ADDR += 4
        FILE_STAT.write("JNE 7 " + str(INSTRUCTION_ADDR) + " 2 1 9 1 10 0 0 0 0 0 4 0 0 0\n")
        INSTRUCTION_ADDR += 2
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # MATCH POSITION (STORE)#
        FILE_STAT.write("MOV 9 " + str(INSTRUCTION_ADDR) + " 6 1 9 1 12 0 0 0 0 1 3 0 0 0\n")  # W 1Byte
        INSTRUCTION_ADDR += 6
        basicBlock += 1
        FILE_STAT.write("@" + str(basicBlock) + "\n")  # APPLY OP)#
        FILE_STAT.write("HMC_CMP 12 " + str(INSTRUCTION_ADDR) + " 4 1 12 1 9 0 0 0 0 0 3 0 0 0\n")  # R HMC_SIZE
        INSTRUCTION_ADDR += 4

    FILE_STAT.write("# eof")
    FILE_STAT.close()
    print "Static File Ok!"

    FILE_DYN = open(dynamic_trace, 'w')
    FILE_MEM = open(memory_trace, 'w')
    FILE_DYN.write("# SiNUCA Trace Dynamic\n")
    FILE_MEM.write("# SiNUCA Trace Memory\n")
    fieldsByInstruction = HMC_OPERATION_CAPACITY / 4
    lastFieldsSum = 0
    loadSize = 32
    #################### DYNAMIC AND MEMORY FILE #########################
    print "Generating Data For Dynamic and Memory Files..."
    for tuple in range(len(tuples)):
        elem = tuples[tuple]
        elem = elem.split()
        basicBlock = 0
        for column in range(numberOfPredicates):
            bitColSum[column] += int(elem[column])
            ########################################################################
            ##  HMC INSTRUCTION WILL BE SENDED
            ########################################################################
            if fieldsByInstruction == 1:
                dynamic_block[column][tuple] += str(str(basicBlock + 1) + "\n")
                ########################################################################
                ##  MATCH FOUND
                ########################################################################
                if bitColSum[column] > 0 or column == 0:
                    lastFieldsSum = bitColSum[column]
                    bitColSum[column] = 0
                    ########################################################################
                    ##  APPLY PREDICATE
                    ########################################################################
                    dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                    memory_block[column][tuple] += (
                        "R " + str(HMC_OPERATION_CAPACITY) + " " + str(address_base[column]) + " " + str(
                            basicBlock + 2) + "\n")
                    address_base[column] += HMC_OPERATION_CAPACITY
                    ########################################################################
                    # CREATE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                    ########################################################################
                    if HMC_OPERATION_CAPACITY == 16:
                        loadSize = 16
                    if column == numberOfPredicates - 1:
                        fieldsByInstruction = (HMC_OPERATION_CAPACITY / 4) + 1
                        dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                        memory_block[column][tuple] += str(
                            "W " + str(HMC_OPERATION_CAPACITY / loadSize) + " " + str(
                                address_target_bitmap[column]) + " " + str(basicBlock + 3) + "\n")
                        address_target_bitmap[column] += (HMC_OPERATION_CAPACITY / loadSize)
                elif column > 0:
                    if lastFieldsSum > 0:
                        lastFieldsSum = 0
                        dynamic_block[column][tuple] += str(str(basicBlock + 2) + "\n")
                        memory_block[column][tuple] += (
                            "R " + str(HMC_OPERATION_CAPACITY) + " " + str(address_base[column]) + " " + str(
                                basicBlock + 2) + "\n")
                        address_base[column] += HMC_OPERATION_CAPACITY
                    else:
                        dynamic_block[column][tuple] += str(str(basicBlock + 4) + "\n")

                    ########################################################################
                    # STORE THE BITMAP 1 Byte of Store by 32 Bytes of Loads
                    ########################################################################
                    if HMC_OPERATION_CAPACITY == 16:
                        loadSize = 16
                    if column == numberOfPredicates - 1:
                        fieldsByInstruction = (HMC_OPERATION_CAPACITY / 4) + 1
                        dynamic_block[column][tuple] += str(str(basicBlock + 3) + "\n")
                        memory_block[column][tuple] += str(
                            "W " + str(HMC_OPERATION_CAPACITY / loadSize) + " " + str(
                                address_target_bitmap[column]) + " " + str(basicBlock + 3) + "\n")
                        address_target_bitmap[column] += (HMC_OPERATION_CAPACITY / loadSize)

                        # if lastSum > 0:
                        # elif column > 0:
            # if fieldCount == 1:
            basicBlock += 4
            loadSize = 32
        fieldsByInstruction -= 1

    print "Writing on Dynamic and Memory File..."

    writeOnDynamicAndMemoryFilesVectorized()

    FILE_MEM.close()
    FILE_DYN.close()
    print "Dynamic and Memory Files Ok!"

    print "Compressing Files..."
    os.system("rm -f " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC/" + str(HMC_OPERATION_CAPACITY) + "/" + "*gz")
    os.system("gzip " + BASEDIR + "traces/" + QUERY + "/columnStore/" + QUERY_ENGINE + "/HMC/" + str(HMC_OPERATION_CAPACITY) + "/" + "*.out")
    print "ALL Done!"
