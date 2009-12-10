Name: audioAmplitudeExtractor
Author: Dominic Drane
Website: www.reality-debug.co.uk
E-mail: dom@reality-debug.co.uk
Version: .9

Description:

This node will allows you to extract the volume (or amplitude) data from an uncompressed wave file and use it to power a Maya attribute or bake the data to a key.
	
Future versions will support frequency analysis so low, medium and high frequencies can power attributes individually.
	
For an installation and usage instruction video please go to: 
www.reality-debug.co.uk/files   

Usage:

Install files located within the scripts folder to your Maya scripts directory and files located within the plug-ins folder to your Maya plug-in directory.

Once Maya is loaded you should active the audioAmplitudeExtractor.py file from your Settings/Preferences > Plug-in manager menu.
The node can then be added by typing the following into your script editor:
		
	createNode audioAmpNode;

If successful you should now have the node controls within your attribute editor.
	
For a more detailed version of installation instructions & usage instructions please see a video tutorial located at: www.reality-debug.co.uk/files
    
If you find any problems that are not listed above me contact me and I'll attempt to fix them as soon as possible.
    

Changelog:

20/07/09 - initial release
18/10/09 - Fixed a couple of bugs/spelling errors and added online help buttons



---
The MIT License

Copyright (c) 2009 Dominic Drane

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.