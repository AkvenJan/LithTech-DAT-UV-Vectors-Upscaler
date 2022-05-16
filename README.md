# LithTech-DAT-UV-Vectors-Upscaler
A script to upscale UV vectors in DAT files to be able to use larger textures without manual rescaling the whole level

Research on DAT files for various versions of LithTech engine for 010 Editor. I took them from here  
https://github.com/haekb/godot-dat-reader/tree/master/Research  
Also added DAT v70 (commented last raw of the DAT v66 format so it apply correctly - and you don't need renderData for upscale script to work)  
And added second DAT v66 template for those rare files without BlockTable section (or they generate error upon upscaling)

# Purpose
This script allows to automatically edit DAT files (map files), upscaling UV vectors for textures, so the textures are rendering correctly if you are trying to use upscaled textures.  
On Lithtech Jupiter you will not need this script because Lithtech Jupiter handles UV mapping in a different way, correctly applying textures.

# Usage
For now script only available and applyable as original snobel's script for 010 Editor. It's located here, just read readme:  
https://github.com/AkvenJan/LithTech-DAT-UV-Vectors-Upscaler/tree/main/research

# Credits
Upscale script for 010 Editor was originally made by by snobel (https://www.ttlg.com/forums/member.php?u=40710)

# LithTech versions
    Lithtech 1.0 (DAT v56), uses DTX v1
    	Shogo: Mobile Armor Division
    	Blood II: The Chosen
    	
    Lithtech 1.5 (DAT v57), uses DTX v1.5
    	Might and Magic IX
    	
    Kiss Psycho Circus (Custom 1.5) (DAT v127)
    	KISS: Psycho Circus: The Nightmare Child 
	
    Lithtech 2.x (DAT v66), uses DTX v2
    	NOLF1
    	Sanity: Aiken's Artifact 
    	Legends of Might and Magic
    	Die Hard: Nakatomi Plaza

    Lithtech PS2 (LTB v66)
    	NOLF1 (PS2)

    Lithtech Talon (DAT v70)
    	Aliens versus Predator 2
    	Might and Magic IX 

---

    Lithtech Jupiter (DAT v85)
    	No One Lives Forever 2: A Spy In H.A.R.M.'s Way
    	Tron 2.0
    	Medal of Honor: Pacific Assault

But on practice I only tried them on DAT v66 and DAT v70 only
