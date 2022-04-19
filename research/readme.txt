LithTech DAT UV vectors Upscaler
================================
by snobel
=========

Purpose
-------
This script allows to automatically edit DAT files (map files), upscaling UV vectors for textures, so the textures are rendering correctly if you are trying to upscale them.
On Lithtech Jupiter you will not need this script because Lithtech Jupiter handles UV mapping in a different way, correctly applying textures.

Theoretically supports this versions:

    Lithtech 1.0 (DAT v56) - template: bspv56.bt
    	Shogo: Mobile Armor Division
    	Blood II: The Chosen
    	
    Lithtech 1.5 (DAT v57) - template: bspv57.bt
    	Might and Magic IX
    	
    Kiss Psycho Circus (Custom 1.5) (DAT v127) - template: bspv127-psycho.bt
	KISS: Psycho Circus: The Nightmare Child 
	
    Lithtech 2.x (DAT v66) - template: bspv66.bt
    	NOLF1
    	Sanity: Aiken's Artifact 
    	Legends of Might and Magic
    	Die Hard: Nakatomi Plaza
    	
    Lithtech Talon (DAT v70) - template: bspv70.bt
    	Aliens versus Predator 2
    	Might and Magic IX 
    	
    Lithtech PS2 (LTB v66) - template: bspv66_ps2.bt
    	NOLF1 (PS2)

________________________________________________________
    Lithtech Jupiter (DAT v85) - template: bsp85.bt
    	No One Lives Forever 2: A Spy In H.A.R.M.'s Way
    	Tron 2.0
    	Medal of Honor: Pacific Assault

But on practice I only tried them on DAT v66 and DAT v70 only

Usage
-----
1. You will need 010 Editor (https://www.sweetscape.com/download/010editor/), it has evaluation period of 30 days, so you don't need to buy it

2. Put all the downloaded files into some folder. Preferrably put the DAT files to the same folder. Open UpscaleDAT.1sc file with 010 Editor
Edit this line, setting name of the chosen LithTech engine version template. For example:
NOLF1
	const char Template[MaxChar] = "bspv66.bt";
Aliens versus Predator 2
	const char Template[MaxChar] = "bspv70.bt";
	
3. Press F7. Enter the scaling factor (the scale of the upscaled textures you'll use. If they are 4 times bigger than the original - set 4.0)

4. Select the files you want to proceed (you can proceed several files at once) 

5. Select the folder for the result

Notes on scale factor
---------------------
The script edit all the textures of the level, upscaling their UV vectors to the same multiply factor. So you need all the textures to be upscaled by the same factor.
LithTech Engine do not support textures bigger than 1024. Most of the textures are maximum of 256 pixels. But for example NOLF had several textures with the size of 512 pixels (and you'll need to downsize them to 2x if you are using 4x upscale factor so they'll be supported by the engine). And since the script treats all the textures the same way - this textures will render wrong ingame. So you'll need to use only 2x factor for DAT files and for textures
This is applied only for the levels and level textures.

Character models, weapons, props and some menu elements use different uv mapping and do not need any DAT editing, they always render and scale right no matter what size of the texture you use (At least in NOLF1 game).

Issues
------
1. In NOLF1 game some sporadic textures ignore scale factor and always render incorrectly. This textures persist throught the levels, so I just revert them back to their original size
2. (not related to script) For some unknown reason in NOLF1 game detail textures and environmental textures do not apply after using any upscaled textures. Maybe somehow related to DTX or TGA formats. I suggest it has something to do with solid white/solid black alpha layers on textures being the flag for this effects rendering, but no matter how I recombine this layers and what program I use - I can't make it work. If anyone knows anything about this - please tell me

P.S.
----
I only tried script on DAT v66 and DAT v70 templates. On other versions you may be forced to change the script using the structure from the template files. To see how template is working on your DAT file, open the template (*.bt file) and press F5 in 010 Editor.

Credits
-------
Templates for DAT files were researched here https://github.com/haekb/godot-dat-reader/tree/master/Research
Script was written by snobel (https://www.ttlg.com/forums/member.php?u=40710)