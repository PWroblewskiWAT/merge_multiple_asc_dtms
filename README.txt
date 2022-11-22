merge_multiple_asc_dtms program contains two *.py files:
	merge_multiple_asc_dtms.py - script to execute
	merge_multiple_asc_dtms_fncts.py - script containing all of the functions, classes and methods, used by merge_multiple_asc_dtms.py

After running the merge_multiple_asc_dtms.py, the user will be asked to specify
	a) path to CATALOGS:
		- input catalog - for example: "C:\Users\user01\data_processing\dtms_merging\input"
		- output catalog - for example: "C:\Users\user01\data_processing\dtms_merging\input"
	b) number corresponding to a header structure of input files. To select the correct option, the user should check for header components' names in asc files.

After that, the script is going to be executed, and the user will see some informations about the sequentially performed processes:
	- 'Loading datasets...'
	- 'Calculating statistics for datasets...'
	- 'Checking the spatial distribution of datasets...'
	- 'Sorting datasets by Y (descending) & by X (ascending)...'
	- 'Searching for tiles with max X & max Y coordinates...'
	- 'Preparing final DTM structure...'
	- 'Merging DTMs...'
	- 'Creating a header for merged DTM...'
	- 'Exporting final DTM as *.asc file...'

After the full execution of data processing part, the program will ask if User wants to merge another set of DTMs or exit the program:
	- "Would You like to merge another set of DTMs [y] or just quit the program [n]?"

There are two correct answers for the question mentioned above: 'y'/'Y' or 'n'/'N'. After selecting 'y'/'Y', the data processing part of the program 
will execute one more time. After selecting 'n'/'N' the program execution will end and the following information will appear:
	-'Press any key to exit...'

After that, pressing any key will close the terminal window.


NOTE:
Program execution successfully tested using Python 3.9.12 & Python 3.10.6