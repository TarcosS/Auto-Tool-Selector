# button.py
import adsk.core
import adsk.fusion
import adsk.cam
import traceback

_handlers = []  # Olay işleyicilerini saklamak için global bir liste

class Button:
    def __init__(self):
        self.handlers = []

    def createButton(self, commandId, commandName, commandDescription, commandResources, workspaceId, panelId):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface

            cmdDef = ui.commandDefinitions.itemById(commandId)
            if not cmdDef:
                cmdDef = ui.commandDefinitions.addButtonDefinition(
                    commandId, commandName, commandDescription, commandResources)
                
            workspace = ui.workspaces.itemById(workspaceId)
            panel = workspace.toolbarPanels.itemById(panelId)
            
            # Butonu ekle ve sabitle
            control = panel.controls.itemById(commandId)
            if not control:
                control = panel.controls.addCommand(cmdDef)
            
            control.isPromoted = True  # Butonu araç çubuğuna sabitleyin
            control.isPromotedByDefault = True  # Varsayılan olarak sabitli olmasını sağlayın

            onCommandCreated = ButtonCommandCreatedHandler()
            cmdDef.commandCreated.add(onCommandCreated)
            _handlers.append(onCommandCreated)

        except:
            if ui:
                ui.messageBox('Failed to create button:\n{}'.format(traceback.format_exc()))

class ButtonCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            cmd = adsk.core.Command.cast(args.command)
            onExecute = ButtonCommandExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
        except:
            if ui:
                ui.messageBox('Failed to create command event handler:\n{}'.format(traceback.format_exc()))

class ButtonCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            # Modal'ı tetikleyin
            from .modal import Modal
            modal = Modal()
            modal.createModal()
        except:
            ui = adsk.core.Application.get().userInterface
            if ui:
                ui.messageBox('Failed to execute command:\n{}'.format(traceback.format_exc()))
