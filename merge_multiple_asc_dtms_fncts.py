#!/usr/bin/env python
# coding: utf-8

# import necessary modules
from operator import itemgetter
from math import *
import numpy as np
import time
import os


def askUserForPath(inOrOut='input'):
    """
    Args:
        inOrOut - String specifying whether we want to obtain input or output catalog path ('input' by default)

    Returns:
        inputCatalog - String storing input/output catalog path
    """
    while True:
        inputCatalog = input(
            "Enter the path to the catalog, where all of the DTMs that You'd like to merge are stored:\n") \
            if inOrOut == 'input' else input(
            "Enter the path to the catalog, where You'd like to save merged DTM *.asc file:\n")

        if inputCatalog.startswith('"') or inputCatalog.startswith("'"):
            inputCatalog = inputCatalog[1:]

        if inputCatalog.endswith('"') or inputCatalog.endswith("'"):
            inputCatalog = inputCatalog[:-1]

        if not (os.path.exists(inputCatalog) and os.path.isdir(inputCatalog)):
            print("The path You've entered leads to a catalog that does not exist. Try again!\n")
            continue

        else:
            time.sleep(.5)
            print('\n')
            break

    return inputCatalog


class MergeAscDtms():


    def __init__(self, inputCatalog, outputCatalog, dataSep = ' ', outputFileName = 'merged_dtm.asc'):
        """
        Args:
            dataSep - String - data separator to be used while loading and exporting datasets (' ' by default)
            outputFileName - String - name of the output DTM - should contain '*.asc' extension ('merged_dtm.asc' by default)
        """
        self.inputCatalog = inputCatalog
        self.outputCatalog = outputCatalog
        self.dataSep = dataSep
        self.outputFileName = outputFileName


    def loadSingleAscDtm(self, path):
        """
        Args:
            path - String, which is specifying the full file path to the *.asc DTM file
        Returns:
            header - dictionary filled with informations stored in a header part of an input *.asc DTM file
            dtm - np.array() with a (nrows, ncols) shape, storing terrain heights (float values for appropriate heights,
                int values for nodata_value)
        """
        headerComponents = ['ncols', 'nrows', 'xllcenter', 'yllcenter', 'cellsize', 'nodata_value']

        with open(path, 'r') as f:

            counter = 0
            header = {}
            dtm = []

            for l in f:

                if l.endswith('\n'):
                    l = l[:l.index('\n')]

                l = l.split(f'{self.dataSep}')

                if counter < 6:

                    if any(map(lambda x: x in headerComponents, l)):
                        counter += 1

                        try:
                            header[l[0]] = int(l[1])

                        except:
                            header[l[0]] = float(l[1])

                else:
                    heights = []

                    for el in l:

                        try:
                            heights.append(int(el))

                        except:
                            heights.append(float(el))

                    dtm.append(heights)

        return header, np.array(dtm)


    def loadMultipleAscDtms(self):
        """
        Returns:
            headers - nested dictionary, storing multiple 'header' dictionaries, obtained with loadSingleAscDtm() function as values,
                and file names as keys.
            dtms - nested dictionary, storing multiple 'dtm' np.arrays(), obtained with loadSingleAscDtm() function as values,
                and file names as keys.
        """
        print('Loading datasets...')

        headers = {}
        dtms = {}

        for i, file in enumerate(os.listdir(self.inputCatalog)):

            if file.endswith('.asc'):
                print(f'Loading dataset #{i + 1} - {file}')
                header, dtm = self.loadSingleAscDtm(os.path.join(self.inputCatalog, file))
                headers[file[:file.index('.')]] = header
                dtms[file[:file.index('.')]] = dtm

        return headers, dtms


    def findStatisticsForDatasets(self, headers):
        """
        Args:
            headers - nested dictionary, storing multiple 'header' dictionaries, obtained with loadSingleAscDtm() function
                as values, and file names as keys.
        Returns:
            statistics - dictionary, which is storing some statistics informations about mean columns number, mean rows
                number, mean cell size, min/max X, min/max Y and nodata_value, calculated using all of the datasets that
                are being processed.
        """
        print('Calculating statistics for datasets...\n')
        time.sleep(.5)

        return {
            'mean cols num': int(np.mean([v['ncols'] for v in headers.values()])),
            'mean rows num': int(np.mean([v['nrows'] for v in headers.values()])),
            'mean cell size': int(np.mean([v['cellsize'] for v in headers.values()])),
            'min X': min([v['xllcenter'] for v in headers.values()]),
            'max X': max([v['xllcenter'] for v in headers.values()]),
            'min Y': min([v['yllcenter'] for v in headers.values()]),
            'max Y': max([v['yllcenter'] for v in headers.values()]),
            'no data': int(np.mean([v['nodata_value'] for v in headers.values()]))
        }


    def findSpatialDistributionOfDatasets(self, statistics):
        """
        Args:
            statistics - dictionary, which is storing some statistics informations about mean columns number, mean rows
                number, mean cell size, min/max X, min/max Y and nodata_value, calculated using all of the datasets that
                are being processed.
        Returns:
            numOfDatasetsAlongX - int - number of datasets which are spatially distributed along X axis (how many datasets
                there are placed along X axis)
            numOfDatasetsAlongY - int - number of datasets which are spatially distributed along Y axis (how many datasets
                there are placed along Y axis)
        """
        print('Checking the spatial distribution of datasets...\n')
        time.sleep(.5)

        numOfDatasetsAlongX = int(
            round((statistics['max X'] - statistics['min X']) / statistics['mean rows num'] * statistics['mean cell size'],
                  0)) + 1
        numOfDatasetsAlongY = int(
            round((statistics['max Y'] - statistics['min Y']) / statistics['mean cols num'] * statistics['mean cell size'],
                  0)) + 1
        return numOfDatasetsAlongX, numOfDatasetsAlongY


    def sortDatasets(self, headers, numOfDatasetsAlongX):
        """
        Args:
            headers - nested dictionary, storing multiple 'header' dictionaries, obtained with loadSingleAscDtm() function
                as values, and file names as keys.
            numOfDatasetsAlongX - int - number of datasets which are spatially distributed along X axis (how many datasets
                there are placed along X axis)
        Returns:
            sortedDatasets - np.array() storing lists of Strings, where each list was created by sorting datasets by Y
                coordinates (descending) and the order of the Strings on each list is corresponding with the result of
                sorting X coordinates (ascending)
        """
        print('Sorting datasets by Y (descending) & by X (ascending)...\n')
        time.sleep(.5)

        sortedByY = list(zip([k for k in headers.keys()], [v['xllcenter'] for v in headers.values()],
                             [v['yllcenter'] for v in headers.values()]))
        sortedByY.sort(key=itemgetter(2), reverse=True)

        splittedBySimilarY = [sortedByY[i: i + numOfDatasetsAlongX] for i in range(0, len(sortedByY), numOfDatasetsAlongX)]

        sortedByXY = []

        for i in range(len(splittedBySimilarY)):
            splittedBySimilarY[i].sort(key=itemgetter(1), reverse=False)

            tmp = []

            for j in range(len(splittedBySimilarY[i])):
                tmp.append(splittedBySimilarY[i][j][0])
            sortedByXY.append(tmp)

        return np.array(sortedByXY)


    def findTilesWithMaxCoords(self, headers):
        """
        Args:
            headers - nested dictionary, storing multiple 'header' dictionaries, obtained with loadSingleAscDtm() function
                as values, and file names as keys.
        Returns:
            xMaxTile - String - file name of the dataset with max X coordinate
            yMaxTile - String - file name of the dataset with max Y coordinate
        """
        print('Searching for tiles with max X & max Y coordinates...\n')
        time.sleep(.5)

        for i, (k, v) in enumerate(headers.items()):

            if i == 0:

                xMax = v['xllcenter']
                xMaxTile = k

                yMax = v['yllcenter']
                yMaxTile = k

            else:

                if v['xllcenter'] > xMax:
                    xMax = v['xllcenter']
                    xMaxTile = k

                if v['yllcenter'] > yMax:
                    yMax = v['yllcenter']
                    yMaxTile = k

        return xMaxTile, yMaxTile


    def createFinalArrayFilledWithNoDataValues(self, statistics, headers, xMaxTile, yMaxTile):
        """
        Args:
            statistics - dictionary, which is storing some statistics informations about mean columns number, mean rows
                number, mean cell size, min/max X, min/max Y and nodata_value, calculated using all of the datasets that
                are being processed.
            headers - nested dictionary, storing multiple 'header' dictionaries, obtained with loadSingleAscDtm() function
                as values, and file names as keys.
            xMaxTile - String - file name of the dataset with max X coordinate
            yMaxTile - String - file name of the dataset with max Y coordinate

        Returns:
            finalDtmArray - np.array() with a specific shape, which was calculated using coordinates substraction and
                'nrows'/'ncols' parameter taken from datasets' headers.
        """
        print('Preparing final DTM structure...\n')
        time.sleep(.5)

        return np.ones((int((statistics['max Y'] - statistics['min Y']) / statistics['mean cell size'] + \
                            headers[yMaxTile]['nrows']),
                        int((statistics['max X'] - statistics['min X']) / statistics['mean cell size'] + \
                            headers[xMaxTile]['ncols'])), dtype=int) * statistics['no data']


    def fillFinalDtmArrayWithData(self, sortedDatasets, headers, statistics, dtms, finalDtmArray):
        """
        Args:
            sortedDatasets - np.array() storing lists of Strings, where each list was created by sorting datasets by Y
                coordinates (descending) and the order of the Strings on each list is corresponding with the result of
                sorting X coordinates (ascending)
            headers - nested dictionary, storing multiple 'header' dictionaries, obtained with loadSingleAscDtm() function
                as values, and file names as keys.
            statistics - dictionary, which is storing some statistics informations about mean columns number, mean rows
                number, mean cell size, min/max X, min/max Y and nodata_value, calculated using all of the datasets that
                are being processed.
            dtms - nested dictionary, storing multiple 'dtm' np.arrays(), obtained with loadSingleAscDtm() function as values,
                and file names as keys.
            finalDtmArray - np.array() with a specific shape, which was calculated using coordinates substraction and
                'nrows'/'ncols' parameter taken from datasets' headers.
        """
        print('Merging DTMs...')
        time.sleep(.5)

        counter = 0

        for i in range(len(sortedDatasets) - 1, -1, -1):
            datasetsOnSimilarY = sortedDatasets[i]

            for j in range(len(datasetsOnSimilarY)):
                curDataset = datasetsOnSimilarY[j]

                print(f'Processing data from dataset #{counter + 1} - {curDataset}')
                counter += 1

                xCur, yCur = headers[curDataset]['xllcenter'], headers[curDataset]['yllcenter']

                xDiff, yDiff = xCur - statistics['min X'], yCur - statistics['min Y']

                xDiffAsCells = int(xDiff / statistics['mean cell size'])
                yDiffAsCells = int(yDiff / statistics['mean cell size'])

                curDtm = dtms[curDataset]

                curRowInFinalDtmArray = -yDiffAsCells - 1

                for k in range(curDtm.shape[0] - 1, -1, -1):
                    curRowInCurDataset = curDtm[k]

                    curColInFinalDtmArray = xDiffAsCells

                    for l in range(len(curRowInCurDataset)):
                        curHeightInCurDataset = curRowInCurDataset[l]

                        if finalDtmArray[curRowInFinalDtmArray][curColInFinalDtmArray] == statistics['no data']:
                            finalDtmArray[curRowInFinalDtmArray][curColInFinalDtmArray] = curHeightInCurDataset

                        curColInFinalDtmArray += 1

                    curRowInFinalDtmArray -= 1


    def constructFinalHeader(self, finalDtmArray, statistics):
        """
        Args:
            finalDtmArray - np.array() with a specific shape, which was calculated using coordinates substraction and
                'nrows'/'ncols' parameter taken from datasets' headers.
            statistics - dictionary, which is storing some statistics informations about mean columns number, mean rows
                number, mean cell size, min/max X, min/max Y and nodata_value, calculated using all of the datasets that
                are being processed.

        Returns:
            finalHeader - dictionary filled with informations which are going to be stored in a header part of an output
                *.asc DTM file. Order of following informations is compatible with header parts of input datasets.
        """
        print('Creating a header for merged DTM...\n')
        time.sleep(.5)

        return {
            'ncols': finalDtmArray.shape[1],
            'nrows': finalDtmArray.shape[0],
            'xllcenter': statistics['min X'],
            'yllcenter': statistics['min Y'],
            'cellsize': statistics['mean cell size'],
            'nodata_value': statistics['no data']
        }


    def exportFinalDtmAsAscFile(self, finalHeader, finalDtmArray):
        """
        Args:
            finalHeader - dictionary filled with informations which are going to be stored in a header part of an output
                *.asc DTM file. Order of following informations is compatible with header parts of input datasets.
            finalDtmArray - np.array() with a specific shape, which was calculated using coordinates substraction and
                'nrows'/'ncols' parameter taken from datasets' headers.
        """
        print('Exporting final DTM as *.asc file...')

        headerComponentsAndValues = list(zip(finalHeader.keys(), finalHeader.values()))

        headerComponentsAndValues = [f'{self.dataSep}'.join(str(el) for el in headerComponentsAndValues[i]) + '\n' for i in
                                     range(len(headerComponentsAndValues))]

        dtmHeights = [f'{self.dataSep}'.join(str(el) for el in finalDtmArray[i]) + '\n' for i in range(finalDtmArray.shape[0])]

        with open(os.path.join(self.outputCatalog, self.outputFileName), 'w') as f:

            for component in headerComponentsAndValues:
                f.write(component)

            for height in dtmHeights:
                f.write(height)