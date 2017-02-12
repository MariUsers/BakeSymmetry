import mari
import PySide
import os


def mirror_bake():
	'''Executes a Mirror Bake'''

	actions = mirrorActions()
	X = actions['X'][1]
	Y = actions['Y'][1]
	Z = actions['Z'][1]

	x=1
	y=1
	z=1
	pbx=1
	pby=1

	if X.isChecked():
		x = -1
		pbx = -1
	elif Y.isChecked():
		y = -1
		pbx = -1
	elif Z.isChecked():
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

	# #disconnect to avoid looping
	paintBuffer.aboutToBake.disconnect(mirror_bake)

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

	#reconnect now that we already passed the bake steps and avoided the loop.
	paintBuffer.aboutToBake.connect(mirror_bake)

# --------------------------------------------------------------------

def SymmetryModeX():
	'''Action Target X Symmetry'''

	paintBuffer = mari.canvases.paintBuffer()

	actions = mirrorActions()
	X = actions['X'][1]
	Y = actions['Y'][1]
	Z = actions['Z'][1]

	if Y.isChecked():
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)
		Y.setChecked(False)
	if Z.isChecked():
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)
		Z.setChecked(False)

	if X.isChecked():
		paintBuffer.aboutToBake.connect(mirror_bake)
	else:
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)

def SymmetryModeY():
	'''Action Target Y Symmetry'''

	paintBuffer = mari.canvases.paintBuffer()

	actions = mirrorActions()
	X = actions['X'][1]
	Y = actions['Y'][1]
	Z = actions['Z'][1]

	if X.isChecked():
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)
		X.setChecked(False)
	if Z.isChecked():
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)
		Z.setChecked(False)

	if Y.isChecked():
		paintBuffer.aboutToBake.connect(mirror_bake)
	else:
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)

def SymmetryModeZ():
	'''Action Target Z Symmetry'''

	paintBuffer = mari.canvases.paintBuffer()

	actions = mirrorActions()
	X = actions['X'][1]
	Y = actions['Y'][1]
	Z = actions['Z'][1]

	if X.isChecked():
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)
		X.setChecked(False)
	if Y.isChecked():
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)
		Y.setChecked(False)

	if Z.isChecked():
		paintBuffer.aboutToBake.connect(mirror_bake)
	else:
		mari.utils.disconnect(paintBuffer.aboutToBake,mirror_bake)


# --------------------------------------------------------------------

def mirrorActions():
	''' convenience dictionary for all the actions'''

	x = '/Mari/Scripts/Mirror X'
	y = '/Mari/Scripts/Mirror Y'
	z = '/Mari/Scripts/Mirror Z'

	x_act = mari.actions.find(x)
	y_act = mari.actions.find(y)
	z_act = mari.actions.find(z)

	actions = {
				'X':(x,x_act),
				'Y':(y,y_act),
				'Z':(z,z_act)
			}

	return actions


def mirrorToolbarActions():
	'''adds actions to mari ui'''

	icon_path = os.path.join(os.path.dirname(__file__), "Icons")

	mirrorX= mari.actions.create ('Mirror X', 'MirrorBake.SymmetryModeX()')
	mirrorY= mari.actions.create ('Mirror Y', 'MirrorBake.SymmetryModeY()')
	mirrorZ= mari.actions.create ('Mirror Z', 'MirrorBake.SymmetryModeZ()')
	mirrorX.setCheckable(True)
	mirrorY.setCheckable(True)
	mirrorZ.setCheckable(True)


	mari.actions.addToSet('RequiresProject',mirrorX)
	mari.actions.addToSet('RequiresProject',mirrorY)
	mari.actions.addToSet('RequiresProject',mirrorZ)


	mirrorX.setIconPath(icon_path + os.sep + 'X.png')
	mirrorY.setIconPath(icon_path + os.sep + 'Y.png')
	mirrorZ.setIconPath(icon_path + os.sep + 'Z.png')

	toolbar = mari.app.findToolBar('Mirroring')
	toolbar.setLocked(False)
	toolbar.addSeparator()
	toolbar.addActionBefore('/Mari/Scripts/Mirror X',None,False)
	toolbar.addActionBefore('/Mari/Scripts/Mirror Y',None,False)
	toolbar.addActionBefore('/Mari/Scripts/Mirror Z',None,False)
	toolbar.setLocked(True)


if __name__ == "__main__":
	mirrorToolbarActions()