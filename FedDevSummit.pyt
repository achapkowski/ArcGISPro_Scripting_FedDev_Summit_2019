"""
    @owner: Andrew Chapkowski
    @date: 1/8/2019
    @description: This toolbox will provide logic for buffering data
    @contact: achapkowski@esri.com
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

import arcpy
from arcpy import env

logname = "buffertool.logger"
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(logname)
log.setLevel(logging.DEBUG)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "My Amazing Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [BufferTool]


class BufferTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Buffer Tool"
        self.description = "This tool will buffer a feature class."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        in_fc = arcpy.Parameter(
            name='in_features', # unique
            displayName='Input Features',
            datatype='GPFeatureLayer',
            direction='Input',
            parameterType='Required')

        lu = arcpy.Parameter(name='lu',
                             displayName="Distance",
                             datatype="GPLinearUnit",
                             direction="Input",
                             parameterType="Required")
        lu.value = "100 Meters"

        out_fc = arcpy.Parameter(name="outfc", displayName="Buffered Results",
                                 datatype="DEFeatureClass",
                                 direction="Output",
                                 parameterType="Derived")
        params = [in_fc, lu, out_fc]

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
        if parameters[1].value == "100 Meters":
            parameters[1].setWarningMessage("This is the default value!")
        return

    def execute(self, parameters, messages):
        """
        This tool performs our buffer logic.

        The source code of the tool.

        """

        fh = RotatingFileHandler("./log.txt", mode='a',
                                 maxBytes=2*1024*1024, backupCount=3,
                                 encoding=None, delay=0)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        log.addHandler(fh)
        #   Inputs
        #
        in_fc = parameters[0].valueAsText
        distance = parameters[1].valueAsText
        #  Local Variables
        #
        out_fc = os.path.join(env.scratchGDB, "buffer")
        #  Setting Environmental Variables
        #
        env.overwriteOutput = True
        #  Logic
        #
        try:
            log.debug("Entering analysis")

            out_fc = arcpy.analysis.Buffer(in_fc, out_fc, distance)[0]
            log.debug("analysis finished")
            log.debug("returning results")
            arcpy.SetParameterAsText(2, out_fc)
        except arcpy.ExecuteError as ae:
            log.error(ae)
            arcpy.AddError(ar)
        except Exception as e:
            log.error(e)
            arcpy.AddError(e)
        finally:
            logging.shutdown()
        return
