import libtcodpy as libtcod

import textwrap
from random_utils import left, mid, right

class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color
        


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height
        self.history = []
        
    def add_message(self, message):
    
        currentmessage = message.text #current message being added
    
        if len(self.history) > 0:
            lastmessage = self.history[len(self.history)-1].text #most recent message in the history log
            
            if lastmessage == currentmessage:
                lastlogmessage = self.messages[len(self.messages)-1].text #most recent message in the on-screen log

                check = right(lastlogmessage, 5)

                if left(check, 2) == "(x":
                    strcount = str(int(mid(check, 3, 2)) + 1)
                else:
                    strcount = "02"
                
                if len(strcount) == 1: strcount = "0" + strcount
                
                currentmessage = currentmessage + " (x" + strcount + ")"
                    
                #delete last message in the on-screen log
                if len(self.messages)>0: del self.messages[len(self.messages)-1]
    
        # Split the message if necessary, among multiple lines using the newly altered 'currentmessage' text
        new_msg_lines = textwrap.wrap(currentmessage, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))
        
        #append the original, unaltered message to the history log
        self.history.append(Message(message.text, message.color))
        
def message_log_history(message_log):
    
    screen_yellow = libtcod.Color(249,220,92)
    screen_blue = libtcod.light_azure
    screen_red = libtcod.Color(254,95,85)
    screen_purple = libtcod.Color(102,46,155)
    
    SCREEN_WIDTH = 60
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    messages_per_page = 33
    
    entries = 0
    for m in message_log.history:
        entries +=1
    
    if entries <= messages_per_page:
        numpages = 1
    else:
        numpages = int(entries / messages_per_page)+1

    currentpage = 1
        
    while True:
        libtcod.console_clear(0)
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        libtcod.console_set_default_background(0, libtcod.light_yellow)
        libtcod.console_set_default_foreground(0, libtcod.black)
 
        libtcod.console_print_ex(0, 30, 1, libtcod.BKGND_SET, libtcod.CENTER, "Message Hisory")
        
        libtcod.console_set_default_foreground(0, libtcod.lighter_gray)
        libtcod.console_print_ex(0, 30, 2, libtcod.BKGND_NONE, libtcod.CENTER, "[ESC] to Close.")
        libtcod.console_print_ex(0, 30, 3, libtcod.BKGND_NONE, libtcod.CENTER, "Down/Up arrow keys for Next/Pervious page")

        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_set_default_foreground(0, screen_blue)
        
        if numpages > 1 :
            libtcod.console_print_ex(0, 1, 38, libtcod.BKGND_NONE, libtcod.LEFT, "pg. " + str(currentpage) + ' of ' + str(numpages))
        
        if entries > 0:
            row = 5
            start = 0 + (messages_per_page * (currentpage-1))
            for m in range(start, start + messages_per_page -1):
                if m <= entries - 1:
                    libtcod.console_set_default_foreground(0, message_log.history[m].color)
                    libtcod.console_print_ex(0, 1, row, libtcod.BKGND_NONE, libtcod.LEFT, message_log.history[m].text)
                    row += 1
                    
        libtcod.console_flush()
        
        choice = key
        if choice.vk == libtcod.KEY_ESCAPE:
            break
            
        if key.vk == libtcod.KEY_DOWN:
            if numpages>= currentpage + 1:
                currentpage += 1
                
        elif key.vk == libtcod.KEY_UP:
            if currentpage - 1 > 0:
                currentpage -= 1
        