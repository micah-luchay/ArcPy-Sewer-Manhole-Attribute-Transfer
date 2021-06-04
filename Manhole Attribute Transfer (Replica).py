import arcpy,sys,os
arcpy.env.overwriteOutput = True

cityManholes = arcpy.GetParameterAsText(0) # the city's GIS data
surveyedManholes = arcpy.GetParameterAsText(1) # surveyed GIS data
containsZ1MHA = arcpy.GetParameter(2) # if the data submittal has newly found assets IDs

workspace = os.path.dirname(os.path.dirname(cityManholes)) # must set a workspace for the edit session - use the location of the Checkout database
arcpy.AddMessage('Editting database location ' + workspace)

# workspace = arcpy.env.workspace = r'C:\Users\luchaymm\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\CW2020_Master_OSA@CLBCWPSQL001_Luchay_Version.sde' #set a workspace for SQL server connection

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

fields = ['FACILITYID', 'INVERT', 'INVERTELEV', 'RIMELEV', 'RIMTOGRADE', 'LIFECYCLESTATUS', 'GPSDATE', 'DATASOURCE', 'LEGACYMHASSETID']

if not invertBoolean and not invertElevationBoolean and not rimElevationBoolean and not rimToGradeBoolean and not lifeCycleBoolean and not GPSDateBoolean and not dataSourceBoolean and not containsZ1MHA: #none of the customized attributes were checked
    arcpy.AddMessage('Must specify fields to update!')
    sys.exit()

surveyedManholeTuple = arcpy.da.SearchCursor(surveyedManholes, fields) # save the search cursor of the surveyed manholes to a tuple

if (invertBoolean or invertElevationBoolean or rimElevationBoolean or rimToGradeBoolean or lifeCycleBoolean or GPSDateBoolean or dataSourceBoolean) and not containsZ1MHA: # if any of the customized attributes return a true value and there are no MHA/ MHZ1 manholes , the user wants customized attributes to be transferred
    arcpy.AddMessage("Updating customized attributes.")

    with arcpy.da.SearchCursor(surveyedManholes, fields) as cursor: #similar to a for loop within a for loop
        for surveyRow in cursor:

            surveyManholeID = str(surveyRow[0]) # grab the FacilityID of the current surveyed Manhole in the loop to use to query the City Manhole FC for a faster edit

            with arcpy.da.UpdateCursor(cityManholes, fields, where_clause = "\"FACILITYID\" = " + "'" + surveyManholeID + "'") as cursor2:
                for cityRow in cursor2:

                    if cityRow[0] == surveyRow[0]: # see if the facility IDs match from the survey and city. Update attribute field values only if the survey data is not null!!!

                        if surveyRow[1] != None and surveyRow[1] != 0 and invertBoolean: # Invert, make sure that customized attribute returns a true value to update it.

                            cityRow[1] = surveyRow[1]
                            cursor2.updateRow(cityRow)

                        if surveyRow[2] != None and surveyRow[2] != 0 and invertElevationBoolean:  #Invert Elevation

                            cityRow[2] = surveyRow[2]
                            cursor2.updateRow(cityRow)

                        if surveyRow[3] != None and surveyRow[3] != 0 and rimElevationBoolean:  #Rim Elevation

                            cityRow[3] = surveyRow[3]
                            cursor2.updateRow(cityRow)

                        if surveyRow[4] != None and rimToGradeBoolean:  #Rim to Grade

                            cityRow[4] = surveyRow[4]
                            cursor2.updateRow(cityRow)

                        if surveyRow[5] != None and lifeCycleBoolean:  # Life Cycle Status

                            cityRow[5] = surveyRow[5]
                            cursor2.updateRow(cityRow)

                        if surveyRow[6] != None and surveyRow[6] != 0 and GPSDateBoolean:  # GPS Date

                            cityRow[6] = surveyRow[6]
                            cursor2.updateRow(cityRow)

                        if surveyRow[7] != None and dataSourceBoolean:  # Data source

                            cityRow[7] = surveyRow[7]
                            cursor2.updateRow(cityRow)

    arcpy.AddMessage("Finished")
    edit.stopOperation()
    edit.stopEditing(True) #stop the edit session and save edits
    sys.exit()


if containsZ1MHA: # update the newly found assets

    fields = ['FACILITYID', 'INVERT', 'INVERTELEV', 'RIMELEV', 'RIMTOGRADE', 'LIFECYCLESTATUS', 'GPSDATE', 'DATASOURCE', 'LEGACYMHASSETID']

    if invertBoolean or invertElevationBoolean or rimElevationBoolean or rimToGradeBoolean or lifeCycleBoolean or GPSDateBoolean or dataSourceBoolean and containsZ1MHA: # if any of the customized attributes return a true value and there are MHA/ MHZ1 manholes , the user wants customized attributes to be transferred
        arcpy.AddMessage("Updating selected fields for the newly discovered assets.")

        with arcpy.da.SearchCursor(surveyedManholes, fields) as cursor: #similar to a for loop within a for loop
            for surveyRow in cursor:

                surveyManholeID = str(surveyRow[0]) # grab the FacilityID of the current surveyed Manhole in the loop to use to query the City Manhole FC for a faster edit

                with arcpy.da.UpdateCursor(cityManholes, fields, where_clause = "\"LEGACYMHASSETID\" = " + "'" + surveyManholeID + "'") as cursor2:
                    for cityRow in cursor2:

                        if cityRow[8] == surveyRow[0]: # see if the LEGACYMHASSETID from the city matches the FacilityID from the contractor. Update attribute field values only if the survey data is not null!!!

                            if surveyRow[1] != None and surveyRow[1] != 0 and invertBoolean: # Invert, make sure that customized attribute returns a true value to update it.

                                cityRow[1] = surveyRow[1]
                                cursor2.updateRow(cityRow)

                            if surveyRow[2] != None and surveyRow[2] != 0 and invertElevationBoolean:  #Invert Elevation

                                cityRow[2] = surveyRow[2]
                                cursor2.updateRow(cityRow)

                            if surveyRow[3] != None and surveyRow[3] != 0 and rimElevationBoolean:  #Rim Elevation

                                cityRow[3] = surveyRow[3]
                                cursor2.updateRow(cityRow)

                            if surveyRow[4] != None and rimToGradeBoolean:  #Rim to Grade

                                cityRow[4] = surveyRow[4]
                                cursor2.updateRow(cityRow)

                            if surveyRow[5] != None and lifeCycleBoolean:  # Life Cycle Status

                                cityRow[5] = surveyRow[5]
                                cursor2.updateRow(cityRow)

                            if surveyRow[6] != None and surveyRow[6] != 0 and GPSDateBoolean:  # GPS Date

                                cityRow[6] = surveyRow[6]
                                cursor2.updateRow(cityRow)

                            if surveyRow[7] != None and dataSourceBoolean:  # Data source

                                cityRow[7] = surveyRow[7]
                                cursor2.updateRow(cityRow)
        arcpy.AddMessage("Finished")
        edit.stopOperation()
        edit.stopEditing(True) #stop the edit session and save edits
        sys.exit()


