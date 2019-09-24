# ControlTool
Mercedes James
9/21/19

This program will create a GUI called create controls that will have 2 buttons 
that will create IK or FK controls on selected joints

The FK button will place a self grouped control on each selected joint.
The control and the group will have frozen transformations

The IK will create an IK handle at the end joint of the selected list with a self grouped control 
that will have frozen transformations. It will also parent constrain the control node to the IK Handle
It then will create another self grouped control with frozen transformations on the 2ed joint in the list.
It will then transverse through the list and find the IK handle and then place a pole vector constraint from 
the control to the IK handle.
