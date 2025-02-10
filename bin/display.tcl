#!/usr/bin/tclsh
package require Tk

proc every {ms body} {eval $body; after $ms [info level 0]}

proc main {} {
    global argc argv
    if {$argc != 0} {
        puts stderr "Usage: display.tcl"
        puts stderr "   Will read on stdin untio EOF"
        exit 1
    }
    label .time -textvar ::time -font {Monospace 20}
    
    every 1000 {
        set value [gets stdin]
        if {[string length $value] > 0} {
            set ::time $value
        }
    }

    pack .time
}

main
