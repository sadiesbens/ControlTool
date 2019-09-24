import maya.cmds as cmds


'''Mercedes James
This program will create a GUI called create controls that will have 2 buttons 
that will create IK or FK controls on selected joints

The FK button will place a self grouped control on each selected joint.
The control and the group will have frozen transformations

The IK will create an IK handle at the end joint of the selected list with a self grouped control 
that will have frozen transformations. It will also parent constrain the control node to the IK Handle
It then will create another self grouped control with frozen transformations on the 2ed joint in the list.
It will then transverse through the list and find the IK handle and then place a pole vector constraint from 
the control to the IK handle.
'''
#put selected in list, for each in list
selectedJoints=cmds.ls(selection=True)


#Make FK Ctrls
def makeCtrls(jnt):
    
    #place selected jnts into list
    selJnts = cmds.ls(sl=True)
    for jnt in selJnts:
       
   
       #create nurbs circle(ctrl)
       controlx=cmds.circle(n=jnt + '_ctrl')
       #rotate and scale
       cmds.xform(ro=(90,0,0), s=(4.5,4.5,4.5))
       #selfGroup and name after joint
       grp=cmds.group(n=jnt + '_ctrl_grp')#*******I
       #position ctrl on selected joint
       con=cmds.parentConstraint( jnt, controlx[0] )
       cmds.delete(con)
       #freeze transformations of ctrl
       cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
       #position grp on selected joint
       cmds.copyAttr(controlx[0],grp,v=True,at=['tx','ty','tz'])
       #center piviot of grp
       cmds.xform(cp=True)
       #freeze transformations of grp
       cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    return









#make IK Ctrls
def makeIK(jnt):

    #created IK handle
    IkHandle=cmds.ikHandle(n=(jnt[-1]+'IK'), sj=jnt[0], ee=jnt[-1] )

   
    #create and place self grouped ctrl
    #create nurbs circle(ctrl)
    controlx=cmds.circle(n=jnt[-1]+'_IKCtrl')
    #rotate and scale
    cmds.xform(ro=(90,0,0), s=(4.5,4.5,4.5))
    #selfGroup and name
    grp=cmds.group(n=jnt[-1]+ '_IKctrl_grp')
    #position ctrl on IKHandle
    con=cmds.parentConstraint(IkHandle, controlx[0])
    cmds.delete(con)
    #freeze transformations of ctrl
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    #position grp on control
    cmds.copyAttr(controlx[0],grp,v=True,at=['tx','ty','tz'])
    #center piviot of grp
    cmds.xform(cp=True)
    #freeze transformations or grp
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    
    
    #constrain ctrl to IKhandle using parent constraint
    conx=cmds.parentConstraint( controlx[0], IkHandle[0])
    
    makePolVec(jnt)
   
 
    
    return
#make polVec Ctrls    
def makePolVec(jnts):
    print jnts
    #create ctrl
    controlx=cmds.circle(n=jnts[0] + '_polVec_ctrl')
    #rotate and scale
    cmds.xform(ro=(90,0,0), s=(4.5,4.5,4.5))
    #selfGroup and name after joint
    grp=cmds.group(n=jnts[0] + '_polVec_ctrl_grp')#*******I

    
    #point constrain
    for each in jnts:
        con1=cmds.pointConstraint(jnts,controlx)
       
    #aim constrain
    con2=cmds.aimConstraint(jnts[1],controlx,aim=(1,0,0))
    #selectConstraints
    cmds.select(con1,con2)
    #delete constraints
    cmds.delete(cn=True)
    #move control
    cmds.select(controlx)
  
    #move ctrl up
    cmds.xform(r=True,os=True,t=(5,0,0))
    
    
    #PolVec Constraint to IK Handle
    
    handle=cmds.listConnections(jnts[0],type='ikHandle')
    cmds.poleVectorConstraint(controlx,handle)
   
   
        
        
    return
    








#create Gui
win = cmds.window(title ='Create Controls')
layout = cmds.rowColumnLayout(adjustableColumn=True)
cmds.text(label ='Please select joints then choose FK or IK controls')
cmds.button(label='FK', command ='makeCtrls(selectedJoints)')
cmds.button(label='IK', command='makeIK(selectedJoints)')



cmds.showWindow()  