import arcpy,sys,os
arcpy.env.overwriteOutput = True

cityManholes = arcpy.GetParameterAsText(0) # the city's GIS manhole feature class
surveyedManholes = arcpy.GetParameterAsText(1) # the surveyed manhole feature class
containsZ1MHA = arcpy.GetParameter(2) # if the data submittal has newly found assets IDs

workspace = os.path.dirname(os.path.dirname(cityManholes)) # must set a workspace for the edit session - use the location of the Checkout database
arcpy.AddMessage('Editting database location ' + workspace)

edit = arcpy.da.Editor(workspace) #set workspace to have an edit session
edit.startEditing(False,True) #start without a redo/undo stack for versioned data, more efficient
edit.startOperation() #start editting

invertBoolean = arcpy.GetParameter(3) # used for customized attributes
invertElevationBoolean = arcpy.GetParameter(4) # used for customized attributes
rimElevationBoolean = arcpy.GetParameter(5) # used for customized attributes
rimToGradeBoolean = arcpy.GetParameter(6) # used for customized attributes
lifeCycleBoolean = arcpy.GetParameter(7) # used for customized attributes
GPSDateBoolean = arcpy.GetParameter(8) # used for customized attributes
dataSourceBoolean = arcpy.GetParameter(9) # used for customized attributes

fields = ['FACILITYID', 'INVERT', 'INVERTELEV', 'RIMELEV', 'RIMTOGRADE', 'LIFECYCLESTATUS', 'GPSDATE', 'DATASOURCE', 'LEGACYMHASSETID'] # field names to be used for the cursors

if not invertBoolean and not invertElevationBoolean and not rimElevationBoolean and not rimToGradeBoolean and not lifeCycleBoolean and not GPSDateBoolean and not dataSourceBoolean and not containsZ1MHA: # none of the customized attributes were checked
    arcpy.AddMessage('Must specify fields to update!')
    sys.exit()

surveyedManholeTuple = arcpy.da.SearchCursor(surveyedManholes, fields) # save the search cursor of the surveyed manholes to a tuple

if (invertBoolean or invertElevationBoolean or rimElevationBoolean or rimToGradeBoolean or lifeCycleBoolean or GPSDateBoolean or dataSourceBoolean) and not containsZ1MHA: # if any of the customized attributes return a true value and there are no newly discovered manholes , the user wants customized attributes to be transferred
    arcpy.AddMessage("Updating customized attributes.")

    with arcpy.da.UpdateCursor(cityManholes, fields) as cursor: # create an update cursor to update the city's manhole feature class
        for cityRow in cursor:

            for surveyedManhole in surveyedManholeTuple: # use a for loop to loop through each surveyed manhole to find a match to the current row in the city's manhole feature class

                surveyedManholeFacilityID = surveyedManhole[0] # Grab the attribute data from the surveyed manhole row in the search cursor tuple and save it to variables
                surveyedManholeInvert = surveyedManhole[1] # Invert
                surveyedManholeInvertElev = surveyedManhole[2] # Invert Elevation
                surveyedManholeRimElev = surveyedManhole[3] # Rim Elevation
                surveyedManholeRimToGrade = surveyedManhole[4] # Rim To Grade
                surveyedManholeLifecycleStatus = surveyedManhole[5] # Lifecyclestatus
                surveyedManholeGPSDate = surveyedManhole[6] # GPS Date
                surveyedManholeDataSource = surveyedManhole[7] # Data source

                if cityRow[0] == surveyedManholeFacilityID: # see if the facility IDs match from the survey and city. Update attribute field values only if the survey data is not null!!!

                    if surveyedManholeInvert != None and surveyedManholeInvert != 0 and invertBoolean: # Invert, make sure that customized attribute returns a true value to update it.

                        cityRow[1] = surveyedManholeInvert
                        cursor.updateRow(cityRow)

                    if surveyedManholeInvertElev != None and surveyedManholeInvertElev != 0 and invertElevationBoolean:  #Invert Elevation

                        cityRow[2] = surveyedManholeInvertElev
                        cursor.updateRow(cityRow)

                    if surveyedManholeRimElev != None and surveyedManholeRimElev != 0 and rimElevationBoolean:  #Rim Elevation

                        cityRow[3] = surveyedManholeRimElev
                        cursor.updateRow(cityRow)

                    if surveyedManholeRimToGrade != None and rimToGradeBoolean:  #Rim to Grade

                        cityRow[4] =  surveyedManholeRimToGrade
                        cursor.updateRow(cityRow)

                    if surveyedManholeLifecycleStatus != None and lifeCycleBoolean:  # Life Cycle Status

                        cityRow[5] = surveyedManholeLifecycleStatus
                        cursor.updateRow(cityRow)

                    if surveyedManholeGPSDate != None and surveyedManholeGPSDate != 0 and GPSDateBoolean:  # GPS Date

                        cityRow[6] = surveyedManholeGPSDate
                        cursor.updateRow(cityRow)

                    if surveyedManholeDataSource != None and dataSourceBoolean:  # Data source

                        cityRow[7] = surveyedManholeDataSource
                        cursor.updateRow(cityRow)

            surveyedManholeTuple.reset() # reset the search cursor tuple so the search can continue on the next City Row

    arcpy.AddMessage("Finished")
    edit.stopOperation()
    edit.stopEditing(True) #stop the edit session and save edits


if containsZ1MHA: # update the newly found assets

    surveyedManholeTuple.reset() # reset the search cursor tuple again, just in case.

    if (invertBoolean or invertElevationBoolean or rimElevationBoolean or rimToGradeBoolean or lifeCycleBoolean or GPSDateBoolean or dataSourceBoolean) and containsZ1MHA: # if any of the customized fields return a true value and there are MHA/ MHZ1 manholes , the user wants customized attributes to be transferred
        arcpy.AddMessage("Updating selected fields for the newly discovered assets.")

        with arcpy.da.UpdateCursor(cityManholes, fields) as cursor2: #similar to a for loop within a for loop
            for cityRow in cursor2:

               for surveyedManhole in surveyedManholeTuple:

                   surveyedManholeFacilityID = surveyedManhole[0] # Grab the attribute data from the surveyed manhole row in the search cursor tuple and save it to variables.
                   surveyedManholeInvert = surveyedManhole[1] # Invert
                   surveyedManholeInvertElev = surveyedManhole[2] # Invert
                   surveyedManholeRimElev = surveyedManhole[3] # Rim Elevation
                   surveyedManholeRimToGrade = surveyedManhole[4] # Rim To Grade
                   surveyedManholeLifecycleStatus = surveyedManhole[5] # Lifecyclestatus
                   surveyedManholeGPSDate = surveyedManhole[6] # GPS Date
                   surveyedManholeDataSource = surveyedManhole[7] # Data source

                   if cityRow[8] == surveyedManholeFacilityID: # see if the facility IDs match from the survey manhole and city's Legacy MH Asset ID field. Update attribute field values only if the survey data is not null!!!

                       if surveyedManholeInvert != None and surveyedManholeInvert != 0 and invertBoolean: # Invert, make sure that customized attribute specified by the user returns a true value to update it.

                           cityRow[1] = surveyedManholeInvert
                           cursor2.updateRow(cityRow)

                       if surveyedManholeInvertElev != None and surveyedManholeInvertElev != 0 and invertElevationBoolean:  #Invert Elevation

                           cityRow[2] = surveyedManholeInvertElev
                           cursor2.updateRow(cityRow)

                       if surveyedManholeRimElev != None and surveyedManholeRimElev != 0 and rimElevationBoolean:  #Rim Elevation

                           cityRow[3] = surveyedManholeRimElev
                           cursor2.updateRow(cityRow)

                       if surveyedManholeRimToGrade != None and rimToGradeBoolean:  #Rim to Grade

                           cityRow[4] =  surveyedManholeRimToGrade
                           cursor2.updateRow(cityRow)

                       if surveyedManholeLifecycleStatus != None and lifeCycleBoolean:  # Life Cycle Status

                           cityRow[5] = surveyedManholeLifecycleStatus
                           cursor2.updateRow(cityRow)

                       if surveyedManholeGPSDate != None and surveyedManholeGPSDate != 0 and GPSDateBoolean:  # GPS Date

                           cityRow[6] = surveyedManholeGPSDate
                           cursor2.updateRow(cityRow)

                       if surveyedManholeDataSource != None and dataSourceBoolean:  # Data source

                           cityRow[7] = surveyedManholeDataSource
                           cursor2.updateRow(cityRow)

               surveyedManholeTuple.reset() # reset the cursor so the search can continue on the next City Row

        arcpy.AddMessage("Finished")
        edit.stopOperation()
        edit.stopEditing(True) #stop the edit session and save edits

sys.exit()
