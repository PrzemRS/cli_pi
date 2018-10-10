#!/bin/bash

LED0=1
OLD_LED0=1
LED1=1
OLD_LED1=1
LED2=1
OLD_LED2=1
LED3=1
OLD_LED3=1

until [ $LED0 -eq 0 ] && [ $LED1 -eq 0 ] && [ $LED2 -eq 0 ] && [ $LED3 -eq 0 ]; do
    echo "vector(+, gen_tp1) := [ 1 1 0 $LED3 $LED2 $LED1 $LED0 ];"
    OLD_LED0=$LED0
    OLD_LED1=$LED1
    OLD_LED2=$LED2
    OLD_LED3=$LED3
    
    let LED0=LED0-1
    if [ $LED0 -eq -1 ]; then
        let LED0=1
    fi

    if [ $OLD_LED0 -eq 0 ] && [ $LED0 -eq 1 ]; then
        let LED1=LED1-1
        if [ $LED1 -eq -1 ]; then
            let LED1=1
        fi
    fi

    if [ $OLD_LED1 -eq 0 ] && [ $LED1 -eq 1 ]; then
        let LED2=LED2-1
        if [ $LED2 -eq -1 ]; then
            let LED2=1
        fi
    fi

    if [ $OLD_LED2 -eq 0 ] && [ $LED2 -eq 1 ]; then
        let LED3=LED3-1
        if [ $LED3 -eq -1 ]; then
            let LED3=1
        fi
    fi
done

echo "vector(+, gen_tp1) := [ 1 1 0 $LED3 $LED2 $LED1 $LED0 ];"