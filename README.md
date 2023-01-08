# Frame Ranger

Changes

![Banner](https://user-images.githubusercontent.com/79613445/210191095-3b92a11b-3381-43d1-9fd5-18fdff878874.png)

Frame Ranger is a blender add-on that helps manages Object's Action, Timeline Markers, Frame Range and more

[FrameRangerDemo.webm](https://user-images.githubusercontent.com/79613445/210191135-78bbee31-6083-4f70-90ab-9d14201328db.webm)

This Add-on Consist of Multiple Sections, You can Turn On / Off Based On Your Needs in the Preferences

## Feature Overview

### Object Action Manager

Stores Actions in Object so that you can associate actions to a object, and switch the object's action easily. It Also Comes With Many Other Feature that can be useful

![ObjectActionManager](https://user-images.githubusercontent.com/79613445/210191176-855d314d-d87a-455a-a714-84e96027ff3a.png)

	Important: This does not work on linked library override`


#### Action Switching

Quickly Switch Object's Action, and setting the frame range to the action's first and last keyframe or manual frame range settings. 

[ActionSwitching.webm](https://user-images.githubusercontent.com/79613445/210191201-c41278ab-1ed3-4a00-9da7-403c2e4e10f3.webm)


#### Import FBX Action

Frame Ranger comes with a wrapper operator that import fbx and remove everything other than the actions, that means you will only import the action instead while other stuff that imported from the fbx will be discarded.

The Action is then Loaded to Object Action Manager. You have the option to use the Build In Import FBX.

This can be useful for combining multiple mixamo fbx into one for game engine use. 

[ImportFBX.webm](https://user-images.githubusercontent.com/79613445/210191369-fdda382e-4495-4559-9b3e-fc2894c10496.webm)

## Action Bin

List Out All the Actions in the Blender File, and helps managing it by providing some basic feature to work on them. 

![ActionBin](https://user-images.githubusercontent.com/79613445/210191216-10c557fa-7bdd-4cf8-9490-e3b9d59a1567.png)

## Auto Frame Range

Automatically Set Frame Range to the first and last key frames when turned on, Works on Object's Action, NLA Strips and Video Sequencer Strips

![AutoFrameRangeMenu](https://user-images.githubusercontent.com/79613445/210191225-06f01856-d53c-46e9-8966-13f364424f40.png)


[ActionAutoFrameRange.webm](https://user-images.githubusercontent.com/79613445/210191258-e58cf949-52a3-4fd9-af17-9ea57db00277.webm)

[NLAAutoFrameRange.webm](https://user-images.githubusercontent.com/79613445/210191261-ca3160e7-e4c1-43ca-9830-73eacea57497.webm)

[SequencerAutoFrameRange.webm](https://user-images.githubusercontent.com/79613445/210191267-ac2046db-1324-4114-b9e8-343722610109.webm)


## Animation Player

Adds the Animation Player Buttons (Play, Pause etc...) and Frame Range Settings from Timeline Editor to Dopesheet, Graph Editor, NLA Editor and Video Sequencer

![AnimationPlayer](https://user-images.githubusercontent.com/79613445/210191273-35d55325-388f-42f0-8857-68995f3b68a2.png)


### Frame Range Manager

Stores Frame Range in a List so that you can Switch Frame Ranges Easily

![FrameRangeManager](https://user-images.githubusercontent.com/79613445/210191276-4b9641ae-3dc3-43a5-bb6f-fa0b68953ef6.png)

#### Frame Range Switching

This Can Be Useful to Breakdown a Scene to Multiple Chunk and Work on it Without Manually Typing in the Frame Numbers.

[FrameRangeSwitching.webm](https://user-images.githubusercontent.com/79613445/210191284-b86f0264-b3d3-487c-b296-a28b5b37464f.webm)

The Frame Ranges Can Be Exported and Imported into other Blend Files.

### Timeline Markers Manager

Presents Timeline Markers In A list form as well as adding some operators that make timeline markers more useful, by allowing it to be easily created, bind to camera, or jump to marker. 

![TimelineMarkersPanel](https://user-images.githubusercontent.com/79613445/210191291-6594d227-8588-4ba3-b14c-a5a51245fbd5.png)


### Bind Camera From View to Marker

Create Marker at Current Frame, Create Camera at Camera View and bind Camera to Marker

[CreateAndBindCamera.webm](https://user-images.githubusercontent.com/79613445/210191399-8ca0d6f2-6eac-4503-9206-dce8078c99a3.webm)


### Import / Export Timeline Marker

You can Import and Export Timeline Markers between blend files

[IOTimelineMarker.webm](https://user-images.githubusercontent.com/79613445/210191504-fed0a569-ab80-4196-8afb-b1aba86577d1.webm)


### Jump To Markers

Jump Current Frame to Markers

[JumpToMarker.webm](https://user-images.githubusercontent.com/79613445/210191308-5e955a82-2d18-498f-8817-43891a26a3b2.webm)

# Documentation

[Frame Ranger Documentation](https://frame-ranger.readthedocs.io/en/latest/index.html#)
