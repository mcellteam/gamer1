# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:45:52 2010

@author: Ludovic Autin
"""
#http://www.blender.org/documentation/blender_python_api_2_59_release/bpy.types.html

import bpy
import mathutils
#from math import *
from bpy import props

from upy.uiAdaptor import uiAdaptor
from functools import partial
import os
#    Add button

def checkUIVar(ww, context):
    if not hasattr(bpy,"current_gui") :
        return
    self = getattr(bpy,"current_gui")
    scn = bpy.context.scene    
    #layout event
    for block in self._layout:
        if type(block) is list :
            for elem in block:
                if elem["type"] in ["inputStr","pullMenu","checkbox",
                    "sliders","slidersInt","inputInt","inputFloat","color"]: 
                    if self.isChanged(elem["name"]):
                        #send event message to command?
#                        self._command([elem["id"],])
                        self._callElemAction(elem)
#                            return
        else : #dictionary: multiple line / format dict?
            if "0" in block:
                for i in range(1,len(block)):
                    for elem in block[str(i)]:
                        if elem["type"] in ["inputStr","pullMenu","checkbox",
                            "sliders","slidersInt","inputInt","inputFloat","color"]: 
                            if self.isChanged(elem["name"]):
                                #send event message to command?
#                                self._command([elem["id"],])
                                self._callElemAction(elem)
#                                    return
            else :                
                for k,blck in enumerate(block["elems"]):
                    for index, item in enumerate(blck):
                        if item["type"] in ["inputStr","pullMenu","checkbox",
                        "sliders","slidersInt","inputInt","inputFloat"]: 
                            if self.isChanged(item["name"]):
                                #send event message to command?
#                                self._command([item["id"],])
                                self._callElemAction(item)
#                                    return

class OP_Subdialog (bpy.types.Operator):
    bl_label = "Sub Dialog"
    bl_idname = "pyubic.subdialog"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    subdialname = bpy.props.StringProperty()
    
    def draw(self, context):
        print ("redraw")
        #will draw here all element from the block
#        #bpy.epmv.gui._draw(bpy.epmv.gui.layout_block["xNamex"],1)
        subdial = getattr(bpy,self.subdialname)
        bpy.current_gui = subdial
        subdial.panel = self
        subdial.layout = self.layout
        subdial.current_layout = self.layout

        subdial.CreateLayout()
        #set defaultValue
#        self.layout.label(self.message)

    def execute(self, context):
        print ("ok subdialog?")
        #rename_datablocks_main(self, context)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        result = wm.invoke_props_dialog(self)#popup?
        print (result)
        return {"RUNNING_MODAL"}

bpy.utils.register_class(OP_Subdialog)


class DialogOperator(bpy.types.Operator):
    bl_idname = "pyubic.dialog_message"
    bl_label = "Message"

#    my_float = bpy.props.FloatProperty(name="Some Floating Point")
#    my_bool = bpy.props.BoolProperty(name="Toggle Option")
    messageString = bpy.props.StringProperty()
    width = bpy.props.IntProperty(default = 300)
    height = bpy.props.IntProperty(default = 20)
    result = bpy.props.BoolProperty(default = True)    
    
    def draw(self, context):
        layout = self.layout
        lines = self.messageString.split("\n")
        for line in lines :
            row = layout.row()
            row.label(line)
        
    def execute(self, context):
        message = "%s" % \
            (self.messageString)
        self.report({'INFO'}, message)
        return {'FINISHED'}

    def cancel(self,context):
        self.result = False
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self,width=self.width, height=self.height)

bpy.utils.register_class(DialogOperator)

# test call
#bpy.ops.object.dialog_operator('INVOKE_DEFAULT')

#call via bpy.ops.pyubic.save('INVOKE_DEFAULT')
class FILEBROWSER_PT_General(bpy.types.Operator):
    bl_idname = "pyubic.filedialog"
    bl_label = "File"
#    filepath = bpy.props.StringProperty(
#        name="File Path", 
#        description="File path to PDB", 
#        maxlen= 1024, default= "",subtype="FILE_PATH")
    filepath = bpy.props.StringProperty(name="File Path", description="File path to write file to")
    filter_folder = bpy.props.BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
    filter_python = bpy.props.BoolProperty(name="Filter python", description="", default=True, options={'HIDDEN'})
    filter_glob = bpy.props.StringProperty(default="*.py;*.zip", options={'HIDDEN'})
    label = "File"
    callback = None
#    @classmethod
#    def poll(cls, context): return True
    
    def invoke(self, context, event):
#        import os
#        if not self.filepath:
#            blend_filepath = context.blend_data.filepath
#            if not blend_filepath:
#                blend_filepath = "untitled"
#            else:
#                blend_filepath = os.path.splitext(blend_filepath)[0]
#
#            self.filepath = blend_filepath# + self.filename_ext        
        self.bl_label = self.label
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if self.callback is not None :
            self.callback(self.filepath)
        print ("should write in ",self.filepath)
        return {'FINISHED'}

## Assign a menu collection
#class MenuSetting(bpy.types.PropertyGroup):
#    name = bpy.props.StringProperty()
#    value = bpy.props.IntProperty()
#    current = bpy.props.IntProperty()
#    
#bpy.utils.register_class(MenuSetting)

class MENU_OT_General(bpy.types.Menu):
    bl_idname = "pyubic.menu"
    bl_label = "Menu"
#    guiname = bpy.props.StringProperty()
#    sub = bpy.props.StringProperty()
    
    #guiname_k = guiname
    
    def draw(self, context):
        self.layout.operator_context = "INVOKE_DEFAULT"
#        print ("text ",self.bl_label)
#        print (dir(self))
        layout = self.layout
#        scn = bpy.context.scene
        gui = getattr(bpy,"current_gui")
#        guiname = getattr(scn,"gui_name")
        #options = getattr(bpy,gui.title.replace(" ","_")+"menu_current")
        k,sub = self.bl_label.split(".")
#        print ("ok for menu ",self.bl_label,k,sub)
        if gui.MENU_ID :
            #MenuOp,menuDic,sub="",menuOrder=None
            gui.internal_createMenu(self,gui.MENU_ID,k,
                                    sub=sub,menuOrder=gui.menuorder)
    
    def invoke(self, context, event):
        print ("INVOKE")
        return {'FINISHED'}
        
class OBJECT_OT_General(bpy.types.Operator):
    bl_idname = "pyubic.push"
    bl_label = "pushbutton"
#    name = bpy.props.StringProperty() 
    id = bpy.props.IntProperty()
    modetype = bpy.props.StringProperty()
#    x=bpy.props.IntProperty()
#    y=bpy.props.IntProperty()
#    w=bpy.props.IntProperty()
#    h=bpy.props.IntProperty()
#    tooltip = bpy.props.StringProperty()
#    icon = None
#    action = None
#    elem = None
    
    def execute(self, context):
        #get the general dictionay ad action
#        print (self.id)
#guiname should be something like bpy.gui...
        guiname, id = self.modetype.split(".")
        print (guiname, id)
        gui = getattr(bpy,guiname)
        gui._command([int(id),])
#        exec(guiname+"._command([int(id),])")
        return{'FINISHED'}
        
bpy.utils.register_class(OBJECT_OT_General)
bpy.utils.register_class(MENU_OT_General)
bpy.utils.register_class(FILEBROWSER_PT_General)

def noaction(ww,context):
    print (context)
    return

#UI general interface
class blenderUI:
    """
    The blender uiAdaptor abstract class
    ====================================
        This Adaptor give access to the basic blender Draw function need for 
        create and display a panel gui.
    """
#    #blender keyword
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'TOOLS'#'UI'"TOOL_PROPS"
#
#    bl_label = "pyubic"
##    bl_context = "objectmode"
#    bl_default_closed = False


    host = "blender25"
    maxStrLenght=100
    scale = 2
#    topLine = 700
    bid=1
    MousePos = [0, 0]
    ScrollPos = 0
    ScrollState = 0
    ScrollInc = 25 
    dock = False
    #special function for subdialog and UIblock
    subdialog = False
    drawUIblock = False
    block = False
    w=250
    h=1
    softdir=None
    prefdir=None
    fileDresult=""
    notebook=None
    currentScroolbar={}
    widgetGap = 6
    limit_scrollbar = 200
    ystep = -30
    layout_block = {}
    panel = None
    uiname = "ui"
    space_type = "VIEW_3D"#"SCRIPTS_WINDOW"#"VIEW_3D"
    region_type = "TOOLS"#_PROPS
    


    def no_action(self, *args, **kwargs):pass
        
#    def Quit(self):
#        """ Close the windows"""
#        Blender.Draw.Exit()

#    def CoreMessage(self, evt, val):
#        """ Hanlde the system event such as key or mouse position """
#        #EXIT EVENT
#        if len(self.currentScroolbar):
#            if self.currentScroolbar["value"] is not None :
#                self.currentScroolbar["value"].eventFilter(evt,val)
#        if evt == Blender.Draw.ESCKEY or evt == Blender.Draw.QKEY:
#           stop = Blender.Draw.PupMenu("OK?%t|Stop the script %x1")
#           if stop == 1:
#                self.Quit()
#        #SCROLLING EVT
##        if (evt == Blender.Draw.WHEELDOWNMOUSE):                         
##            #Scroll area down
##            if (self.ScrollState < 0):
##                self.ScrollPos   = self.ScrollPos+self.ScrollInc
##            Blender.Draw.Draw()
##        elif (evt == Blender.Draw.WHEELUPMOUSE):                         
##            #Scroll area up
##            if (self.ScrollPos > 0):
##                self.ScrollPos = self.ScrollPos-self.ScrollInc
##            else: self.ScrollPos = 0
##            Blender.Draw.Draw()
##        if (evt == Blender.Draw.DOWNARROWKEY):                           
##            #Scroll area down
##            if (self.ScrollState < 0):
##                self.ScrollPos   = self.ScrollPos+self.ScrollInc
##            Blender.Draw.Draw()
##        elif (evt == Blender.Draw.UPARROWKEY):                           
##            #Scroll area up
##            if (self.ScrollPos > 0):
##                self.ScrollPos   = self.ScrollPos-self.ScrollInc
##            else: self.ScrollPos = 0
##            Blender.Draw.Draw()
##        #MOUSE CLICK EVT
#        elif (evt == Blender.Draw.LEFTMOUSE and val):                    
#            #Calculate mouse position in this area
#            areaVert        =  [item["vertices"] \
#                for item in Blender.Window.GetScreenInfo() \
#                if item["id"] == Blender.Window.GetAreaID()]
#            MouseCor        = Blender.Window.GetMouseCoords()
#            self.MousePos[0]     = MouseCor[0]-areaVert[0][0]
#            self.MousePos[1]     = MouseCor[1]-areaVert[0][1]
##            print "mouse", self.MousePos
#            Blender.Draw.Draw()
#        elif (evt == Blender.Draw.LEFTMOUSE and not val):                
#            #If button up then clear mouse position
#            self.MousePos[0]     = 0
#            self.MousePos[1]     = 0
#        elif (evt == Blender.Draw.RIGHTMOUSE and val):                   
#            #Collapse or expand all subWindows based on popmenu choice
#            result = Blender.Draw.PupMenu("Expand all|Collapse all|Exit",27)
#            if (result == 1):
#                for elem in self._layout:
#                    if type(elem) is not list :
#                        if elem["type"] == "frame":
#                            elem["collapse"] = False
#                self.ScrollPos = 0
#            if (result == 2):
#                for elem in self._layout:
#                    if type(elem) is not list :
#                        if elem["type"] == "frame":
#                            elem["collapse"] = True
#                self.ScrollPos = 0
#            if (result == 3):
#                self.Quit()
#            Blender.Draw.Draw()
#        elif (evt == Blender.Draw.HKEY and not val):
#            pass#ShowHelp()
#        elif (evt == Blender.Draw.RKEY and not val):
#            pass
#        elif (evt == Blender.Draw.AKEY and not val):
#            pass
#        elif (evt == Blender.Draw.PKEY and not val):
#            pass
#        elif (evt == Blender.Draw.MOUSEX or evt == Blender.Draw.MOUSEY):              
#            pass
#            #Update area if mouse is over it and scene or active object has changed
#            #Set mouse position to zero to prevent LEFTMOUSE tab collapse flashing while moving
#            self.MousePos[0]         = 0                         
#            self.MousePos[1]         = 0
##            CurrentScene        = Blender.Scene.GetCurrent()
##            CurrentObject       = CurrentScene.objects.active
##            try:
##                CurrentMaterial = CurrentObject.getMaterials(1)[CurrentObject.activeMaterial-1]
##                if (CurrentMaterial == None):   CurrentMaterial = CurrentObject.getData(False, True).materials[CurrentObject.activeMaterial-1]
##            except:                             CurrentMaterial = ""
##            if ((CurrentScene and LastScene != CurrentScene.name) or (CurrentObject and LastObject != CurrentObject.name) or (CurrentMaterial and LastMaterial != CurrentMaterial.name)):
##                Draw()
#      
    def makeUpdateFunction(self,callback=None):
        if callback is None :
            return None
        def updateFunction(self, context):
            callback()
        return updateFunction
    
    def SetTitle(self,title):
        """ Initialised the windows and define the windows titles 
        @type  title: string
        @param title: the window title

        """
        if not title :
            title  = self.title        
        #how do we access it throught bpy?
        setattr(bpy,title.replace(" ","_")+"ui",self)
        setattr(bpy,"current_gui",self)
        self.uiname = title.replace(" ","_")+"ui"
        
#        setattr(bpy.types.Scene,self.title.replace(" ","_")+"menu_settings",
#                bpy.props.CollectionProperty(type=MenuSetting))
#        setattr(bpy,self.title.replace(" ","_")+"menu_current",
#                bpy.props.StringProperty())#should be name+sub ?

#        self.ScrollState     = 0
#        self.AreaDims        = Blender.Window.GetAreaSize()  
##        print self.AreaDims
#        #Get AreaSize for widget placement
#        self.y = self.top  = self.SubPosYInc  = self.AreaDims[1]+self.ScrollPos             
#        #Increment by ScrollPos 
#        self.TitleHeight     = 25                                
#        #Height of top title bar
#        self.WindowGap       = 6                                 
#        #Distance between and around sub-windows
#        self.SubPosXInc      = self.WindowGap
#        self.SubPosYStart    = self.SubPosYInc-self.TitleHeight-self.WindowGap
#        self.SubMinimum      = 400
#        if (self.AreaDims[0] < self.SubMinimum):  
#            self.SubWidth = self.AreaDims[0]
#        else:                           
#            self.SubWidth = self.AreaDims[0]/int(self.AreaDims[0]/self.SubMinimum)
#        if not title :
#            title  = self.title
#        if title:
#            TitleColor      = Theme.Get()[0].get("BUTS").header
#            TextColor       = Theme.Get()[0].get("ui").menu_text
#                #Draw Title
#            BGL.glColor3f(TitleColor[0]/256.0, 
#                          TitleColor[1]/256.0, 
#                          TitleColor[2]/256.0)
#            BGL.glRecti(0, self.SubPosYInc, self.AreaDims[0], self.SubPosYInc-self.TitleHeight)
#            BGL.glColor3f(TextColor[0]/256.0, 
#                          TextColor[1]/256.0, 
#                          TextColor[2]/256.0)
#            BGL.glRasterPos2d(10, self.SubPosYInc-self.TitleHeight/2-4)
#            Blender.Draw.Text(title)
##            BGL.glColor3f(0.,0.,0.)
##            endGap = 5
##            x= 5 
##            BGL.glLineWidth(1)
##            BGL.glBegin(BGL.GL_LINES)
##            BGL.glVertex2i(x, self.SubPosYInc-self.TitleHeight/2-4)
##            BGL.glVertex2i(x, self.SubPosYInc-self.TitleHeight/2-4)
##            BGL.glEnd()            
#            self.SubPosYInc = self.SubPosYStart
#            self.y = self.SubPosYInc - self.TitleHeight/2
#        else :
#            self.y = self.SubPosYInc

    def setupMenu(self):
        #need to create the collection and access it for each menu and submenu item?
        #setattr(bpy.types.Scene,self.title.replace(" ","_")+"menu_settings",
        lookat = self.menuorder
        menuDic = self.MENU_ID
#        menuSetting = getattr(bpy.types.Scene,self.title.replace(" ","_")+"menu_settings")
        for k in lookat:
            lelem = menuDic[k]                  
            idname = ("pyubic.menu_%s_%s" % (self.uiname,k))
#                def func(self, context):
#                    print("Hello World", self)
#                    return {'FINISHED'}   
            opclass = type("DynMT%s_%s" % (self.uiname,k), (MENU_OT_General, ), {"bl_idname": idname,
                                                                    "bl_label": k+".",})
#                                                                    "execute": func})
            bpy.utils.register_class(opclass)
            lelem = menuDic[k]
            for i,elem in enumerate(lelem):
                if elem["sub"] is not None:
                    idname = ("pyubic.sub_menu_%s_%d" % (self.uiname,i))
                    opclass = type("DynMT%s_%d" % (self.uiname,i), (MENU_OT_General, ), {"bl_idname": idname,
                                                                    "bl_label": k+"."+elem["name"],})
#                                                                    "execute": func})
                    bpy.utils.register_class(opclass)
                
                
    def internal_createMenu(self,MenuOp,menuDic,k,sub="",menuOrder=None):
#        print("createMenu ",k,"sub",sub)
#        print (getattr(bpy,self.title.replace(" ","_")+"menu_current"))
        if menuOrder : 
            lookat = menuOrder
        else :
            lookat = list(menuDic.keys())
        layout = MenuOp.layout
        #for k in lookat :
        lelem = menuDic[k]
#        print (len(lelem))
        for i,elem in enumerate(lelem):
            if sub == elem["name"] :
                #need to create whats in the submenu
                for sub in elem['sub']:
                    layout.operator("pyubic.push",
                    text = elem['sub'][sub]["name"]).modetype = self.uiname+"."+str(elem['sub'][sub]["id"])
                break
            else :
                if elem["sub"] is not None:
                    setattr(bpy,self.title.replace(" ","_")+"menu_current",
                            k+"."+elem["name"]) 
                    idname = ("pyubic.sub_menu_%s_%d" % (self.uiname,i))
                    layout.menu(idname,text = elem["name"])
                else :
                    layout.operator("pyubic.push",
                    text = elem["name"]).modetype = self.uiname+"."+str(elem["id"])
        
    def createMenu(self,menuDic,menuOrder=None):
        """ Define and draw the window/widget top file menu
        @type  menuDic: dictionary
        @param menuDic: the menu elements, ie entry, callback and submenu
        @type  menuOrder: array
        @param menuOrder: the menu keys oredered
        """        
        #There is no Actual Menu in Blender, bu we can use the Pull Down Menu
        #subMenu: create a callback that create another PupMenu with the subvalue
        #the menu id is the first elem id
#        print("createMenu")
        if menuOrder : 
            lookat = menuOrder
        else :
            lookat = list(menuDic.keys())
        self.startBlock()
        setattr(bpy,"current_gui",self)
        #need to call an operator per menu items...so need to instanciate each of them
        for k in lookat:
#            print ("menu ",k)
#            setattr(bpy,self.title.replace(" ","_")+"menu_current",k+".")            
#            setattr(bpy,self.title.replace(" ","_")+"menu_"+k,"")            
            idname = ("pyubic.menu_%s_%s" % (self.uiname,k))
            self.current_layout.menu(idname,text=k)
#        for k in lookat:
#            Blender.Draw.PushButton(mitem,menuDic[mitem][0]["id"], x, 
#                                        self.y, 75, 25)
#            menuDic[k]
#            pos={}
#            pos["x"]=x
#            pos["y"]=self.SubPosYInc-self.TitleHeight/2-1
#            pos["w"]=75
#            pos["h"]=25
#            item = menuDic[k]
#            menuDic[k] = [item,pos]
#            self.drawLabel(k, x, self.SubPosYInc-self.TitleHeight/2-1, 75, 25)
#            x = x + 75
#        for k in lookat:
#            mitem=menuDic[k]
#            item = mitem[0]
#            mitem = mitem[1]
#            if (self.MousePos[0] > mitem["x"] and self.MousePos[0] < mitem["x"]+mitem["w"] \
#                and self.MousePos[1] > mitem["y"] \
#                and self.MousePos[1] < mitem["y"]+mitem["h"]):
#                self.MousePos = [0, 0]                    
#                self.menu_cb(menuDic,k)
#        for k in lookat:
#            menuDic[k] = menuDic[k][0]
        
#    def menu_cb(self,menu,menuId):
#        listOptions =[]
#        suboptions={}
#        litem = menu[menuId][0]
#        for i,item in enumerate(litem):
##            print item
#            listOptions.append(item["name"])
#            if item["sub"] is not None :
#                msubOptions = []
#                suboptions[str(i+1)]={}
#                for j,sub in enumerate(item['sub']):
#                    suboptions[str(i+1)][j]=item['sub'][sub]
#                    msubOptions.append(item['sub'][sub]["name"])
#        choice = Blender.Draw.PupMenu('|'.join(listOptions))
#        if choice == -1 :
#            return
#        elif str(choice) in list(suboptions.keys()):
#            subchoice = Blender.Draw.PupMenu('|'.join(msubOptions))
#            action = suboptions[str(choice)][subchoice-1]["action"]
#            if action is not None:
#                action(suboptions[str(choice)][subchoice-1]["id"])
#        else :
#            action = menu[menuId][0][choice-1]["action"]
#            if action is not None :
#                print(action,choice)
#                action(choice)


    def checkwh(self,elem,w,h):
        """ Specific function for blender which check the size of the elem """
#        print "ok",w,h
        #if w is None :
        #    w = elem["width"]*self.scale
        #if h is None:
        #    h = elem["height"]*self.scale
        #if elem["type"] == "pullMenu":
        #    w,h = elem["width"],elem["height"]*self.scale
#        print "use",w,h
        return int(elem["width"]*self.scale), int(elem["height"]*self.scale)
        
    def addVariable(self,type,value):
        """ Create a container for storing a widget states """
        return [type,value]
#        if type == "col" or type == "color":
#            var = bpy.props.FloatVectorProperty()#Blender.Draw.Create(value[0],value[1],value[2])
#        elif type == "int":
#            var =  bpy.props.IntProperty()
#        elif type == "float":
#            var =  bpy.props.FloatProperty()
#        elif type == "str": 
#            var =  bpy.props.StringProperty()
#        elif type == "bool": 
#            var =  bpy.props.BoolProperty()
#        #add the var to scene...
#        return var

    def addVariablePropToSc(self,elem,type,value):
        updateF = noaction#checkUIVar
        if "action" in elem:
            updateF = self.makeUpdateFunction(elem["action"])
            if updateF == None :
                updateF = noaction
        name = elem["name"]
#        if len(name) > 31 :
#            name = name [0:30]
        propName = name.replace(" ","_")            
        #maxLength is 31
        if type == "col" or type == "color":
            setattr(bpy.types.Scene,propName,bpy.props.FloatVectorProperty(update=updateF,
                        step=1,precision = 3,min=0.,max=1.0,soft_min=0.,
                        soft_max=1.0,subtype="COLOR"))
            setattr(self,propName+"_o",None)
            #setattr(bpy.types.Scene,propName+"_o",bpy.props.FloatVectorProperty())
#            setattr(self,propName+"_o",None)
        elif type == "int":
            if elem["type"] == "pullMenu":
                #setMenu
                lMenu=[]
                for i,m in enumerate(elem["value"]) :
                    l = (str(i),m,m)
                    lMenu.append(l)#return,name,description
                if elem["action"] is not None :
                    setattr(bpy.types.Scene,propName,
                        bpy.props.EnumProperty(items=lMenu,name=elem["name"],
                        update=self.makeUpdateFunction(elem["action"])))
                else :        
                    setattr(bpy.types.Scene,propName,
                        bpy.props.EnumProperty(items=lMenu,name=elem["name"],update=updateF))
                
                setattr(self,propName+"_o","0")
#                setattr(bpy.types.Scene,propName+"_o",
#                        bpy.props.EnumProperty(items=lMenu,name=elem["name"]))
#                setattr(self,propName+"_o",None))
            elif elem["type"] == "checkbox":
#                print (propName,name)
                setattr(bpy.types.Scene,propName,bpy.props.BoolProperty(name=name,update=updateF))
                setattr(self,propName+"_o",bool(value))
#                setattr(bpy.types.Scene,propName+"_o",bpy.props.BoolProperty(name=name))
            elif elem["type"] == "sliders" or elem["type"] == "slidersInt":
                setattr(bpy.types.Scene,propName,
                                bpy.props.IntProperty(default=value, 
                                min=elem["mini"], max=elem["maxi"], 
                                #soft_min=elem["mini"], soft_max=elem["maxi"], 
                                step=elem["step"], update=updateF))
                setattr(self,propName+"_o",value)
#                setattr(bpy.types.Scene,propName+"_o",bpy.props.IntProperty())
            else :
                setattr(bpy.types.Scene,propName,bpy.props.IntProperty(default=value,
                                                                       update=updateF))
                setattr(self,propName+"_o",value)
#                setattr(bpy.types.Scene,propName+"_o",bpy.props.IntProperty())
        elif type == "float":
            if elem["type"] == "sliders":
#                print (elem["name"],int(elem["precision"]),float(elem["mini"]),float(elem["maxi"]),
#                float(elem["step"]),float(value))
                setattr(bpy.types.Scene,propName,
                                bpy.props.FloatProperty(default=float(value), 
                                precision = int(elem["precision"]),
                                min=float(elem["mini"]), max=float(elem["maxi"]), 
                                #soft_min=elem["mini"], soft_max=elem["maxi"], 
                                step=elem["step"], update=updateF))
                setattr(self,propName+"_o",value)
#                setattr(bpy.types.Scene,propName+"_o",bpy.props.FloatProperty())
            else :
                setattr(bpy.types.Scene,propName,bpy.props.FloatProperty(default=value,
                                                                         update=updateF))
                setattr(self,propName+"_o",value)
#                setattr(bpy.types.Scene,propName+"_o",bpy.props.FloatProperty())
        elif type == "str": 
            setattr(bpy.types.Scene,propName,
                    bpy.props.StringProperty(default=value,
                                             update=updateF))
            setattr(self,propName+"_o",value)
#            setattr(bpy.types.Scene,propName+"_o",bpy.props.StringProperty())
        elif type == "bool": 
            if elem["type"] == "frame":
                setattr(bpy.types.Scene,propName+"_c",bpy.props.BoolProperty(name=name,
                        description='Collapse the Frame', default=bool(elem["collapse"])))
            else :
                setattr(bpy.types.Scene,propName+"_o",
                        bpy.props.BoolProperty(default=value,update=checkUIVar))
                setattr(self,propName+"_o",bool(value))
#                setattr(bpy.types.Scene,propName+"_o",bpy.props.BoolProperty())
#        setattr(self,propName,None)
        elem["id"] == name
            
    def startBlock(self,m=1,n=1):
        self.current_layout = self.layout.row(align=True)
        self.current_layout.alignment = 'LEFT'#'EXPAND'

    def endBlock(self):
        pass
#        self.current_layout.separator()

    def drawButton(self,elem,x,y,w=None,h=None):
        """ Draw a Button 
        @type  elem: dictionary
        @param elem: the button dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """
        w,h = self.checkwh(elem,w,h)

        self.current_layout.operator("pyubic.push",
                                     text = elem["name"]).modetype = self.uiname+"."+str(elem["id"])
#        args = (elem["name"], elem["id"], int(x), int(y), int(w), int(h),\
#                elem["tooltip"])
#        if self.subdialog : 
#            return self.check_addAction(Blender.Draw.PushButton, elem["action"],
#                                        *args)
#        else :
#            return Blender.Draw.PushButton(*args)

    def drawButtonToggle(self,elem,x,y,w=None,h=None):
        """ Draw a checkBox 
        @type  elem: dictionary
        @param elem: the button dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """     
        w,h = self.checkwh(elem,w,h)
        args = (elem["name"], elem["id"], int(x), int(y), int(w), int(h),\
                elem["variable"].val, elem["tooltip"])
        if self.subdialog :
            elem["variable"]=self.check_addAction(Blender.Draw.Toggle, \
                                                  elem["action"], *args)
        else :
            elem["variable"]=Blender.Draw.Toggle(*args)

    def drawBOX(self,x1,x2,y1,y2):
        back_color = [col/256. for col in Theme.Get()[0].get("ui").menu_back[:-1]]
        line_color = [col/256.*3/4 for col in Theme.Get()[0].get("ui").outline[:-1]]
        BGL.glColor3f(*back_color)
        BGL.glLineWidth(1)
        BGL.glBegin(BGL.GL_QUADS)
        BGL.glVertex2i(x1, y1)
        BGL.glVertex2i(x2, y1)
        BGL.glVertex2i(x2, y2)
        BGL.glVertex2i(x1, y2)
        BGL.glEnd()        
        BGL.glColor3f(*line_color)
        BGL.glBegin(BGL.GL_LINE_LOOP)
        BGL.glVertex2i(x1, y1)
        BGL.glVertex2i(x2, y1)
        BGL.glVertex2i(x2, y2)
        BGL.glVertex2i(x1, y2)
        BGL.glEnd()        
        BGL.glColor3f(0, 0, 0)

    def drawCROSS(self,x1,x2,y1,y2):
        line_color = [col/256./2 for col in Theme.Get()[0].get("ui").outline[:-1]]
        BGL.glColor3f(*line_color)
        BGL.glLineWidth(2)
        BGL.glBegin(BGL.GL_LINES)
        BGL.glVertex2i(x1, y1)
        BGL.glVertex2i(x2, y2)
        BGL.glVertex2i(x2, y1)
        BGL.glVertex2i(x1, y2)
        BGL.glEnd()        
        BGL.glColor3f(0, 0, 0)

    def drawCheckBox(self,elem,x,y,w=None,h=None):#drawGLCheckBox
#        if not elem["show"]:
#            return
        w,h = self.checkwh(elem,w,h)
        self.drawElem(elem,x,y,w=w,h=h)
#        if self.subdialog :
#            elem["variable"]=self.check_addAction(Blender.Draw.Toggle, \
#                elem["action"], elem["name"], elem["id"], int(x), int(y), \
#                int(w), int(h), elem["variable"].val, elem["tooltip"])
#        else :
#            box_offset = 2
#            box_coordinates = [x+box_offset,x+h-2*box_offset,\
#                               y+1+box_offset,y+h+1-2*box_offset]
#            doit = False
#            if (self.MousePos[0] > x and self.MousePos[0] < x+w \
#                and self.MousePos[1] > y-h+10 and self.MousePos[1] < y+20):
#                elem["variable"].val = not elem["variable"].val
#                self.MousePos = [0, 0]
#    #            print elem["variable"].val
#                doit = True
#            self.drawBOX(*box_coordinates)
#            if elem["variable"].val :
#                self.drawCROSS(*box_coordinates)
#            #need to draw the text
#            #Draw Tab Text
#            TitleHeight = 15
#            TextOffset  = TitleHeight/2+4        
#            BGL.glRasterPos2d(x+h, y+3*box_offset)
#            Blender.Draw.Text(elem["name"], "normal")        
#            #what about the calback?
#            if elem["action"] is not None and doit:
#                elem["action"]()

    def drawObj(self,elem,x,y,w=None,h=None):
        """ Draw an object input where you can drag on object 
        @type  elem: dictionary
        @param elem: the button dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """   
        pass


    def resetPMenu(self,elem):
        """ Add an entry to the given pulldown menu 
        @type  elem: dictionary
        @param elem: the pulldown dictionary
        """
        elem["value"]=[]
        #elem["variable"].val = len(elem["value"])
        lMenu=[]
        propName = elem["name"].replace(" ","_")
        if elem["action"] is not None :
            setattr(bpy.types.Scene,propName,
                bpy.props.EnumProperty(items=lMenu,name=elem["name"],
                update=self.makeUpdateFunction(elem["action"])))
        else :        
            setattr(bpy.types.Scene,propName,
                bpy.props.EnumProperty(items=lMenu,name=elem["name"],
                update=checkUIVar))

    def addItemToPMenu(self,elem,item):
        """ Add an entry to the given pulldown menu 
        @type  elem: dictionary
        @param elem: the pulldown dictionary
        @type  item: string
        @param item: the new entry
        """
        propName = elem["name"].replace(" ","_")
        elem["value"].append(item)
        lMenu=[]
        for i,m in enumerate(elem["value"]) :
            l = (str(i),m,m)
            print (l)
            lMenu.append(l)#return,name,description
        if elem["action"] is not None :
            setattr(bpy.types.Scene,propName,
                bpy.props.EnumProperty(items=lMenu,name=elem["name"],
                update=self.makeUpdateFunction(elem["action"])))
        else :        
            setattr(bpy.types.Scene,propName,
                bpy.props.EnumProperty(items=lMenu,name=elem["name"],
                update=checkUIVar))

    def drawPMenu(self,elem,x,y,w=None,h=None):
        """ Draw a pulldown menu 
        @type  elem: dictionary
        @param elem: the pulldown dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """            

        w,h = self.checkwh(elem,w,h)
        scn = bpy.context.scene
        self.current_layout.prop(scn, elem["name"].replace(" ","_"))        
        #prop_enum
#        
#        menuitems = ""
#        if elem["name"]:
#            menuitems += elem["name"]+"%t|"  # if no %xN int is set, indices start from 1
#        for i,it in enumerate(elem["value"]):
#            menuitems+="|"+it+"%x"+str(i+1)
##        menuitems+='|'.join(elem["value"])
#        #name, event, x, y, width, height, default, tooltip=None, callback=None
#
#        args = (menuitems,elem["id"], int(x), int(y), int(w), int(h),
#                elem["variable"].val,elem["tooltip"])
#        if self.subdialog :
#            elem["variable"]=self.check_addAction(Blender.Draw.Menu, elem["action"],
#                                                  *args)
#        else :
#            elem["variable"]=Blender.Draw.Menu(*args)
        
    def drawText(self,elem,x,y,w=None,h=None):
        """ Draw a Label
        @type  elem: dictionary
        @param elem: the label dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """     
#        elem["width"] = len(elem["label"])* 3.
        if type(elem) == str :
            label = elem
        else :
            label = elem["label"]
            w,h = self.checkwh(elem,w,h)
        #Blender.BGL.glRasterPos2i(x,y+5)
        Blender.BGL.glColor3i(0,0,0)
        Blender.Draw.Label(label, x, y, w, h)
#        elem["width"] = len(elem["label"])* 3 #TODO find a more flexible solution

    def drawLine(self,elem,x,y,w=None,h=None):
        """ Draw a Separative Line
        @type  elem: dictionary
        @param elem: the label dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """   
        TitleColor  = Theme.Get()[0].get("BUTS").header        
        BGL.glColor3f(TitleColor[0]/256., TitleColor[1]/256.0, TitleColor[2]/256.0)
        endGap      = 5
        w,h = self.checkwh(elem,w,h)
        if elem["value"] == "H":  
            BGL.glLineWidth(1)
            BGL.glBegin(BGL.GL_LINES)
            BGL.glVertex2i(x+endGap, y)
            BGL.glVertex2i(x+self.w-endGap, y)
            BGL.glEnd()
        elif elem["value"] == "V":
            BGL.glLineWidth(1)
            BGL.glBegin(BGL.GL_LINES)
            BGL.glVertex2i(x, y+endGap)
            BGL.glVertex2i(x, y+self.h-endGap)
            BGL.glEnd()
        if elem["label"] is not None :
            self.drawText(elem,x+endGap,y+4,w=w,h=h)

    def drawLabel(self,elem,x,y,w=None,h=None):
        """ Draw a Label
        @type  elem: dictionary
        @param elem: the label dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """      
#        elem["width"] = 50#len(elem["label"])* 3.       
        if type(elem) == str :
            label = elem
        else :
            label = elem["label"]
            w,h = self.checkwh(elem,w,h)
#        Blender.BGL.glRasterPos2i(x,y+5)
        self.current_layout.label(label)
#        elem["width"] = 50#len(elem["label"])* 3 #TODO find a more flexible solution

    def drawElem(self,elem,x,y,w=None,h=None):
        scn = bpy.context.scene
        #should I put the val here ?
        self.setVal(elem,elem["value"])
        self.current_layout.prop(scn, elem["name"].replace(" ","_"))        

    def drawString(self,elem,x,y,w=None,h=None):
        """ Draw a String input elem
        @type  elem: dictionary
        @param elem: the string input dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """   
#        print (elem["variable"])
    #        if elem["variable"] is not None :
        self.drawElem(elem,x,y,w=w,h=h)

#        print ("PANEL "+elem["name"].replace(" ","_"))
#        print(self.panel)
#        print (hasattr(self.panel,elem["name"].replace(" ","_")))
#        w,h = self.checkwh(elem,w,h)
#        args = (elem["name"], elem["id"],int(x), int(y), int(w), int(h),
#                elem["variable"].val,self.maxStrLenght,elem["tooltip"])
#        if self.subdialog :
#            elem["variable"]= self.check_addAction(Blender.Draw.String,
#                    elem["action"], *args)
#        else :
#            elem["variable"]= Blender.Draw.String(*args)
        pass
            
    def drawStringArea(self,elem,x,y,w=None,h=None):
        """ Draw a String Area input elem, ie multiline
        @type  elem: dictionary
        @param elem: the string area input dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """          
#        w,h = self.checkwh(elem,w,h)
#        Blender.BGL.glRasterPos2i(x,y+5)
#        Blender.Draw.Text(elem["value"])
        #this could be a Text creation instead
        elem["width"] = 0
        elem["height"] = 0
#        self.SetStringArea(elem,elem["value"])
#        texts = list(bpy.data.texts)
#        newText = [tex for tex in texts if tex.name == elem["name"]]
#        print newText
#        if not len(newText) :
#            newText = Blender.Text.New(elem["name"])
#        else :
#            newText[0].clear()
#            for line in elem["value"]: newText[0].write(line)

    def drawNumbers(self,elem,x,y,w=None,h=None):
        """ Draw a Int input elem
        @type  elem: dictionary
        @param elem: the Int input dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """    
        self.drawElem(elem,x,y,w=w,h=h)     
#        w,h = self.checkwh(elem,w,h)
#        w = max(w, Blender.Draw.GetStringWidth(elem["label"]))
#        #name, event, x, y, width, height, initial, min, max, tooltip=None, 
#        #callback=None, clickstep=None, precision=None
#        clickstep = elem["step"]*100
#        args = (elem["label"], elem["id"],int(x), int(y),\
#                int(w), int(h), elem["variable"].val, elem["mini"],\
#                elem["maxi"], elem["tooltip"], self.no_action, clickstep,\
#                elem["precision"])
#
#        if self.subdialog :
#            elem["variable"]= self.check_addAction(Blender.Draw.Number,
#                    elem["action"],i=-3, *args)
#        else  :
#            elem["variable"]= Blender.Draw.Number(*args)

    def drawFloat(self,elem,x,y,w=None,h=None):
        """ Draw a Int input elem
        @type  elem: dictionary
        @param elem: the Int input dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """  
        self.drawElem(elem,x,y,w=w,h=h)       
#        w,h = self.checkwh(elem,w,h)
#        w = max(w, int(Blender.Draw.GetStringWidth(elem["label"])))
#        clickstep = elem["step"]*100
#        #name, event, x, y, width, height, initial, min, max, tooltip=None, 
#        #callback=None, clickstep=None, precision=None
#        args = (elem["label"], elem["id"],int(x), int(y),\
#                int(w), int(h), elem["variable"].val, elem["mini"],\
#                elem["maxi"], elem["tooltip"], self.no_action, clickstep,\
#                elem["precision"])
#        
#        if self.subdialog :
#            elem["variable"] = self.check_addAction(Blender.Draw.Number,
#                    elem["action"],i=-3, *args)
#        else:
#            elem["variable"]= Blender.Draw.Number(*args)

    def drawError(self,errormsg=""):
        """ Draw a error message dialog
        @type  errormsg: string
        @param errormsg: the messag to display
        """  
#        Blender.Draw.PupMenu("ERROR: "+errormsg)
        bpy.ops.pyubic.dialog_message('INVOKE_DEFAULT',messageString = "ERROR: "+errormsg,
                                      width=300, height=300)
        return
        
    def drawQuestion(self,title="",question=""):
        """ Draw a Question message dialog, requiring a Yes/No answer
        @type  title: string
        @param title: the windows title       
        @type  question: string
        @param question: the question to display
        
        @rtype:   bool
        @return:  the answer     
        """            
        block=[]
        for line in question.split('\n'):
            if len(line) > 30 :
                block.append(line[0:28]+"-")
                block.append("-"+line[28:])
            else :
                block.append(line)
        bpy.ops.pyubic.dialog_message('INVOKE_DEFAULT',messageString = question,
                                      width=300, height=300)
        
        #return Blender.Draw.PupBlock(title, block)
        
    def drawMessage(self,title="",message=""):
        """ Draw a message dialog
        @type  title: string
        @param title: the windows title       
        @type  message: string
        @param message: the message to display   
        """            
#        block=[]
        #need to split the message, as windows length limited, 
        #31car
#        for line in message.split('\n'):
#            if len(line) >= 30 :
#                block.append(line[0:28]+"-")
#                block.append("-"+line[28:])
#            else :
#                block.append(line)
#        bpy.ops.('INVOKE_DEFAULT')
        bpy.ops.pyubic.dialog_message('INVOKE_DEFAULT',messageString = message,
                                      width=300, height=300)
#        retval = Blender.Draw.PupBlock(title, block)
        return

    def drawInputQuestion(self,title="",question="",callback=None):
        """ Draw an Input Question message dialog, requiring a string answer
        @type  title: string
        @param title: the windows title       
        @type  question: string
        @param question: the question to display
        
        @rtype:   string
        @return:  the answer     
        """                  
        result = None#Blender.Draw.PupStrInput(question, "", 100)
        if result :
            if callback is not None :
                callback(result)
            else :
                return result

    def getSelectTxt(self):
        """ specific function that proposed all text open in blender Text windows,
        and return the selected one from a pull-down menu
        """
        return
#        texts = list(bpy.data.texts)
#        textNames = [tex.name for tex in texts]
#        if textNames:
#            choice = Blender.Draw.PupMenu('|'.join(textNames))
#            if choice != -1:
#                text = texts[choice-1]
#                cmds=""
#                for l in text.asLines():
#                    cmds+=l+'\n'
#                return cmds
#        return None

    def drawSliders(self,elem,x,y,w=None,h=None):
        """ Draw a Slider elem, the variable/value of the elem define the slider format
        @type  elem: dictionary
        @param elem: the slider input dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """                
        w,h = self.checkwh(elem,w,h)
        scn = bpy.context.scene
        self.current_layout.prop(scn, elem["name"].replace(" ","_"),slider=True,event=True)        
        
        #(name, event, x, y, width, height, initial, min, max, 
        #realtime=1, tooltip=None, callback=None)
        #if elem["action"] is not None :
        #    elem["variable"]=Blender.Draw.Slider(elem["label"], elem["id"],x,y, 
        #            elem["width"]*self.scale, elem["height"]*self.scale,
        #            elem["variable"].val, elem["mini"], elem["maxi"],1,
        #            elem["tooltip"],elem["action"])#not sure about action..
        #else :
#        if self.subdialog :
#            elem["variable"] = self.check_addAction(Blender.Draw.Slider,
#                elem["action"], elem["label"], elem["id"], int(x), int(y), \
#                int(w), int(h), elem["variable"].val, elem["mini"], \
#                elem["maxi"], 0, elem["tooltip"])
#        else :#elem["label"]
#            elem["variable"] = Blender.Draw.Slider("", elem["id"], int(x),\
#                int(y), int(w), int(h), elem["variable"].val, elem["mini"],\
#                elem["maxi"], 0, elem["tooltip"])

    def drawImage(self,elem,x,y,w=None,h=None):
        """ Draw an Image, if the host supported it
        @type  elem: dictionary
        @param elem: the image input dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """           
        w,h = self.checkwh(elem,w,h)
        img = Blender.Image.Load(elem["value"])
        #we can add some gl call to make some transparency if we want
        #Blender.BGL.glEnable( Blender.BGL.GL_BLEND ) # Only needed for alpha blending images with background.
        #Blender.BGL.glBlendFunc(Blender.BGL.GL_SRC_ALPHA, Blender.BGL.GL_ONE_MINUS_SRC_ALPHA) 
        #Blender.BGL.glDisable( Blender.BGL.GL_BLEND )
        Blender.Draw.Image(img, x, y-h-10)#, zoomx=1.0, zoomy=1.0, clipx=0, clipy=0, clipw=-1, cliph=-1)

    def drawColorField(self,elem,x,y,w=None,h=None):
        """ Draw a Color entry Field
        @type  elem: dictionary
        @param elem: the color input dictionary
        @type  x: int
        @param x: position on x in the gui windows
        @type  y: int
        @param y: position on y in the gui windows
        @type  w: int
        @param w: force the width of the item
        @type  h: int
        @param h: force the height of the item
        """           
        w, h = self.checkwh(elem,w,h)
        scn = bpy.context.scene
        self.current_layout.prop(scn, elem["name"].replace(" ","_"))        
        
        #print "color",elem["id"], x, y, w, h, elem["variable"].val,elem["action"]
#        args = (elem["id"], int(x), int(y), int(w), int(h), elem["variable"].val)
#
#        if self.subdialog and elem["action"] is not None :
#            args += ("c", elem["action"])
#        elem["variable"]=Blender.Draw.ColorPicker(*args)
        #???COLOR???,
        #or a floatvectorProperti
#        self.current_layout.operator("pyubic.push",
#                                     text = elem["name"],
#                                     icon = "COLOR").modetype = self.uiname+"."+str(elem["id"])
                                    
    def handleSCrollEvent(self,evt,*args):
        if len(self.currentScroolbar):
            if self.currentScroolbar["value"] is not None :
                self.currentScroolbar["value"].buttonFilter(evt)
    
    def Tab_cb(self,*args):
        bloc = args[0]
        for tab in self.notebook :
#            print "O",tab["variable"].val
            if tab != bloc :
                tab["variable"].val = False
                tab["collapse"] = True                    
#                print "ok toggle",tab["name"]

    def drawTab(self,bloc,x,y):
        """
        Function to draw a block as a tab in a notebook layout of the gui. 
        
        @type  block: array or dictionary
        @param block: list or dictionary of item dictionary
        @type  x: int
        @param x: position on x in the gui windows, used for blender
        @type  y: int
        @param y: position on y in the gui windows, used for blender
        
        @rtype:   int
        @return:  the new horizontal position, used for blender
        """ 
        #scroll = self.use_scrollbar
        w = 45
        st= int(len(bloc["name"])*6.4)
        if st > w :
            w = st
        bloc["width"] = w
        scroll = False
        oriy = self.SubPosYInc - self.TitleHeight/2 - 10
        y = self.SubPosYInc - self.TitleHeight/2 - 10
        if y > self.top:
            y = self.top
#        print "top",y
        orix=x
#        print "left",x
        #print "0",x
        #print "1",self.notebook
        #print "2",bloc not in self.notebook
        if self.notebook is None:
            self.notebook=[]
        #position
        #x = x + pos
        if bloc not in self.notebook:
            for bl in self.notebook:
                x += bl["width"] + self.widgetGap
            self.notebook.append(bloc)
        else :
            for i in range(0,self.notebook.index(bloc)):
                bl = self.notebook[i]
                x += bl["width"] + self.widgetGap
            
        #print "3",self.notebook.index(bloc)
#        print x,y,oriy,bloc["id"],bloc["name"],bloc["width"]
        if bloc["variable"] is None :
            bloc["variable"] = self.addVariable("bool",False)
        #the toggle should addapt to the size of the string
#        print "size text fpr 45 b ",len(bloc["name"])
        bloc["variable"] = Blender.Draw.Toggle(bloc["name"],
                                bloc["id"], x, y,int(w),20,
                                bloc["variable"].val, 
                                bloc["tooltip"],
                                partial(self.Tab_cb,bloc))
        #find the size of the bloc on Y and decide if scroll is require
        
        size=0
        for i,blk in enumerate(bloc["elems"]):
            for j,item in enumerate(blk):
                size+=item["height"]*self.scale
#        print size
        if size > self.limit_scrollbar:
            scroll = True
        if scroll :
            if "scrollbar" not in bloc :
                bloc["scrollbar"] = self._addElemt(name=bloc["name"]+"scroll")
                bloc["scrollbar"]["variable"] = self.addVariable("int",1)
    #            bloc["scrollbar"]["y"] =  self.y
                bloc["scrollbar"]["up"] = bloc["scrollbar"]["id"]
                bloc["scrollbar"]["down"] = self.id 
                bloc["scrollbar"]["value"] = ReplacementScrollbar(0,0,100,bloc["scrollbar"]["up"],
                                              bloc["scrollbar"]["down"],sub= self.subdialog)
                self.id = self.id + 1 
     
            x = orix+20+self.widgetGap
        else :
            x = orix
        startx = x
        #top = y
        oriy = oriy - 30
        if bloc["variable"].val or not bloc["collapse"]:
#            print "click"
            if scroll :
                self.currentScroolbar = bloc["scrollbar"]
                if bloc["scrollbar"]["value"] is not None :
                    y = oriy + bloc["scrollbar"]["value"].getCurrentValue()*4
            for i,blk in enumerate(bloc["elems"]): #blk is a line
#                Blender.Draw.BeginAlign()
                draw = True
                y = y - 30
                if scroll :
                    if bloc["scrollbar"]["value"] is not None and \
                    (y < oriy - 200 or y > oriy-200+200) :
#                    print "not drawn"
                        draw =False
                for j,item in enumerate(blk):
                    if draw :
                        ButWidth = item["width"]*self.scale
                        ButtonHeight = item["height"]*self.scale
                        self._drawElem(item,x,y,ButWidth,ButtonHeight)
                        x= x + item["width"]*self.scale + 15
                x=startx
            if scroll :
                self.currentScroolbar["value"].draw(orix, oriy-200, 20, 200)
#            print "return ",-230
            return -230
        return 0

    def drawFrame(self,bloc,x,y):
        """
        Function to draw a block as a collapsable frame layout of the gui. 
        
        @type  block: array or dictionary
        @param block: list or dictionary of item dictionary
        @type  x: int
        @param x: position on x in the gui windows, used for blender
        @type  y: int
        @param y: position on y in the gui windows, used for blender
        
        @rtype:   int
        @return:  the new horizontal position, used for blender
        """            
#        if bloc["collapse"] :
#            collapse = c4d.BFV_BORDERGROUP_FOLD
#        else :
#            collapse = c4d.BFV_BORDERGROUP_FOLD|c4d.BFV_BORDERGROUP_FOLD_OPEN
#        self.GroupBegin(id=bloc["id"],title=bloc["name"],cols=1,
#                                flags=c4d.BFH_SCALEFIT | c4d.BFV_MASK,
#                                groupflags=collapse)
#        self.GroupBorder(c4d.BORDER_THIN_IN|c4d.BORDER_WITH_TITLE|c4d.BORDER_MASK)#c4d.BORDER_BLACK|
#        self.GroupBorderSpace(self.left, self.top, self.right, self.bottom)
        #collapse should be a boolean associate to button
        box = self.layout.box()
        toprow = box.row()
        scn = bpy.context.scene
#        self.current_layout.prop(scn, elem["name"].replace(" ","_"),slider=True,event=True)
#        self.current_layout = box
        cname = bloc["name"].replace(" ","_")+"_c"
        collapse = getattr(scn,cname)
        if  collapse :
            toprow.prop(scn, cname, icon="TRIA_RIGHT", icon_only=False,
                emboss=False)
        else :
            toprow.prop(scn, cname, icon="TRIA_DOWN", icon_only=False,
                emboss=False)
            for k,blck in enumerate(bloc["elems"]):
    #            cmds.rowLayout(numberOfColumns=len(blck))
#                self.startBlock(m=len(blck))
                self.current_layout = box.row()
                self.current_layout.alignment = 'LEFT'
                for index, item in enumerate(blck):
                    self._drawElem(item,x,y)
#                self.endBlock()
#        self.endBlock()
#        self.LayoutChanged(bloc["id"])
        return y

    def storeUIVar(self):
        scn = bpy.context.scene
        for block in self._layout:
            if type(block) is list :
                for elem in block:
                    propName = elem["name"].replace(" ","_")
#                    setattr(bpy.types.Scene,propName,bpy.props.FloatVectorProperty())
#                    setattr(bpy.types.Scene,propName+"_o",getattr(scn,propName))
                    if elem["type"] in ["inputStr","pullMenu","checkbox",
                        "sliders","slidersInt","inputInt","inputFloat"]:
                        setattr(self,propName+"_o",getattr(scn,propName))
            else : #dictionary: multiple line / format dict?
                if "0" in block:
                    for i in range(1,len(block)):
                        for elem in block[str(i)]:
                            propName = elem["name"].replace(" ","_")
#                            setattr(bpy.types.Scene,propName+"_o",getattr(scn,propName))
                            if elem["type"] in ["inputStr","pullMenu","checkbox",
                        "sliders","slidersInt","inputInt","inputFloat"]:
                                setattr(self,propName+"_o",getattr(scn,propName))                            
                else :                
                    for k,blck in enumerate(block["elems"]):
                        for index, item in enumerate(blck):
                            propName = item["name"].replace(" ","_")
#                            setattr(bpy.types.Scene,propName+"_o",getattr(scn,propName))
                            if item["type"] in ["inputStr","pullMenu","checkbox",
                        "sliders","slidersInt","inputInt","inputFloat"]:
                                setattr(self,propName+"_o",getattr(scn,propName))

    def isChanged(self,name):
        name = name.replace(" ","_")
        old = getattr(self,name+"_o")
        new = getattr(bpy.context.scene,name)
#        print (type(old),type(new))
#        print (old,new)
#        print (new != old)
        if new != old :
            print (name+" changed",old,new)
            setattr(self,name+"_o",new)
            return True
        return False

    def UpdateMenuData(self,blocklayout):
        """ special to update the frame layout """
#        global ButtonData, Filters
        selection       = ""
        
        if blocklayout is not None:
#            ArrayItem   = ButtonData[ArrayIndex]
            #Figure Buttons
            for index, item in enumerate(blocklayout["elems"]):
                buttonCount = len(blocklayout["elems"])
                if (buttonCount and index > buttonCount): break 
                #If buttonCount is specified stop drawing button list past count
                if (item["show"] == True): #Is button set to show
                    if (item["type"] == "pullMenu"): 
                        pass

    def SubFrame(self,blocklayout,x = 0, y = 100, width = 200): 
        """ this is the main code for drawing the collapsable frame
        layout, this code was taken from the Mosaic plugin for Blender"""
        
        #ArrayIndex is the index in ButtonData to the sub-window to draw in ButtonData array
        TitleHeight = 15
        TextOffset  = TitleHeight/2+4
        Bevel       = 6
        ArrowSize   = 4
        WindowGap   = self.widgetGap
        LineGap     = 15
        PosInc      = y
        showSection = True
        lineWidth   = width-WindowGap*2
        
        #Grab colors applied to standard areas of Blender so interface looks built in
        TitleColor  = Theme.Get()[0].get("BUTS").header     #Color of menu title
        TextColor   = [0,0,0]#Theme.Get()[0].get("BUTS").text_hi    #Color of submenu text
        TextColor2  = [0,0,0]#Theme.Get()[0].get("ui").menu_text    #Color of menu text
        TabColor    = [TitleColor[0]/4*3, TitleColor[1]/4*3, TitleColor[2]/4*3] #Color of System submenu tabs
        BackColor   = Theme.Get()[0].get("BUTS").panel      #Color of System submenu backgrounds
#        print blocklayout["wcolor"]
        blocklayout["wcolor"] = [1,1,1,1]
        #Collapse button if left mouse click in title subWindow title area
        if (self.MousePos[0] > x and self.MousePos[0] < x+width \
            and self.MousePos[1] > y-TitleHeight and self.MousePos[1] < y):
            blocklayout["collapse"] = not blocklayout["collapse"]
            self.MousePos = [0, 0]
        
        #Make sure menu data is revised for visible subs
#        if (not blocklayout["collapse"]): self.UpdateMenuData(blocklayout)
        
#        Blender.Draw.BeginAlign()
        #Draw Tab
        BGL.glColor3f(TabColor[0]/256.0*blocklayout["wcolor"][0], 
                      TabColor[1]/256.0*blocklayout["wcolor"][1],
                      TabColor[2]/256.0*blocklayout["wcolor"][2])
        BGL.glBegin(BGL.GL_POLYGON)
        BGL.glVertex2i(x, y-TitleHeight+Bevel)
        BGL.glVertex2i(x, y-Bevel)
        BGL.glVertex2i(x+Bevel/3, y-Bevel/3)
        BGL.glVertex2i(x+Bevel, y)
        BGL.glVertex2i(x+width-Bevel, y)
        BGL.glVertex2i(x+width-Bevel/3, y-Bevel/3)
        BGL.glVertex2i(x+width, y-Bevel)
        if blocklayout["collapse"]:          
            #Change titles bottom radius effect based on collapse state
            BGL.glVertex2i(x+width-Bevel/3, y-TitleHeight+Bevel/3)
            BGL.glVertex2i(x+width-Bevel, y-TitleHeight)
            BGL.glVertex2i(x+Bevel, y-TitleHeight)
            BGL.glVertex2i(x+Bevel/3, y-TitleHeight+Bevel/3)
        else:
            BGL.glVertex2i(x+width, y-TitleHeight)
            BGL.glVertex2i(x, y-TitleHeight)
        BGL.glEnd()
            
        PosInc      -= TitleHeight
        ButX        = x+WindowGap
        
        if (not blocklayout["collapse"]):      
            #Draw Buttons and Background according to Collapse state
            #Draw BackGround Top
            BGL.glEnable(BGL.GL_BLEND)
            BGL.glBlendFunc(BGL.GL_SRC_ALPHA, BGL.GL_ONE_MINUS_SRC_ALPHA)
            BGL.glColor4f(BackColor[0]/256.0*blocklayout["wcolor"][0], 
                          BackColor[1]/256.0*blocklayout["wcolor"][1], 
                          BackColor[2]/256.0*blocklayout["wcolor"][2], 
                          BackColor[3]/256.0*blocklayout["wcolor"][3])
            BGL.glRecti(x, PosInc, x+width, PosInc-WindowGap)
            BGL.glDisable(BGL.GL_BLEND)
            
            PosInc      -= WindowGap
            firstButton = True
            
            #Draw Buttons
            for k,block in enumerate(blocklayout["elems"]):
                #one block is one line
                ButX    = x+WindowGap    
                firstButton = True
                showSection = True
                availWidth  = lineWidth
                for index, item in enumerate(block):
                    buttonCount = len(block)
                    if (buttonCount and index > buttonCount): break 
                    #If buttonCount is specified stop drawing button list if past count
                    if (showSection == False and item["type"] != "line"): 
                        #If showSection is toggled off then hide all buttons up to next section line
                        item["show"] = False
                    else :
                        item["show"] = True
                    if item["show"]: 
                        #Is button set to show              
                        if False :#(firstButton):                       
                            #If first button of line cycle through the rest to 
                            #extract locked button widths from available line width
                            i           = index
                            availWidth  = lineWidth             
                            #Default available width to whole line
                            while firstButton:                  
                                #Look through buttons until end button is reached
    #                            print i,buttonCount
                                if i >= buttonCount : 
                                    break
                                if (block[i]["show"] == True): 
                                    #Only use visible buttons
                                    d  = block[i]["width"]
    #                                print d
                                    if (d > 1.0 and d < 100.0): 
                                        #If fixed width remove from available line width
                                        availWidth  -= d
                                    elif (d >= 100.0):          
                                        #If last button treat any value over 100 as 
                                        #fixed and break loop closing line
                                        availWidth  -= d-100.0
                                        firstButton = False
                                i+= 1
                        Trigger     = item["trigger"]
                        #Are there any special triggers on this button
                        Divider     = item["width"]*self.scale
                        #Get width ratio for this button
                        #ButWidth    = int(availWidth*Divider)  
                        #Figure button with divider as percent of window width
                        
                        #if (Divider > 1.0 and Divider < 100.0): 
                        #    ButWidth = int(Divider) 
                        #If over 1.0 then use as actual width instead of percent
                        #if (Divider >= 100.0):                  
                        #    ButWidth = int(x+width-WindowGap-ButX) 
                        #If last button set to tab width
                        ButWidth = item["width"]*self.scale#50#int(Divider) 
                        if (item["type"] == "line"): #If this is a line
                            if (Trigger):   ButtonHeight = LineGap
                            else:           ButtonHeight = WindowGap
                        else:               
                            ButtonHeight = item["height"]*self.scale#18   #Otherwise this is a button
                            if item["type"] == "inputStrArea":
                                ButtonHeight = 0    
                        
                        if (ButX == x+WindowGap):
                            #Draw Button BackGround
                            BGL.glEnable(BGL.GL_BLEND)
                            BGL.glBlendFunc(BGL.GL_SRC_ALPHA, BGL.GL_ONE_MINUS_SRC_ALPHA)
                            BGL.glColor4f(BackColor[0]/256.0*blocklayout["wcolor"][0], 
                                            BackColor[1]/256.0*blocklayout["wcolor"][1], 
                                            BackColor[2]/256.0*blocklayout["wcolor"][2], 
                                            BackColor[3]/256.0*blocklayout["wcolor"][3])
                            BGL.glRecti(x, PosInc, x+width, PosInc-ButtonHeight)
                            BGL.glDisable(BGL.GL_BLEND)
                            PosInc  -= ButtonHeight
                        if (item["type"] == "button"): 
                            #If this is supposed to be a button...
#                            print item["name"],ButX,PosInc,ButWidth,ButtonHeight
                            self.drawButton(item,ButX,PosInc,w=ButWidth, h=ButtonHeight)
                        elif (item["type"] == "label"): 
                            self.drawText(item,ButX,PosInc,w=ButWidth, h=ButtonHeight)
#                        elif item["type"] == "inputStrArea":
#                            ButtonHeight = 0
#                            self.drawStringArea(item,ButX,PosInc,w=ButWidth, h=ButtonHeight)
#                        elif (item["type"] == "pullMenu"): 
#                            #If this is supposed to be a list menu...
#                            #Draw menu description
#    #                        BGL.glColor3f(TextColor2[0]/256.0, TextColor2[1]/256.0, TextColor2[2]/256.0)
#    #                        BGL.glRasterPos2d(ButX, PosInc+5)
#    #                        if (Trigger):
#    #                            Text(ButtonData[ArrayIndex][WIN_BUTS][index][BUT_PROP], "normal")
#    #                            ButX        += Trigger
#    #                            ButWidth    -= Trigger
#    #                        #Draw Menu
#                            self.drawPMenu(item,ButX,PosInc,w=ButWidth,h=ButtonHeight)
#                        elif (item["type"] == "inputNbr"): 
#                            #If this is supposed to be a number button...
#                            pass
#    #                        ButtonData[ArrayIndex][WIN_BUTS][index][BUTTON] = Number(ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TITLE], ButtonData[ArrayIndex][WIN_EVENT]+index, ButX, PosInc, ButWidth, ButtonHeight, ButtonData[ArrayIndex][WIN_BUTS][index][BUTTON].val, ButtonData[ArrayIndex][WIN_BUTS][index][BUT_MIN], ButtonData[ArrayIndex][WIN_BUTS][index][BUT_MAX], ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TIP])
#                        elif (item["type"] == "checkbox"): 
#                            #If this is supposed to be a toggle button...
#                            if (Trigger == 9):                  
#                                #If toggle is using section hide trigger use 
#                                #button state to turn buttons section on and off
#                                showSection = item["variable"].val
#                            self.drawCheckBox(item,ButX,PosInc,w=ButWidth,h=ButtonHeight)                        
    #                    elif (ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TYPE] == 4): 
    #                        #If this is supposed to be a string button...
    #                        if (Trigger):                       #If text is all on one line separate description, otherwise show in text
    #                            #Draw text description
    #                            BGL.glColor3f(TextColor2[0]/256.0, TextColor2[1]/256.0, TextColor2[2]/256.0)
    #                            BGL.glRasterPos2d(ButX, PosInc+5)
    #                            Text(ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TITLE], "normal")
    #                            ButX        += Trigger
    #                            ButWidth    -= Trigger
    #                            ButtonData[ArrayIndex][WIN_BUTS][index][BUTTON] = String("", ButtonData[ArrayIndex][WIN_EVENT]+index, ButX, PosInc, ButWidth, ButtonHeight, ButtonData[ArrayIndex][WIN_BUTS][index][BUTTON].val, ButtonData[ArrayIndex][WIN_BUTS][index][BUT_MAX], ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TIP])
    #                        else:
    #                            ButtonData[ArrayIndex][WIN_BUTS][index][BUTTON] = String(ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TITLE], ButtonData[ArrayIndex][WIN_EVENT]+index, ButX, PosInc, ButWidth, ButtonHeight, ButtonData[ArrayIndex][WIN_BUTS][index][BUTTON].val, ButtonData[ArrayIndex][WIN_BUTS][index][BUT_MAX], ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TIP])
    #                    elif (ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TYPE] == 5): 
    #                        #If this is supposed to be a line...
    #                        EndAlign()
    #                        showSection     = True              
    #                        #Make all line types determine a new section and therefore 
    # turn section on automatically
    #                        if (Trigger):                       
    #                            #Only draw line if trigger is set
    #                            BGL.glColor3f(TabColor[0]/256.0*ButtonData[ArrayIndex][WIN_COLOR][0], TabColor[1]/256.0*ButtonData[ArrayIndex][WIN_COLOR][1], TabColor[2]/256.0*ButtonData[ArrayIndex][WIN_COLOR][2])
    #                            endGap      = 5
    #                            BGL.glLineWidth(1)
    #                            BGL.glBegin(BGL.GL_LINES)
    #                            BGL.glVertex2i(x+endGap, PosInc+2)
    #                            BGL.glVertex2i(x+width-endGap, PosInc+2)
    #                            BGL.glEnd()
    #                            BGL.glRasterPos2d(x+WindowGap, PosInc+4)
    #                            Text(ButtonData[ArrayIndex][WIN_BUTS][index][BUT_TITLE], "small")
    #                        BeginAlign()
                        else :
                            self._drawElem(item,ButX,PosInc,w=ButWidth,h=ButtonHeight)
#                            if item["type"]=="label":
#                                ButX = ButWidth = len(item["label"])*3.
#                        if (Divider >= 100.0):
#                            ButX    = x+WindowGap               
#                            #If this is the last button on the line...
#                            firstButton = True
#                        else:
#                            ButX    += ButWidth                 
#                            #Otherwise set next button to the end of last
                        ButX    += ButWidth+WindowGap
#                if len(blocklayout["elems"]) > 1 and k < len(blocklayout["elems"]):
                    #new line
                ButX    = x+WindowGap    
                firstButton = True
#                Blender.Draw.EndAlign()
                showSection     = True
#                Blender.Draw.BeginAlign()
            #Draw BackGround Bottom
            BGL.glEnable(BGL.GL_BLEND)
            BGL.glBlendFunc(BGL.GL_SRC_ALPHA, BGL.GL_ONE_MINUS_SRC_ALPHA)
            BGL.glColor4f(BackColor[0]/256.0*blocklayout["wcolor"][0], 
                            BackColor[1]/256.0*blocklayout["wcolor"][1], 
                            BackColor[2]/256.0*blocklayout["wcolor"][2], 
                            BackColor[3]/256.0*blocklayout["wcolor"][3])
            BGL.glRecti(x, PosInc, x+width, PosInc-WindowGap)
            BGL.glDisable(BGL.GL_BLEND)
            PosInc = PosInc-WindowGap
       
        else :
            for block in blocklayout["elems"]:
                for item in block:
                    item["show"] = False
        BGL.glColor3f(TextColor[0]/256.0, TextColor[1]/256.0, TextColor[2]/256.0)
        #Draw Arrow (rotate 90deg according to collapse boolean state)
        BGL.glPushMatrix()
        BGL.glTranslated(x+3*4, y-TitleHeight/2-1, 0)
        BGL.glRotated(-90*blocklayout["collapse"], 0, 0, -1)
        BGL.glBegin(BGL.GL_POLYGON)
        BGL.glVertex2i(0, -ArrowSize)
        BGL.glVertex2i(-ArrowSize, ArrowSize)
        BGL.glVertex2i(ArrowSize, ArrowSize)
        BGL.glEnd()
        BGL.glPopMatrix()
        
        #Draw Tab Text
        BGL.glRasterPos2d(x+4*6, y-TextOffset)
        Blender.Draw.Text(blocklayout["name"], "small")
        Blender.Draw.EndAlign()
#        print y,PosInc
        return y-PosInc                             #Return the final height of sub-window

    def fileDialog_cb(self, filename):
        self.fileDresult = filename
    
    def fileDialog(self, label="", callback=None, suffix=""):
        """ Draw a File input dialog
        @type  label: string
        @param label: the windows title       
        @type  callback: function
        @param callback: the callback function to call
        @type  suffix: string
        @param suffix: suffix of filename
        #work only in main windows..? not from a pull down menu.how to triger?
        """ 
        if callback is None :
            callback = self.fileDialog_cb
        idname = "pyubic.%s" % (self.uiname.lower()+label.lower().replace(" ","_"))
        classname = self.uiname+label.lower().replace(" ","_")
        print ("callback is ",callback)
        #how to change the exec?
        ldic = locals()
        gdic = globals()
        ldic["callback"] = callback
        gdic["callback"] = callback
        clascode = ""
#        if not hasattr(bpy.ops,idname) :
        clascode += "class fileDialog%s (bpy.types.Operator):\n" % classname
        clascode += "    bl_label = '%s'\n" % label
        clascode += "    bl_idname =   '%s'\n" %  idname
        clascode += "    filepath = bpy.props.StringProperty()\n"
        clascode += "    def invoke(self, context, event):\n"
        clascode += "        wm = context.window_manager\n"
        clascode += "        wm.fileselect_add(self)\n"
        clascode += "        return {'RUNNING_MODAL'}\n"
        clascode += "    def execute(self,context):\n"
        clascode += "        if callback:\n"
        clascode += "            print ('callback',self.filepath)\n"
        clascode += "            callback(self.filepath)\n"
        clascode += "        else : print ('filename ',self.filepath)\n"
        clascode += "        return {'FINISHED'}\n"
        clascode += "bpy.utils.register_class(fileDialog%s)\n" % classname
        clascode += "bpy.ops.%s('INVOKE_DEFAULT')\n" % idname
        exec(clascode, gdic,ldic)
        #exec(codeString, globals(), locals())
        
#        
#        def fileCB(ww,context,*args):
#            print (args)
#            print (ww.filepath)
#            if callback:
#                #filepath dont work ?
##                f = open(ww.filepath,"r")
##                f.close()
#                callback(ww.filepath)
#            return {'FINISHED'}
            
#        idname = "pyubic.%s" % ("filedial1")
#        opclass = type("fileDialog%s" % (self.uiname), (FILEBROWSER_PT_General, ), {"bl_idname": idname,
#                                                                    "bl_label": "Open PDB",
#                                                                    "execute":fileCB})
#        bpy.utils.register_class(opclass)
#        bpy.ops.pyubic.filedial1('INVOKE_DEFAULT')
#        bpy.ops.pyubic.filedialog('INVOKE_DEFAULT',label=label)
#        if callback is not None :
#            Blender.Window.FileSelector (callback, label, suffix)
#        else :
#            Blender.Window.FileSelector (self.fileDialog_cb, label, suffix)
#            return self.fileDresult

    def saveDialog(self,label="",callback=None, suffix=""):
        """ Draw a File input dialog
        @type  label: string
        @param label: the windows title       
        @type  callback: function
        @param callback: the callback function to call
        """     
        self.fileDialog(label=label,callback=callback,suffix=suffix)
#        if callback is not None:
#            Blender.Window.FileSelector (callback, label, suffix)
#        else :
#            Blender.Window.FileSelector (self.fileDialog_cb, label, suffix)
#            return self.fileDresult
            
    def waitingCursor(self,toggle):
        """ Toggle the mouse cursor appearance from the busy to idle.
        @type  toggle: Bool
        @param toggle: Weither the cursor is busy or idle 
        """             
        pass
#        Blender.Window.WaitCursor(toggle)

    def getString(self,elem):
        """ Return the current string value of the String Input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        
        @rtype:   string
        @return:  the current string input value for this specific elem
        """            
        scn = bpy.context.scene
        return getattr(scn,elem["name"].replace(" ","_")) #str(elem["variable"].val)

    def setString(self,elem,val):
        """ Set the current String value of the string input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        @type  val: string
        @param val: the new string value    
        """
        scn = bpy.context.scene       
        if elem["type"] == "label":
            elem["label"] = str(val)
        else :
            setattr(scn,elem["name"].replace(" ","_"),str(val))

    def getStringArea(self,elem):
        """ Return the current string area value of the String area Input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        
        @rtype:   string
        @return:  the current string area input value for this specific elem
        """                
        return self.getSelectTxt()

    def SetStringArea(self,elem,val):
        """ Set the current String area value of the string input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        @type  val: string
        @param val: the new string value (multiline)   
        """                
        
        texts = list(bpy.data.texts)
        newText = [tex for tex in texts if tex.name == elem["name"]]
#        print newText
        if not len(newText) :
            newText = None#Blender.Text.New(elem["name"])
        else :
            newText[0].clear()
            newText=newText[0]
        for line in val : newText.write(line)
        elem["value"] = val
        
    def getLong(self,elem):
        """ Return the current Int value of the Input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        
        @rtype:   Int
        @return:  the current Int value input for this specific elem
        """   
        scn = bpy.context.scene
        val = getattr(scn,elem["name"].replace(" ","_"))
        if elem["type"] == "pullMenu":
            print ("menu",elem)
            print ("value",val)
            
            return int(val) #for menu...as its start at 1
        else :
            return int(getattr(scn,elem["name"].replace(" ","_")))

        
    def setLong(self,elem,val):
        """ Set the current Int value of the Int input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        @type  val: Int
        @param val: the new Int value
        """ 
        scn = bpy.context.scene
        if elem["type"] == "pullMenu":
            propName = elem["name"].replace(" ","_")
            lMenu=[]
            for i,m in enumerate(elem["value"]) :
                l = (str(i),m,m)
                lMenu.append(l)#return,name,description
            print ("default",elem["value"][val])
            if elem["action"] is not None :
                setattr(bpy.types.Scene,propName,
                    bpy.props.EnumProperty(items=lMenu,name=elem["name"],
                    #default=elem["value"][val],
                    update=self.makeUpdateFunction(elem["action"])))
            else :
                setattr(bpy.types.Scene,propName,
                    bpy.props.EnumProperty(items=lMenu,
                        #default=elem["value"][val],
                        name=elem["name"],
                        update=checkUIVar))            
        else :
            setattr(scn,elem["name"].replace(" ","_"),int(val))
            
    def getReal(self,elem):
        """ Return the current Float value of the Input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        
        @rtype:   Float
        @return:  the current Float value input for this specific elem
        """ 
        scn = bpy.context.scene 
        return float(getattr(scn,elem["name"].replace(" ","_")))
#        if elem["type"] == "sliders":
#            #check if float or int !
#            print(type(elem["variable"].val))
#            if type(elem["variable"].val) is int :
#                return int(elem["variable"].val)
#            else :
#                return float(elem["variable"].val)
#        else :
#            return float(elem["variable"].val)

    def setReal(self,elem,val):
        """ Set the current Float value of the Float input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        @type  val: Float
        @param val: the new Float value
        """     
        #scn = bpy.context.scene
        #setattr(scn,elem["name"].replace(" ","_"),float(val))
        self.addVariablePropToSc(elem,"float",val)
        
    def getBool(self,elem):
        """ Return the current Bool value of the Input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        
        @rtype:   Bool
        @return:  the current Bool value input for this specific elem
        """   
        scn = bpy.context.scene        
        return bool(getattr(scn,elem["name"].replace(" ","_")))
        
    def setBool(self,elem,val):
        """ Set the current Bool value of the Bool input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        @type  val: Bool
        @param val: the new Bool value
        """     
        scn = bpy.context.scene
        setattr(scn,elem["name"].replace(" ","_"),bool(val))

    def getColor(self,elem):
        """ Return the current Color value of the Input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        
        @rtype:   Color
        @return:  the current Color array RGB value input for this specific elem
        """                        
        scn = bpy.context.scene        
        color = getattr(scn,elem["name"].replace(" ","_"))
        return (color[0],color[1],color[2])

    def setColor(self,elem,val):
        """ Set the current Color rgb arrray value of the Color input elem
        @type  elem: dictionary
        @param elem: the elem input dictionary       
        @type  val: Color
        @param val: the new Color value
        """        
        scn = bpy.context.scene
        setattr(scn,elem["name"].replace(" ","_"),val)

    def updateSlider(self,elem,mini,maxi,default,step):
        """ Update the state of the given slider, ie format, min, maxi, step
        @type  elem: dictionary
        @param elem: the slider elem dictionary       
        @type  maxi: int/float
        @param maxi: max value for the item, ie slider
        @type  mini: int/float
        @param mini: min value for the item, ie slider
        @type  default: int/float
        @param default: default value for the item, ie slider
        @type  step: int/float
        @param step: step value for the item, ie slider
        """      
        ##should change the slider property   
        updateF = self.makeUpdateFunction(elem["action"])
        if updateF == None :
            updateF = checkUIVar
        elem["maxi"] = maxi
        elem["mini"] = mini
#        elem["default"] = 
        elem["step"] = step
        propName = elem["name"].replace(" ","_")
        if elem["value"] is None :
            elem["value"] = mini
        if type(step) is int :
            setattr(bpy.types.Scene,propName,
                                bpy.props.IntProperty(default=int(elem["value"]), 
                                min=elem["mini"], max=elem["maxi"], 
                                #soft_min=elem["mini"], soft_max=elem["maxi"], 
                                step=elem["step"], update=updateF))
        else :
            setattr(bpy.types.Scene,propName,
                                bpy.props.FloatProperty(default=float(elem["value"]), 
                                precision = int(elem["precision"]),
                                min=float(elem["mini"]), max=float(elem["maxi"]), 
                                #soft_min=elem["mini"], soft_max=elem["maxi"], 
                                step=elem["step"], update=updateF))
        
    def updateViewer(self):
        """
        update the 3d windows if any
        """
        pass
#        Blender.Scene.GetCurrent().update()
#        Blender.Draw.Redraw()
#        Blender.Window.RedrawAll()
#        Blender.Window.QRedrawAll()  
#        Blender.Redraw()

    def _restore(self,rkey,dkey=None):
        """
        Function used to restore the windows data, usefull for plugin
        @type  rkey: string
        @param rkey: the key to access the data in the registry/storage       
        @type  dkey: string
        @param dkey: wiether we want a particular data from the stored dic
        """
        if hasattr(bpy,rkey):
            obj = bpy.__dict__[rkey]
            if dkey is not None:
                if dkey in bpy.__dict__[rkey] :
                    return  bpy.__dict__[rkey][dkey]       
                else :
                    return None
            return obj
        else :
            return None


    def _store(self,rkey,dict):
        """
        Function used to store the windows data, usefull for plugin
        @type  rkey: string
        @param rkey: the key to access the data in the registry/storage       
        @type  dict: dictionary
        @param dict: the storage is done throught a dictionary
        """     
        bpy.__dict__[rkey]= dict
        
    def close(self,*args):
        """ Close the windows"""
        if not self.subdialog :
#            print ("try to remove %s"%self.uiname)
#            bpy.utils.unregister_class(type(bpy.myGuiui.panel))
            exec("bpy.utils.unregister_class(type(bpy.%s.panel))"%self.uiname)
        else :
            #should stop drawing it
            self.drawUIblock = False
#
#    def drawSubDialogUI(self):
#        Blender.Draw.UIBlock(self._createLayout, mouse_exit=0)

    def drawSubDialog(self,dial,id,callback=None,asynchro = True):
        """
        Draw the given subdialog whit his own element and callback
        
        @type  dial: dialog Object
        @param dial: the dialog object to be draw
        @type  id: int
        @param id: the id of the dialog
        @type  callback: function
        @param callback: the associate callback
        """        
        #dial is an object
#        print ("do i have a panel",dial.panel)
#        print ("do i have a panel id",dial.panel.bl_idname)
#        operator = getattr(bpy.ops,dial.panel.bl_idname)
#        operator('INVOKE_DEFAULT')
        setattr(bpy,dial.uiname,dial)
        bpy.ops.pyubic.subdialog('INVOKE_DEFAULT',subdialname=dial.uiname)

#        
#        sub=[]
#        if dial.block  :
#            dial.drawUIblock = True
#            #need per button callback...
#            x,y=Blender.Window.GetMouseCoords()
#            dial.x = y
#            dial.y = x
#            while dial.drawUIblock:
#                Blender.Draw.UIBlock(dial._createLayout,0)#self.drawSubDialogUI()
#            return
#        for block in dial._layout:
#            for elem in block :
#                if elem["type"] == "inputInt":
##                    print "elem", elem["name"]
#                    sub.append((elem["name"],elem["variable"],elem["mini"],elem["maxi"]))
#                elif elem["type"] == "label":
#                    sub.append(elem["label"])
#                elif elem["type"] == "checkbox":
#                    sub.append((elem["name"],elem["variable"]))
##                elif elem["type"] == "button"  :
##                    sub.append((elem["name"],elem["variable"]))
##        print sub
#        retval = Blender.Draw.PupBlock(dial.title, sub)
##        print retval
#        if callback is not None:
#            callback()
#        else :
#            return retval
#        #apply the command?

    def display(self):
        """ Create and Open the current gui windows """        
        #Blender.Draw.Register(self.CreateLayout, self.CoreMessage, self.Command)
        #    Registration

        panelCode =""
        panelCode+="class %s (bpy.types.Panel):\n" % self.uiname
        panelCode+="    bl_label = '%s'\n" % self.title
        panelCode+="    bl_space_type = '%s'\n" % self.space_type
        panelCode+="    bl_region_type = '%s'\n" % self.region_type
        
        panelCode+="    def draw(self, context):\n"       
        panelCode+="        dial = bpy.%s\n" % self.uiname
        panelCode+="        dial.panel = self\n"   
        panelCode+="        dial.layout = self.layout\n"   
        panelCode+="        dial.current_layout = self.layout\n"   
        panelCode+="        bpy.current_gui = dial\n"   
        panelCode+="        dial.CreateLayout()\n"   
        panelCode+="bpy.utils.register_class(%s)\n" % self.uiname
        exec(panelCode)
#        print (panelCode)
        
    def getDirectory(self):
        """return software directory for script and preferences"""
        #bpy.app.binary_path
        #bpy.utils.user_resource
        #bpy.context.user_preferences.filepaths.script_directory
        self.softdir = os.path.abspath(Blender.Get("homedir"))
        self.prefdir = Blender.Get('uscriptsdir')
        if self.prefdir is None:
            self.prefdir = Blender.Get('scriptsdir')
        self.prefdir =os.path.abspath( self.prefdir)
        
class blenderUIDialog(blenderUI,uiAdaptor):
    def __init__(self,**kw):
#        print ("initADGUI",kw)
        if "title" in kw.keys():
            self.title= kw["title"]
        else :
            self.title= "pyubic_blenderUI"
        self.SetTitle(self.title)    
        print ("title",self.title)
#
#class blenderUISubDialog(blenderUIDialog):
#    def __init__(self,name):
#        blenderUIDialog.__init__(self,)
#        #a subdialog is a popup
#        self.name = name
#        self.elems = []
#        self.result = None
#    
#    def draw(self):
#        self.result = Blender.Draw.PupBlock(self.name, self.elems)
#


