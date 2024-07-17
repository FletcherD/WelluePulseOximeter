# WelluePulseOximeter
Simple library to read data from Wellue BLE Pulse Oximeter.

## Usage

Import Wellue.
Call Wellue.connect() with the MAC address of your device.
Pop a reading from Wellue.reading_queue.

There are two types of readings: `fast` and `slow`.

Each reading is a dictionary object containing the following values:

### Fast Reading

`type`: `'fast'`

`counter`: An index which increments for each fast reading and rolls over at 256.

`oximeter`: A pulse oximeter reading, which has already been scaled by the device to be relative to its current operating range. Range: 0-100

`pulse`: A normalized indicator of pulse used to update the bar graph on the device. Range: 0-16

`status`: A bitmask containing some flags about operating state. Meaning currently unknown.

### Slow Reading

`type`: `'slow'`

`counter`: An index which increments for each slow reading and rolls over at 256.

`bpm`: Beats per minute. Range: 0-255

`sp_o2`: SpO2 (blood oxygenation percentage). Range: 0-100

`pi`: Perfusion index. Range: 0-100 (floating point)

## Files

### Wellue.py

The main library.

### PlotData.py

A simple example, just a live plot of the last 500 values for `oximeter` and `pulse`.
