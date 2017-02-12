import mari
import PySide
import os

class BakeSymmetry(object):

    def __init__(self):
        super(BakeSymmetry, self).__init__()
        self.script_path = self.script_path()

        self.initUI()


    def initUI(self):
        ''' Creating UI and Connections '''

        # Combo Box
        self.comboSymmetryXYZ = PySide.QtGui.QComboBox()
        self.comboSymmetryXYZ.addItem("Off")
        self.comboSymmetryXYZ.addItem("On")
        # grid.addWidget(self.comboSymmetryXYZ,0,0,1)

        # Radio Buttons
        self.x_axis = PySide.QtGui.QRadioButton("X")
        self.y_axis = PySide.QtGui.QRadioButton("Y")
        self.z_axis = PySide.QtGui.QRadioButton("Z")
        self.x_axis.setChecked(True)


        # Add to Toolbar
        toolbar = mari.app.findToolBar('Mirroring')
        toolbar.setLocked(False)
        toolbar.addSeparator()
        toolbar.addWidget(self.comboSymmetryXYZ)
        toolbar.addWidget(self.x_axis)
        toolbar.addWidget(self.y_axis)
        toolbar.addWidget(self.z_axis)
        toolbar.setLocked(True)

        self.SymmetryMode()
        mari.utils.connect(self.comboSymmetryXYZ.activated[str], lambda: self.SymmetryMode())

    def SymmetryMode(self):
        paintBuffer = mari.canvases.paintBuffer()
        if self.comboSymmetryXYZ.currentIndex() == 1:
            paintBuffer.aboutToBake.connect(self.mirror_bake)
        else:
            try:
                paintBuffer.aboutToBake.disconnect(self.mirror_bake)
            except:
                pass

    def script_path(self):
        ''' Loops through the Mari user dirs finding the script location '''
        for script_paths in mari.resources.path(mari.resources.USER_SCRIPTS).split(";"):
    		for dirname, folder, files in os.walk(script_paths):
    			if "BakeSymmetry" in str(dirname):
    				scriptPath = os.path.join(dirname)
    				return scriptPath

    def shortcuts_menu(self):
        #Mari custom shortcuts actions.
        actionSymmetryBakeX = mari.actions.create('Bake Symmetry X', 'mirror_bake()')
        actionSymmetryBakeX.setShortcut("Shift+X")
        mari.menus.addAction( actionSymmetryBakeX, "MainWindow/d&eTools/&Symmetry" )

        actionSymmetryBakeY = mari.actions.create('Bake Symmetry Y', 'symmetryBakeY()')
        actionSymmetryBakeY.setShortcut("Shift+Y")
        mari.menus.addAction( actionSymmetryBakeY, "MainWindow/d&eTools/&Symmetry")

        actionSymmetryBakeZ = mari.actions.create('Bake Symmetry Z', 'symmetryBakeZ()')
        actionSymmetryBakeZ.setShortcut("Shift+Z")
        mari.menus.addAction( actionSymmetryBakeZ, "MainWindow/d&eTools/&Symmetry")

        actionCameraInverseX = mari.actions.create('Invert Canvas X', 'cameraInverseX()')
        actionCameraInverseX.setShortcut("Ctrl+Shift+X")
        mari.menus.addAction( actionCameraInverseX, "MainWindow/d&eTools/&Symmetry")

        actionCameraInverseY = mari.actions.create('Invert Canvas Y', 'cameraInverseY()')
        actionCameraInverseY.setShortcut("Ctrl+Shift+Y")
        mari.menus.addAction( actionCameraInverseY, "MainWindow/d&eTools/&Symmetry")

        actionCameraInverseZ = mari.actions.create('Invert Canvas Z', 'cameraInverseZ()')
        actionCameraInverseZ.setShortcut("Ctrl+Shift+Z")
        mari.menus.addAction( actionCameraInverseZ, "MainWindow/d&eTools/&Symmetry")

    def is_checked():
        ''' Checks or sets the axis '''

        self.x_axis.setChecked(True)

    def bake(self):
        ''' '''

    def mirror_bake(self):

        x=1
        y=1
        z=1
        pbx=1
        pby=1

        if self.x_axis.isChecked():
            x = -1
            pbx = -1
        elif self.y_axis.isChecked():
            y = -1
            pbx = -1
        elif self.z_axis.isChecked():
            z = -1
            pbx = -1

        canvas = mari.canvases.current()
        camera = canvas.camera()

        #Avoid Mirroring in the UV Viewport.
        if camera.UV == camera.type():
            return


        bake = mari.actions.find("/Mari/Canvas/Bake")

        paintBuffer = mari.canvases.paintBuffer()
        currentpaint = paintBuffer.saveContent()

        pb_scale = paintBuffer.scale()
        pb_rotation = paintBuffer.rotation()
        pb_translation = paintBuffer.translation()

        lookAt = camera.lookAt()
        translation = camera.translation()
        up = camera.up()

        #Move to mirrored position
        camera.setLookAt(mari.VectorN(x*lookAt.x(),y*lookAt.y(),z*lookAt.z()))
        camera.setTranslation(mari.VectorN(x*translation.x(),y*translation.y(),z*translation.z()))
        camera.setUp(mari.VectorN(x*up.x(),y*up.y(),z*up.z()))

        #Mirror paint buffer
        paintBuffer.setScale(PySide.QtCore.QSizeF(pbx*pb_scale.width(),pby*pb_scale.height()))
        paintBuffer.setTranslation(pb_translation)
        paintBuffer.setRotation(pb_rotation)

        #disconnect to avoid looping
        if self.comboSymmetryXYZ.currentIndex() == 1:
            paintBuffer.aboutToBake.disconnect(self.mirror_bake)

        #Bake from the mirrored position first
        bake.trigger()

        #Restore the original position
        camera.setLookAt(lookAt)
        camera.setTranslation(translation)
        camera.setUp(up)
        #Resotre the original paint buffer
        paintBuffer.setScale(pb_scale)
        paintBuffer.setTranslation(pb_translation)
        paintBuffer.setRotation(pb_rotation)
        paintBuffer.restoreContent()

        currentBehave = mari.projection.getProperty("Projection/bakeBehavior")

        bake.trigger()
        mari.projection.setProperty("Projection/bakeBehavior", currentBehave)


        self.clearType = self.comboSymmetryXYZ.currentIndex()

        #reconnect now that we already passed the bake steps and avoided the loop.
        if self.comboSymmetryXYZ.currentIndex() == 1:
            paintBuffer.aboutToBake.connect(self.mirror_bake)




if __name__ == "__main__":
    BakeSymmetry()