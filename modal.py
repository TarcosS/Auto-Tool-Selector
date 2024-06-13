import adsk.core, adsk.fusion, adsk.cam, traceback
app = adsk.core.Application.get()
ui = app.userInterface
    
class Modal:
    def __init__(self):
        self.handlers = []
        self.selectedFace = None

    def createModal(self):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface

            # Command Definition oluşturma
            cmdDef = ui.commandDefinitions.itemById('MyModalCommand')
            if not cmdDef:
                cmdDef = ui.commandDefinitions.addButtonDefinition('MyModalCommand', 'My Modal', 'Select face and set process parameters')

            # Command Created event handler oluşturma
            onCommandCreated = CommandCreatedHandler(self)
            cmdDef.commandCreated.add(onCommandCreated)
            self.handlers.append(onCommandCreated)

            # Command başlatma
            inputs = adsk.core.NamedValues.create()
            cmdDef.execute(inputs)

        except:
            if ui:
                ui.messageBox('Failed to create modal:\n{}'.format(traceback.format_exc()))

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, modal):
        super().__init__()
        self.modal = modal

    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = eventArgs.command
            inputs = cmd.commandInputs

            # Input alanları ekleme
            # inputs.addTextBoxCommandInput('textBoxInput', 'Enter text:', '', 1, False)
            faceInput = inputs.addSelectionInput('faceSelection', 'Select Face', 'Select the face to be machined')
            faceInput.addSelectionFilter(adsk.core.SelectionCommandInput.PlanarFaces)
            faceInput.setSelectionLimits(1, 1)

            # OK ve Cancel button'ları ekleme
            onExecute = CommandExecuteHandler(self.modal)
            cmd.execute.add(onExecute)
            self.modal.handlers.append(onExecute)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            if ui:
                ui.messageBox('Failed to create command inputs:\n{}'.format(traceback.format_exc()))

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, modal):
        super().__init__()
        self.modal = modal

    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            inputs = eventArgs.command.commandInputs

            # textValue = inputs.itemById('textBoxInput').text
            # numericValue = inputs.itemById('valueInput').value
            # faceSelection = inputs.itemById('faceSelection')



            app = adsk.core.Application.get()
            ui = app.userInterface

            # createProcess fonksiyonunu burada çalıştırma
            createProcess(1)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            if ui:
                ui.messageBox('Failed to execute command:\n{}'.format(traceback.format_exc()))

def createProcess(selectedFace):
    try:
        #################### Find tools in sample tool library ####################
        # get the tool libraries from the library manager
        camManager = adsk.cam.CAMManager.get()
        libraryManager = camManager.libraryManager
        toolLibraries = libraryManager.toolLibraries
        
        showMessage('=============================================')
        showMessage('Creating Manufacturing Model...')
        # we can use a library URl directly if we know its address (here we use Fusion's Metric sample library)
        url = adsk.core.URL.create('systemlibraryroot://Samples/Turning Tools (Metric).json')
        
        # load tool library 
        toolLibrary = toolLibraries.toolLibraryAtURL(url)

        # create some variables for the milling tools which will be used in the operations
        faceTool = None
        turningTool = None
        groovingTool = None

        # searching the face mill and the bull nose using a loop for the roughing operations
        for tool in toolLibrary:
            # read the tool type
            toolType = tool.parameters.itemByName('tool_type').value.value 
            # select the first face tool found
            if toolType == 'turning general' and tool.parameters.itemByName('tool_hand').value.value == 'R' and not turningTool:
                faceTool = tool
                turningTool = tool  
            elif toolType == 'turning grooving' and tool.parameters.itemByName('tool_holderType').value.value == 'groove external' and  not groovingTool:
                # for i in range(tool.parameters.count):
                #     param = tool.parameters.item(i)
                #     if param:
                #         try:
                #             showMessage(param.name + ': ' + str(param.value.value))
                #         except:
                #             showMessage(param.name + ': ' + 'Error')
                groovingTool = tool
            # exit when the 2 tools are found
            if turningTool and groovingTool:
                break

        #################### create setup ####################
        # get the CAM product
        doc = app.activeDocument
        products = doc.products
        cam = adsk.cam.CAM.cast(products.itemByProductType("CAMProductType"))
      
        setups = cam.setups
        setupInput = setups.createInput(adsk.cam.OperationTypes.TurningOperation)
        # create a list for the models to add to the setup Input
        models = [] 
        part = cam.designRootOccurrence.bRepBodies.item(0)
        # add the part to the model list
        models.append(part) 
        # pass the model list to the setup input
        setupInput.models = models 
        # create the setup
        setup = setups.add(setupInput) 
            
        # change some properties of the setup
        setup.name = 'CAM Basic Script Sample'  
        setup.stockMode = adsk.cam.SetupStockModes.RelativeCylinderStock
        # set offset mode
        setup.parameters.itemByName('job_stockOffsetMode').expression = "'simple'"
        # set offset stock side
        setup.parameters.itemByName('job_stockOffsetSides').expression = '5 mm'
        # set offset stock top
        # setup.parameters.itemByName('job_stockOffsetTop').expression = '2 mm'
        # set setup origin
        setup.parameters.itemByName('wcs_origin_boxPoint').value.value = 'top 1'
                
        #################### face operation ####################
        # create a face operation input
        faceInput = setup.operations.createInput('turning_face')
        faceInput.tool = faceTool
        faceInput.displayName = 'Face Operation'       
        # input.parameters.itemByName('tolerance').expression = '0.01 mm'
        # input.parameters.itemByName('stepover').expression = '0.75 * tool_diameter'
        # input.parameters.itemByName('direction').expression = "'climb'"
        
        #################### turning operation ####################
        # create a turning operation input
        turningInput = setup.operations.createInput('turning_profile_roughing')
        turningInput.tool = turningTool
        turningInput.displayName = 'Turning Operation'       
        # input.parameters.itemByName('tolerance').expression = '0.01 mm'
        # input.parameters.itemByName('stepover').expression = '0.75 * tool_diameter'
        # input.parameters.itemByName('direction').expression = "'climb'"

        #################### turning operation ####################
        # create a turning operation input
        grooveInput = setup.operations.createInput('turning_groove_roughing')
        grooveInput.tool = groovingTool
        grooveInput.displayName = 'Groove Operation'       
        # input.parameters.itemByName('tolerance').expression = '0.01 mm'
        # input.parameters.itemByName('stepover').expression = '0.75 * tool_diameter'
        # input.parameters.itemByName('direction').expression = "'climb'"
        
        # add the operation to the setup
        faceOp = setup.operations.add(faceInput)
        turningOp = setup.operations.add(turningInput)
        grooveOp = setup.operations.add(grooveInput)

        ##################### generate operations ####################
        cam.generateToolpath(faceOp)            
        cam.generateToolpath(turningOp)            
        cam.generateToolpath(grooveOp)         

    except:
        if ui:
            ui.messageBox('Failed to create process:\n{}'.format(traceback.format_exc()))

def showMessage(message):
    app.log(message)

    # Give control back to Fusion, so it can update the UI.
    adsk.doEvents()