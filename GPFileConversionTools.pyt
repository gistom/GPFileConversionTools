import arcpy, os, zipfile


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "File Conversion Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [CsvToTable, ZipShapeFileToFC]


class CsvToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "CSV to Table"
        self.description = "Converts a CSV file to a table"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramInCsvFile = arcpy.Parameter(
            displayName='CSV File',
            name='in_csvFile',
            datatype='DEFile',
            parameterType='Required',
            direction='Input')
        paramInCsvFile.filter.list = ['csv']
        paramOutTable = arcpy.Parameter(
            displayName='Output Table',
            name='out_csvTable',
            datatype='DETable',
            parameterType='Required',
            direction='Output')
        params = [paramInCsvFile, paramOutTable]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputCSV = parameters[0].valueAsText
        outputTable = parameters[1].valueAsText
        outPathTuple = os.path.split(outputTable)
        arcpy.TableToTable_conversion(inputCSV, outPathTuple[0], outPathTuple[1], None)
        return

class ZipShapeFileToFC(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ZIP Shapefile to Feature Class"
        self.description = "Convert a ZIP file with one ShapeFile into a feature class"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramInZipFile = arcpy.Parameter(
            displayName='ZIP File',
            name='in_zipFile',
            datatype='DEFile',
            parameterType='Required',
            direction='Input')
        paramUnzipFolder = arcpy.Parameter(
            displayName='Unzip Folder',
            name='out_zipfolder',
            datatype='DEFolder',
            parameterType='Required',
            direction='Output')
        paramOutFC = arcpy.Parameter(
            displayName='Output Feature Class',
            name='out_FeatureClass',
            datatype='DEFeatureClass',
            parameterType='Derived',
            direction='Output')
        params = [paramInZipFile, paramUnzipFolder, paramOutFC]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputZIP = parameters[0].valueAsText
        outputFolder = parameters[1].valueAsText
        shapeFileName = ''
        with zipfile.ZipFile(inputZIP, 'r') as zip_ref:
            listOfFileNames = zip_ref.namelist()
            for fileName in listOfFileNames:
                if fileName.endswith('.shp'):
                    shapeFileName = fileName
                    break
            zip_ref.extractall(outputFolder)
        fullShapePath = os.path.join(outputFolder, shapeFileName)
        arcpy.SetParameterAsText(2, fullShapePath)

        return