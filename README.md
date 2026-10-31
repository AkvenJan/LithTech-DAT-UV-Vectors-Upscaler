# LithTech-DAT-UV-Vectors-Upscaler
A script to upscale UV/OPQ vectors in DAT files to be able to use larger textures without manual rescaling the whole level

Research on DAT files for various versions of LithTech engine for 010 Editor. I took them from here  
https://github.com/haekb/godot-dat-reader/tree/master/Research  
Also added DAT v70 (commented last raw of the DAT v66 format so it apply correctly - and you don't need renderData for upscale script to work)  

# Purpose \ Why this is needed
In LithTech, UV coordinates and effect parameters are stored in the map's DAT file at the original scale. If you simply swap in upscaled textures, they will appear too small (or too large), and the scrolling speed of "Pan" effects will be wrong. These scripts fix both issues.

This scripts allows to automatically edit DAT files (map files), upscaling UV/OPQ vectors for textures, so the textures are rendering correctly if you are trying to use upscaled textures. Script also fix Pan effect (upscaled textures move faster on animated textures).  
On Lithtech Jupiter you will not need this script because Lithtech Jupiter handles UV mapping in a different way, correctly applying textures.

# Usage
## 1. UV scaling
>python fix_uv-dat66.py <scale> <file1.dat> [file2.dat ...] [-o <out_dir>]

## 2. Pan effect fix
>python fix_pan-dat66.py <divisor> <input.dat> <output.dat>

## Example
If you upscaled textures four times - you need to multiply UV vectors by 4 and divide pan effect values by 4  
>python fix_uv-dat66.py 4 M01S03.DAT -o fixed/  
>python fix_pan-dat66.py 4 M01S03.DAT -o M01S03-fixed.DAT

## Old script
Script for UV scaling also available and applyable as original snobel's script for 010 Editor. It's located here, just read readme:  
https://github.com/AkvenJan/LithTech-DAT-UV-Vectors-Upscaler/tree/main/research  
There are two versions of this script:  
* UpscaleDATv56.sc - fo DAT v56  
* UpscaleDAT.1sc - for DAT v66 and DAT v70

Example of usage in mod: https://www.moddb.com/mods/blood-ii-the-chosen-upscale-pack

# Credits
Upscale script for 010 Editor was originally made by by snobel (https://www.ttlg.com/forums/member.php?u=40710)  
A lot of information was given by https://github.com/StenApp. He also fixed some issues for DAT v66

# LithTech versions
    Lithtech 1.0 (DAT v56), uses DTX v1
    	Shogo: Mobile Armor Division
    	Blood II: The Chosen
		Sanity: Aiken's Artifact (had some Lithtech 2.0 enhancements)

	Lithtech 1.0 (DAT v57), uses DTX v1
		TNN Outdoors Pro Hunter 2
    	
    Kiss Psycho Circus (Custom 1.5) (DAT v127), uses DTX v1.5
    	KISS: Psycho Circus: The Nightmare Child 
	
	Lithtech 1.5 (DAT v66), uses DTX v2  
    The engine is 1.5 but textures and levels are packed as LithTech 2x resourсes
    	Might and Magic IX

    Lithtech 2.x (DAT v66), uses DTX v2
    	NOLF1
    	Legends of Might and Magic
    	Die Hard: Nakatomi Plaza

    Lithtech PS2 (LTB v66), uses DTX v2 (mainly 32palletized)
    	NOLF1 (PS2)

    Lithtech Talon (DAT v70), uses DTX v2
    	Aliens versus Predator 2

    Lithtech Jupiter (DAT v85), uses DTX v2
    	No One Lives Forever 2: A Spy In H.A.R.M.'s Way
		Contract J.A.C.K.
    	Tron 2.0

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

* Lithtech (everything lesser than DAT v85) - levels use OPQ Mapping
* Lithtech Jupiter (DAT v85 and higher) - levels use UV Mapping
