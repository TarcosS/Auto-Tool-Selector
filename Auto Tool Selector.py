import adsk.core, adsk.fusion, adsk.cam, traceback
import os
from .button import Button

app = adsk.core.Application.get()
ui  = app.userInterface
        
def run(context):
    try:
        #################### initialisation #####################
        
        # use existing document, load 2D Strategies model from the Fusion CAM Samples folder
        doc = app.activeDocument

        # Make sure the TEXT COMMAND palette is visible.
        textPalette = ui.palettes.itemById('TextCommands')
        if not textPalette.isVisible:
            textPalette.isVisible = True
            adsk.doEvents()

        doc = app.activeDocument
        products = doc.products
        
        # switch to manufacturing space
        camWS = ui.workspaces.itemById('CAMEnvironment') 
        camWS.activate()

        # Button sınıfını oluştur
        button = Button()

        # Buton detayları
        commandId = 'AutoToolSelectorCommandId1'
        commandName = 'Run Auto Tool Selector'
        commandDescription = 'If you want to use the Auto Tool Selector, click here.'
        commandResources = 'resources/button'  # İkon kullanmak istemiyorsanız boş bırakın
        workspaceId = 'CAMEnvironment'
        panelId = 'CAMScriptsAddinsPanel'

        # Butonu oluştur ve UI'ye ekle
        button.createButton(commandId, commandName, commandDescription, commandResources, workspaceId, panelId)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # UI'den butonu kaldır
        cmdDef = ui.commandDefinitions.itemById('AutoToolSelectorCommandId1111111111')
        if cmdDef:
            cmdDef.deleteMe()

        workspace = ui.workspaces.itemById('CAMEnvironment')
        panel = workspace.toolbarPanels.itemById('CAMScriptsAddinsPanel')
        control = panel.controls.itemById('AutoToolSelectorCommandId1111111111')
        if control:
            control.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed to remove button:\n{}'.format(traceback.format_exc()))

def showMessage(message):
    app.log(message)

    # Give control back to Fusion, so it can update the UI.
    adsk.doEvents()