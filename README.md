## Converting DW8 files into SYX format

This is a puny Python script that I used to convert a bunch of DW8 files into SYX format.

Häh?

Ok, some friendly fellow on the Facebook Group Korg DW-8000 / EX-8000 found a bunch of files in the Internet that looked 
like they could contain "patches" for the Korg DW-8000 (and EX-8000) synthesizers. Patches are just data sets stored
on some medium that allow the synthesizer to recall a specific sound that was dialed in via its controls. The Korg
needs 51 bytes per patch.

Those files can be found in some old CD-ROM archive over at [CD.TEXTFILES.COM](http://cd.textfiles.com/10000soundssongs/SYNTHDAT/KORG/DW8000/).

Now, we did not find out what program created those DW8 files, most probably a stone-age librarian, maybe even some software for an Atari ST.
But looking into those files with a hex editor quickly shows that essentially, I could figure out that
* The first data clearly is a String with the patch name (the Korg doesn't store patch names, so this was a computer-based name only)
* As the first byte is obviously the count of characters in the following text, and there are always 16 bytes reserved, my assumption was that it is a short string in Pascal
* After that, we have 53 bytes - I needed only 51 bytes, so it is unclear what the two additional bytes did
* Finding one file called FCTSIDEA.DW8, which sounds like it was the side A of the factory cassette (the Korg stored its patches on audio cassettes)
* Inside this file I found one patch called CX-3, which I had found also as a separate Korg sysex file elsewhere on the net
* With this, I had my [Rosetta Stone](https://en.wikipedia.org/wiki/Rosetta_Stone) to confirm my interpretation. 
 
So the DW8 format is:
* Two magic bytes at the start (0x00 0x40)
* And then a repeating section of 70 bytes each:
    * One byte for the number of characters used in the next section
    * 16 bytes reserved for the patch name (which is not transferred into the synthesizer)
    * one 0 byte without purpose I could figure out
    * 51 bytes of pure sysex data of the patch
    * another unknown 0 byte

In this repo you find the script that I wrote to run the conversion of a bunch of DW8 files, and create edit buffer dumps that can be sent to the synthesizer.

The result of this conversion were 850 new old patches for the synthesizer saved from oblivion!

## Contributing

All pull requests and issues welcome, I will try to get back to you as soon as I can.  

## About the author

Christof is a lifelong software developer having worked in various industries, and can't stop his programming hobby anyway.     
   