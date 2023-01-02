# Frame Ranger

![Banner](https://user-images.githubusercontent.com/79613445/210191095-3b92a11b-3381-43d1-9fd5-18fdff878874.png)

Frame Ranger is a blender add-on that helps manages Object's Action, Timeline Markers, Frame Range and more

[FrameRangerDemo.webm](https://user-images.githubusercontent.com/79613445/210191135-78bbee31-6083-4f70-90ab-9d14201328db.webm)

This Add-on Consist of Multiple Sections, You can Turn On / Off Based On Your Needs in the Preferences

## Feature Overview

### Object Action Manager

Stores Actions in Object so that you can associate actions to a object, and switch the object's action easily. It Also Comes With Many Other Feature that can be useful

![Object Action Manager](https://BlenderBoi.com/gallery/FrameRanger/ObjectActionManager.png)

	Important: This does not work on linked library override`


#### Action Switching

Quickly Switch Object's Action, and setting the frame range to the action's first and last keyframe or manual frame range settings. 

![Action Switching](https://BlenderBoi.com/gallery/FrameRanger/ActionSwitching.gif)

#### Import FBX Action

Frame Ranger comes with a wrapper operator that import fbx and remove everything other than the actions, that means you will only import the action instead while other stuff that imported from the fbx will be discarded.

The Action is then Loaded to Object Action Manager. You have the option to use the Build In Import FBX.

This can be useful for combining multiple mixamo fbx into one for game engine use. 

![Import FBX Action](https://BlenderBoi.com/gallery/FrameRanger/ImportFBXAction.gif)

## Action Bin

List Out All the Actions in the Blender File, and helps managing it by providing some basic feature to work on them. 

![Action Bin](https://BlenderBoi.com/gallery/FrameRanger/ActionBin.png)

## Auto Frame Range

Automatically Set Frame Range to the first and last key frames when turned on, Works on Object's Action, NLA Strips and Video Sequencer Strips

![Auto Frame Range Menu](https://BlenderBoi.com/gallery/FrameRanger/AutoFrameRangeMenu.png)

| Action Mode | NLA Mode | Sequencer Mode |
| -- | -- | -- |
| ![Action Auto Frame Range](https://BlenderBoi.com/gallery/FrameRanger/ActionAutoFrameRange.gif) | ![NLA Auto Frame Range](https://BlenderBoi.com/gallery/FrameRanger/NLAAutoFrameRange.gif) | ![Sequencer Auto Frame Range](https://BlenderBoi.com/gallery/FrameRanger/SequencerAutoFrameRange.gif) |

## Animation Player

Adds the Animation Player Buttons (Play, Pause etc...) and Frame Range Settings from Timeline Editor to Dopesheet, Graph Editor, NLA Editor and Video Sequencer

![Animation Player](https://BlenderBoi.com/gallery/FrameRanger/AnimationPlayer.png)

### Frame Range Manager

Stores Frame Range in a List so that you can Switch Frame Ranges Easily

![Frame Range Manager](https://BlenderBoi.com/gallery/FrameRanger/FrameRangeManager.png)

#### Frame Range Switching

This Can Be Useful to Breakdown a Scene to Multiple Chunk and Work on it Without Manually Typing in the Frame Numbers.

![Frame Range Switching](https://BlenderBoi.com/gallery/FrameRanger/FrameRangeSwitching.gif)

The Frame Ranges Can Be Exported and Imported into other Blend Files.

### Timeline Markers Manager

Presents Timeline Markers In A list form as well as adding some operators that make timeline markers more useful, by allowing it to be easily created, bind to camera, or jump to marker. 

![Timeline Markers Panel](https://BlenderBoi.com/gallery/FrameRanger/TimelineMarkersPanel.png)

### Import / Export Marker

You can Import and Export Timeline Markers between blend files

![IO Timeline Markers](https://BlenderBoi.com/gallery/FrameRanger/IOTimelineMarkers.png)

### Jump To Markers

Jump Current Frame to Markers

![Jump To Marker](https://BlenderBoi.com/gallery/FrameRanger/JumpToMarker.gif)


