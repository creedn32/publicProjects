;Key
;#   Win (Windows logo key)
;!   Alt
;^   Control
;+   Shift
;&   An ampersand may be used between any two keys or mouse buttons to combine them into a custom hotkey.
;http://ahkscript.org/docs/Tutorial.htm#s21

; ------------------------------------
; VIM Like Shortcuts for All Programs
; ------------------------------------
; These assume you have remapped Left-Windows to F13 using sharpkeys2
; I also typically remap Caps Lock to Left-Windows as well.
; Have VIM like movement in various applications is extremely ;useful!


;#a::
;    Run "C:\Program Files\Everything\Everything.exe"



F13 & m::
    SendInput {Blind}{Down}
return

F13 & u::
    SendInput {Blind}{Up}
return

F13 & j::
    SendInput {Blind}{Left}
return

F13 & k::
    SendInput {Blind}{Right}
return



;Sc029 & m::
;    SendInput {Blind}{Down}
;return

;Sc029 & u::
;    SendInput {Blind}{Up}
;return

;Sc029 & j::
;    SendInput {Blind}{Left}
;return

;Sc029 & k::
;    SendInput {Blind}{Right}
;return



;LCtrl & m::
;    SendInput {Down}
;return

;LCtrl & u::
;    SendInput {Up}
;return

;LCtrl & j::
;    SendInput {Left}
;return

;LCtrl & k::
;    SendInput {Right}
;return




;#IfWinActive Executor
;    Tab::
;        SendInput {Blind}{Right}{End}
;    return



;    LCtrl & m::
;        SendInput {Down}
;    return

;    LCtrl & u::
;        SendInput {Up}
;    return

;    LCtrl & j::
;        SendInput {Left}
;    return

;    LCtrl & k::
;        SendInput {Right}
;    return