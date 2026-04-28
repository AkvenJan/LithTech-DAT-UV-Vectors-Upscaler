# LithTech-DAT-UV-Vectors-Upscaler
A script to upscale UV/OPQ vectors in DAT files to be able to use larger textures without manual rescaling the whole level

Research on DAT files for various versions of LithTech engine for 010 Editor. I took them from here  
https://github.com/haekb/godot-dat-reader/tree/master/Research  
Also added DAT v70 (commented last raw of the DAT v66 format so it apply correctly - and you don't need renderData for upscale script to work)  

And added second DAT v66 template for those rare files without BlockTable section (or they generate error upon upscaling). Update: You don't need second template anymore, main template was fixed by https://github.com/StenApp

# Purpose
This script allows to automatically edit DAT files (map files), upscaling UV/OPQ vectors for textures, so the textures are rendering correctly if you are trying to use upscaled textures.  
On Lithtech Jupiter you will not need this script because Lithtech Jupiter handles UV mapping in a different way, correctly applying textures.

# Usage
For now script only available and applyable as original snobel's script for 010 Editor. It's located here, just read readme:  
https://github.com/AkvenJan/LithTech-DAT-UV-Vectors-Upscaler/tree/main/research  
There are two versions of this script:  
* UpscaleDATv56.sc - fo DAT v56  
* UpscaleDAT.1sc - for DAT v66 and DAT v70

Example of usage: https://www.moddb.com/mods/blood-ii-the-chosen-upscale-pack

`dataup.py` is incomplete, don't use it

# Credits
Upscale script for 010 Editor was originally made by by snobel (https://www.ttlg.com/forums/member.php?u=40710)

# LithTech versions
    Lithtech 1.0 (DAT v56), uses DTX v1
    	Shogo: Mobile Armor Division
    	Blood II: The Chosen

    Kiss Psycho Circus (Custom 1.5) (DAT v127), uses DTX v1.5
    	KISS: Psycho Circus: The Nightmare Child 

    Lithtech 1.5 (DAT v66), uses DTX v1.5
	The engine is 1.5 but textures and levels are packed as LithTech 2x resourсes
    	Might and Magic IX

    Lithtech 2.x (DAT v66), uses DTX v2
    	NOLF1
    	Sanity: Aiken's Artifact 
    	Legends of Might and Magic
    	Die Hard: Nakatomi Plaza

    Lithtech PS2 (LTB v66)
    	NOLF1 (PS2)

    Lithtech Talon (DAT v70), uses DTX v2
    	Aliens versus Predator 2

---

    Lithtech Jupiter (DAT v85), uses DTX v2
    	No One Lives Forever 2: A Spy In H.A.R.M.'s Way
    	Tron 2.0
    	Medal of Honor: Pacific Assault

But on practice I only tried them on DAT v56, DAT v66 and DAT v70 only

# UV Vectors vs OPQ Vectors
From https://github.com/StenApp
> UV Mapping
> 
>     Definition: Standard coordinate mapping (U for horizontal, V for vertical).
>     Behavior: The texture is "wrapped" to the specific vertices of the surface.
>     Key Characteristic: If you move or stretch the vertices of the brush, the texture stretches and deforms with them.
>     Usage: Best for specific trim work or when you want a texture to remain locked to a face regardless of its position in world space.
> 
> OPQ Mapping
> 
>     Definition: Planar or "World" mapping (O, P, Q represent the origin and two directional vectors).
>     Behavior: The texture is projected onto the surface based on a fixed plane in 3D space.
>     Key Characteristic: If you move the vertices of the brush, the texture remains stationary in the world—it looks as though the brush is "cutting through" a static wallpaper. The texture does not stretch when the brush shape is modified; it simply reveals more of the pattern.
>     Usage: This is the standard for walls, floors, and ceilings. It allows for perfectly seamless textures across multiple brushes because the alignment is based on world coordinates rather than individual face geometry.
> 
> In short: Use UV if you want the texture to stick and stretch with the shape; use OPQ for architectural surfaces where you want the texture to remain consistent and undistorted across the environment.

* Lithtech (everything lesser than DAT v85) - OPQ Mapping
* Lithtech Jupiter (DAT v85 and higher) - UV Mapping