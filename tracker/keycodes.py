''' ASCII Key Codes '''

KEY_ESC = 27
KEY_BKSP = 8
KEY_ENTR = 13
KEY_TAB = 9
KEY_SPC = 32
KEY_UP = 38
KEY_DOWN = 40
KEY_LEFT = 37
KEY_RIGHT = 39

def KEY_ALPHA(ch):
  return ord(ch)

def KEY_NUM(x):
  return 96 + x

def KEY_FUNC(x):
  return 112 + x