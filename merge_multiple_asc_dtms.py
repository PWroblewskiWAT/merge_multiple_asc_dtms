#!/usr/bin/env python
# coding: utf-8

# import necessary modules
import os
import time
import shutil
from merge_multiple_asc_dtms_fncts import MergeAscDtms, askUserForPath

# print program name
columns = shutil.get_terminal_size().columns
print(os.path.basename(__file__).center(columns))
print('-' * columns)

# specify paths to input and output catalogs
inputCatalog = askUserForPath('input')
outputCatalog = askUserForPath('output')

# initialize MergeAscDtms() class
merge = MergeAscDtms(inputCatalog, outputCatalog, ' ', 'merged_dtm.asc')

while True:
    # load all *.asc DTMs from input catalog and display the loading time in sec
    start = time.time()
    headers, dtms = merge.loadMultipleAscDtms()
    print(f'Data loading - execution time: {round(time.time() - start, 1)} [s]\n')

    # calculate statistics of all datasets
    statistics = merge.findStatisticsForDatasets(headers)

    # find spatial distribution of all datasets
    numOfDatasetsAlongX, numOfDatasetsAlongY = merge.findSpatialDistributionOfDatasets(statistics)

    # sort datasets in Y-descending and X-ascending order
    sortedDatasets = merge.sortDatasets(headers, numOfDatasetsAlongX)

    # find tiles with max X and Y coordinates
    xMaxTile, yMaxTile = merge.findTilesWithMaxCoords(headers)

    # create final DTM array initially filled with 'nodata_values'
    finalDtmArray = merge.createFinalArrayFilledWithNoDataValues(statistics, headers, xMaxTile, yMaxTile)

    # fill the final DTM array with data from sorted datasets
    start = time.time()
    merge.fillFinalDtmArrayWithData(sortedDatasets, headers, statistics, dtms, finalDtmArray)
    print(f'Merging DTMs - execution time: {round(time.time() - start, 1)} [s]\n')

    # create header to be used in output file
    finalHeader = merge.constructFinalHeader(finalDtmArray, statistics)

    # export created header and DTM array as *.asc file
    start = time.time()
    merge.exportFinalDtmAsAscFile(finalHeader, finalDtmArray)
    print(f'Exporting DTM - execution time: {round(time.time() - start, 1)} [s]\n')

    # ask if user want to merge another set of DTMs or just to exit the program
    while True:
        answer = input("Would You like to merge another set of DTMs [y] or just quit the program [n]?\n")

        if answer == 'y' or answer == 'Y':
            break

        elif answer == 'n' or answer == 'N':
            break

        else:
            print('Incorrect answer. Try again...\n')
            continue

    if answer == 'y' or answer == 'Y':
        print('\n')
        continue

    elif answer =='n' or answer == 'N':
        print('\n')
        break

# press any key to exit:
input('Press any key to exit...')