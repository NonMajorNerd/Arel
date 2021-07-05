           ,ggg,    d8' ,ggggggggggg,                   
          dP""8I   d8' dP"""88""""""Y8,           ,dPYb,
         dP   88  ""   Yb,  88      `8b           IP'`Yb
        dP    88        `"  88      ,8P           I8  8I
       ,8'    88            88aaaad8P"            I8  8'
       d88888888            88""""Yb,     ,ggg,   I8 dP 
 __   ,8"     88            88     "8b   i8" "8i  I8dP  
dP"  ,8P      Y8            88      `8i  I8, ,8I  I8P   
Yb,_,dP       `8b,          88       Yb, `8b*d8' ,d8b,_ 
 "Y8P"         `Y8          88        Y8888P"Y8888P'"Y88
 
 A'Rel Readme
 
 v 0.0.0.1
 Coding by NonMajorNerd and RubberDucky
 Testing and design by NonMajorNerd, RubberDucky, Narmyra, FinitelyCraig, and ProbablyTom
 Art by Quale (https://imgur.com/a/uHx4k), Kenney (https://kenney.nl/assets/bit-pack), and NonMajorNerd
 
 Based on the tcod library
 

 ****************
 * Dependencies *
 ****************
 
 Python v3+  			(https://www.python.org/downloads/)
 Python tcod Library	(https://python-tcod.readthedocs.io/en/latest/installation.html)
 
 **************
 *  Controls  *
 **************
 
    Movement;
	
		Numpad;			Arrow Keys;		(eg R is Right-Arrow, sR is Shift + Right-Arrow)
							
			7  8  9 		sL  U sU         
			 \ | / 			  \ | /              
			4- 5 -6			 L- z -R         
			 / | \  		  / | \               
			1  2  3 		sD  D  sR 
    
	[c] Close
		press [c] and then a directional key as outlined above to close objects.
	
    [i] Inventory
        Press [i] to open your inventory
            press [i] or [esc] to close the inventory
            
			Within the inventory menu you can use the arrow keys to move and [Enter] to select/use/(d)equip an item, or you can use the mouse and left-click to select/use/(d)equip an item.
    
    [k] Kick
        Press [k] and then a directional key as outlined above to kick.
		
	[l] Message Log
		Press [l] to view the verbose message log
        
    [s] Stats
        Press [s] to open your stats menu
        Press [esc] to close the stats menu
		
	[x] Examine/Target
		Press [x] to enter targeting mode, then use the arrow keys to select a cell/target to examine.
		Press [esc] to leave targeting mode.
 
    ****************
    *  To-Do List  *
    ****************
	
		*Add left/right (KP4/KP6) in menus to naviage pages
		*Add communicable conditions
		*Add score to death screen
		*Add score saving, high-score tables
		*Build AI subroutines capable of opening doors (A*  ignore door? check when moving if destination is a door, if so open instead of move)
		*Check carrying cap after dequipping items (currently you can dequip a bag and be carrying more than you should be able to)
		*Build support for two-handed weapons
		*Penis-shaped yogurt-shooting baton
		*Update accessory system
		*Fix fireball scroll displaying true name of unidentified burned items 
		*Add description_list and effects_list
		*Add a check/return so if a list is searched and there is no result, it returns a default .. eg if names list does not have a name for this item, just return the default name.
		*WAP Fatigue
		*Expand scoring system
		*Build a check for 'is there a camera op? if not, spawn one nearby (but outside of player FoV)'
		*Extend ranged weapon systems
			*accuracy??
			*capability to hip-fire at reduced accuaracy/damage?
			*reduced damage if firing at range 1?
		*Certainly a ton of other things	
		
		
    **************
    * Change log *
    **************
	
	4/22/21
		Blocked out core systems and logic for more robust ammo usability
		Added the Quiver item
	
	03/24/21
		Added ranged weaponry, ammo typess
	
	03/15/21
		Small bug fixes and cosmetics in the inventory
		AI and spawning tweaks
		
	03/14/21
		Rebalanced item spawn rates, monster spawn rates, monster stats
		All monster and player stats rebalanced
		Took care of minor bugs related to inventory menu
		Kept basic data sheets for future balancing
		Implemented context menu for examining creatures.
		Nailed it.
		Got rid of inventory pre-identification via effect text

	03/12/21
		Decoupled inventory and equipment lists
		Restructured equipment system
		Implemented basic inventory sorting
	
	03/06/21
		Added basic score system .. points are gained for kills, kills seen by camera operator reward more points
		Added character naming
		Added unique sprites for each origin choice
	
	03/02/21
		Added inventories and equipment to monsters
		Fixed bug related to the "Illiterate" conduct
	
	02/24/21
		Small interface changes (menu locations, item colors, description texts)
	
	02/23/21
		Added intro screen
		Added origins and starting equipment
		Added carrying capacity bonuses to equipment
		Bug fixes related to unidentified items
		Changes to item spawn rates
		
	02/22/21
		Fixed a bug related to the colors_list and names_list after items had been identified.
		
		Updated the engine to catch the input and game state for door closing

		added trackers for players # of scrolls read, # of potions drank
	
	02/19/21
		Added the ability to close doors
			TODO :: factor opening doors into certain AI subsets (etc for the camera op, but not for rats)
			
		Added the 'flammable' property to the item component, and made fireball scroll destroy flammable objects
				
		Fixed the order-of-operations in target seraching when kicking (mainly fixes kicking things through open doorways)
		
		Fixed spawn rates    



*The current TEMPORARY menu_background.png file is the sole property of Wizards of the Coast (© 1993-2021 Wizards of the Coast LLC, a subsidiary of Hasbro, Inc. All Rights Reserved.)*