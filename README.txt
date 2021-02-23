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
 NonMajorNerd (ObservantDoggo)
 
 Based on libtcod
 
 
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
    * Known Issues *
    ****************
    
    **************
    * Change log *
    **************
	
	02/22/21
		Fixed a bug related to the colors_list and names_list after items had been identified.
		
		Updated the engine to catch the input and game state for door closing

		added trackers for players # of scrolls read, # of potions drank
	
	02/19/21
		Added the ability to close doors
			TODO :: factor opening doors into certain AI subsets (etc for the camera op, but not for rats)
			
		Added the 'flamable' property to the item component, and made fireball scroll destroy flamable objects
			TODO :: Fix unidentified items displaying identified name when burned this way
				
		Fixed the order-of-operations in target seraching when kicking (mainly fixes kicking things through open doorways)
		
		Fixed spawn rates    