#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

"""
Converts 2A03-register writes (csv) into bytebeat-code.
Correctly formatted csv-output file from lua-script needed.

== SETUP ==
Get an emulator which supports nsf-playback. It was tested with fceux 2.2.3 on Windows.
Put the .lua file into the lua-scripts folder and load it inside the emulator.
Make sure it is set to Recording-mode and play back your .nsf
A file "logAPU.csv" is created. Move that one into your Python-Project folder and run this script.
A file "output.txt" is created, this is your tune.

== LIMITATIONS ==
- no F-1 note (miau and me don't know why, but the lua script isn't properly recording those lol)
- no Hardware Sweep
- no DPCM
- only supports 0cc-FT exports, no vanilla or Deflemask

Author: @kleeder
Created: 2022-07-25 to 2023-04-10
"""

import csv
with open('logAPU.csv', newline='\n') as csvfile:
    apu_log = csv.reader(csvfile, delimiter=',', quotechar='|')
    new_text = """SAMP_RATE = 44100,
CLOCK = 1789773,

convert_duty=function(value){
    if(value == '3'){
        return 12.5;
    }
    else if(value == '7'){
        return 25;
    }
    else if(value == 'B'){
        return 50;
    }
    else if(value == 'F'){
        return 75;
    }
},

convert_freq_1=function(value){
    freq_byte=value.substr(0,2);
    high_byte=value.substr(2,2);
    if(high_byte === '08'){HIGH_BYTE_1 = 8}
    if(high_byte === '09'){HIGH_BYTE_1 = 9}
    if(high_byte === '0A'){HIGH_BYTE_1 = 10}
    if(high_byte === '0B'){HIGH_BYTE_1 = 11}
    if(high_byte === '0C'){HIGH_BYTE_1 = 12}
    if(high_byte === '0D'){HIGH_BYTE_1 = 13}
    if(high_byte === '0E'){HIGH_BYTE_1 = 14}
    if(high_byte === '0F'){HIGH_BYTE_1 = 15}
    if(freq_byte === '00'){return 0}
    if(HIGH_BYTE_1 === 9){freq_byte='1'+freq_byte}
    if(HIGH_BYTE_1 === 10){freq_byte='2'+freq_byte}
    if(HIGH_BYTE_1 === 11){freq_byte='3'+freq_byte}
    if(HIGH_BYTE_1 === 12){freq_byte='4'+freq_byte}
    if(HIGH_BYTE_1 === 13){freq_byte='5'+freq_byte}
    if(HIGH_BYTE_1 === 14){freq_byte='6'+freq_byte}
    if(HIGH_BYTE_1 === 15){freq_byte='7'+freq_byte}

    return (CLOCK / (16 * parseInt(freq_byte, 16) + 1));
},

convert_freq_2=function(value){
    freq_byte=value.substr(0,2);
    high_byte=value.substr(2,2);
    if(high_byte === '08'){HIGH_BYTE_2 = 8}
    if(high_byte === '09'){HIGH_BYTE_2 = 9}
    if(high_byte === '0A'){HIGH_BYTE_2 = 10}
    if(high_byte === '0B'){HIGH_BYTE_2 = 11}
    if(high_byte === '0C'){HIGH_BYTE_2 = 12}
    if(high_byte === '0D'){HIGH_BYTE_2 = 13}
    if(high_byte === '0E'){HIGH_BYTE_2 = 14}
    if(high_byte === '0F'){HIGH_BYTE_2 = 15}
    if(freq_byte === '00'){return 0}
    if(HIGH_BYTE_2 === 9){freq_byte='1'+freq_byte}
    if(HIGH_BYTE_2 === 10){freq_byte='2'+freq_byte}
    if(HIGH_BYTE_2 === 11){freq_byte='3'+freq_byte}
    if(HIGH_BYTE_2 === 12){freq_byte='4'+freq_byte}
    if(HIGH_BYTE_2 === 13){freq_byte='5'+freq_byte}
    if(HIGH_BYTE_2 === 14){freq_byte='6'+freq_byte}
    if(HIGH_BYTE_2 === 15){freq_byte='7'+freq_byte}

    return (CLOCK / (16 * parseInt(freq_byte, 16) + 1));
},

convert_freq_3=function(value){
    freq_byte=value.substr(0,2);
    high_byte=value.substr(2,2);
    if(high_byte === '08'){HIGH_BYTE_3 = 8}
    if(high_byte === '09'){HIGH_BYTE_3 = 9}
    if(high_byte === '0A'){HIGH_BYTE_3 = 10}
    if(high_byte === '0B'){HIGH_BYTE_3 = 11}
    if(high_byte === '0C'){HIGH_BYTE_3 = 12}
    if(high_byte === '0D'){HIGH_BYTE_3 = 13}
    if(high_byte === '0E'){HIGH_BYTE_3 = 14}
    if(high_byte === '0F'){HIGH_BYTE_3 = 15}
    if(freq_byte === '00'){return 0}
    if(HIGH_BYTE_3 === 9){freq_byte='1'+freq_byte}
    if(HIGH_BYTE_3 === 10){freq_byte='2'+freq_byte}
    if(HIGH_BYTE_3 === 11){freq_byte='3'+freq_byte}
    if(HIGH_BYTE_3 === 12){freq_byte='4'+freq_byte}
    if(HIGH_BYTE_3 === 13){freq_byte='5'+freq_byte}
    if(HIGH_BYTE_3 === 14){freq_byte='6'+freq_byte}
    if(HIGH_BYTE_3 === 15){freq_byte='7'+freq_byte}

    return ((CLOCK / (16 * parseInt(freq_byte, 16) + 1))/2);
},

noise_frequencies = [
        440.0,
        879.9,
        1761.6,
        2348.8,
        3523.2,
        4709.9,
        7046.4,
        8860.3,
        11186.1,
        13982.6,
        18643.5,
        27965.2,
        55930.4,
        111860.8,
        223721.6,
        447443.3,
    ],

convert_freq_4=function(mode, value, active){
    if (active !== '8'){return 0}
    if(value === 'F'){return noise_frequencies[0]}
    if(value === 'E'){return noise_frequencies[1]}
    if(value === 'D'){return noise_frequencies[2]}
    if(value === 'C'){return noise_frequencies[3]}
    if(value === 'B'){return noise_frequencies[4]}
    if(value === 'A'){return noise_frequencies[5]}
    if(value === '9'){return noise_frequencies[6]}
    if(value === '8'){return noise_frequencies[7]}
    if(value === '7'){return noise_frequencies[8]}
    if(value === '6'){return noise_frequencies[9]}
    if(value === '5'){return noise_frequencies[10]}
    if(value === '4'){return noise_frequencies[11]}
    if(value === '3'){return noise_frequencies[12]}
    if(value === '2'){return noise_frequencies[13]}
    if(value === '1'){return noise_frequencies[14]}
    if(value === '0'){return noise_frequencies[15]}
   return 0;
},

convert_chan4_wave=function(mode, freq){
   if (mode === '0'){return floor(t * (chan4_freq * 440 / SAMP_RATE) / 440)}
   else if (mode === '8'){return (floor(t * (chan4_freq * 440 / SAMP_RATE) / 440))%93}
   return 0;
},

read_data=(data, t)=>(
    current_order=data[int(t/724) % data.length],

    chan1_amp=(parseInt(current_order.charAt(1), 16) * (-2))+256,
    chan1_freq=convert_freq_1(current_order.substr(4, 4)),
    chan1_pulse = convert_duty(current_order.charAt(0)),

    chan2_amp=(parseInt(current_order.charAt(9), 16) * (-2))+256,
    chan2_freq=convert_freq_2(current_order.substr(12, 4)),
    chan2_pulse = convert_duty(current_order.charAt(8)),

    chan3_freq=convert_freq_3(current_order.substr(20, 4)),

    chan4_amp=(parseInt(current_order.charAt(25), 16)),
    chan4_mode = current_order.substr(28, 1),
    chan4_freq=convert_freq_4(chan4_mode, current_order.substr(29, 1), current_order.substr(31, 1)),
    chan4_pulse = convert_chan4_wave(chan4_mode, chan4_freq),

    chan1_phase += chan1_freq*256,
    chan2_phase += chan2_freq*256,
    chan3_phase += chan3_freq*32,
    
    (((chan1_phase / SAMP_RATE) % 256 < 256 * chan1_pulse / 100) * chan1_amp - chan1_amp / 2) +
    (((chan2_phase / SAMP_RATE) % 256 < 256 * chan2_pulse / 100) * chan2_amp - chan2_amp / 2) +

    ((17*abs(min(16-chan3_phase/SAMP_RATE%32|0,15)) / 2 + 204)/4) +
    (((((floor(65536 * sin(chan4_pulse*chan4_pulse)) & 255)) * chan4_amp / 128) * 800 / 128)/4 + 64)
),

t?0:(chan1_phase=0,chan2_phase=0,chan3_phase=0),

t?0:DATA = [
"""
    for row in apu_log:
        if row[0].startswith('==='):
            continue
        new_text += f"'{''.join([x.zfill(2) for x in row])}',\n"

new_text += """
],

read_data(DATA, t)
"""

with open("output.txt", "w") as f:
    f.write(new_text)
    f.close()
