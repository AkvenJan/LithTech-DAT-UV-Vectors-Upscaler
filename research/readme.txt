LithTech DAT UV vectors Upscaler (for 010 Editor)
=================================================
by snobel
=========

Purpose
-------
This script allows to automatically edit DAT files (map files) for LithTech engine games, upscaling UV vectors for textures, so the textures are rendering correctly if you are trying to upscale them.
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

But on practice I only tried them on DAT v66 and DAT v70

Usage
-----
1. You will need 010 Editor (https://www.sweetscape.com/download/010editor/), it has evaluation period of 30 days, so you don't need to buy it for tests

2. Put all the downloaded files into some folder. Preferrably put the DAT files to the same folder. Open UpscaleDAT.1sc file with 010 Editor.
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
Maximum size of the LithTech Engine games I encountered was 512x512 (2048x2048 upon 4x upscaling). Engine supports them just fine. However, dtxutil (convertor from TGA to engine specific DTX format) does not support sizes bigger than 1024 neigher in DEDIT (map editor). So in order to convert them you'll need to find modified DEDIT for your game with support for larger textures (NOLF and AvP2 surely has one). You'll only need this if you are upscaling textures yourself.

This DAT editing is applied only for the levels and level textures.
Character models, weapons, props and some menu elements use different UV mapping and do not need any DAT editing, they always render and scale right no matter what size of the texture you use (At least in NOLF1 game).

Issues
------
1. For few NOLF1 levels I needed to use bspv66_noblock.bt template because of non-standard dat format with commented PBlockTable BlockTable section (this DAT files doesn't had it). In case you encounter non-standard files you'll need to do your own research or ask someone.
2. For textures to render correctly you also need DTX files to retain their meta information (more info here: https://github.com/AkvenJan/DTX-Meta-Transfer). If your are using someone else's upscaled textures and just want to make level compatible with them - you don't have to worry about it.

P.S.
----
I only tried script on DAT v66 and DAT v70 templates. On other versions you may be forced to change the script using the structure from the template files. To see how template is working on your DAT file, open the template (*.bt file) and press F5 in 010 Editor.

Credits
-------
Templates for DAT files were researched here: https://github.com/haekb/godot-dat-reader/tree/master/Research
Script was written by snobel (https://www.ttlg.com/forums/member.php?u=40710)
