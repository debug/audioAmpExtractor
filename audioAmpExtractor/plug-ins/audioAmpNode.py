'''
#	The MIT License
#
#	Copyright (c) 2009 Dominic Drane
#
#	Permission is hereby granted, free of charge, to any person obtaining a copy
#	of this software and associated documentation files (the "Software"), to deal
#	in the Software without restriction, including without limitation the rights
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is
#	furnished to do so, subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be included in
#	all copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#	THE SOFTWARE.
#
#	audioAmplitudeExtrator Maya Python plug-in
#
#	Author: Dominic Drane
#		www.reality-debug.co.uk
#		dom@reality-debug.co.uk
#
#	Version .9
#	Release date: 18/10/09
#
#	Usage: See readme.txt for details/limitations.
#	Video tutorial available online at www.reality-debug.co.uk/files
#
'''

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import wave
import audioop
import struct

kPluginNodeName = "audioAmpNode"
kPluginNodeId = OpenMaya.MTypeId(0x5ffff)
nodeCreator = "_reality debug();"

class audioAmp(OpenMayaMPx.MPxNode):
	filePathIn = OpenMaya.MObject()
	timeIn = OpenMaya.MObject()
	exponentIn = OpenMaya.MObject()
	outputAmp = OpenMaya.MObject()
	soundSizeOut = OpenMaya.MObject()
	offsetIn = OpenMaya.MObject()

	
	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, data):
		frameRate = OpenMaya.MTime.uiUnit()
		if plug == audioAmp.outputAmp:
			

			
			#read the inputs
		
			filePathIn  = data.inputValue(audioAmp.filePathIn)
			timeData = data.inputValue(audioAmp.timeIn)
			exponentInVar = data.inputValue(audioAmp.exponentIn)
			exponentFloat = exponentInVar.asFloat()
			offsetData = data.inputValue(audioAmp.offsetIn)
			
			
			#convert the timein to something a bit more human
			inValue = timeData.asFloat()
			inValueAsInt = int(inValue)
			
			offsetValue = offsetData.asFloat()
			offsetValueAsInt = int(offsetValue)
			
			#sort out the string stuff
			fnString = OpenMaya.MFnStringData( filePathIn.data() )
			fileNamePathFinal = ""
			fileNamePathFinal = fnString.string()
			
			#set up processing object
			waveFile = audioProcessor(frameRate)
			waveFile.processAudio(fileNamePathFinal, offsetValueAsInt)
			
			
			returnedValue = waveFile.processAudio(fileNamePathFinal, offsetValueAsInt)
			if inValueAsInt > waveFile.audioTrackSize():
				result = 0
			else:
				if returnedValue == 0:
					result = 0
				else:
					result = returnedValue[inValueAsInt]
			
			#multiply by expodent
			finalOut = result + (result * exponentFloat)
			
			#print (waveFile.mult(returnedValue[], returnedValue[]))
			
			#output data
			outputSoundSize = data.outputValue(audioAmp.soundSizeOut)
			outputSoundSize.setInt(waveFile.audioTrackSize())
			
			outputAmp = data.outputValue(audioAmp.outputAmp)
			outputAmp.setFloat(finalOut)
			
			#clean up duh
			data.setClean(plug)

		else:
			return OpenMaya.kUnknownParameter
			
class audioProcessor():
	
	def __init__(self, frameRate):
		
		if(frameRate == 0):
			self.sceneFrameRate = "xx"
			print "ERROR: THIS FRAMERATE IS NOT SUPPORTED"
		elif(frameRate == 1):
			self.sceneFrameRate = 3600
		elif(frameRate == 2):
			self.sceneFrameRate = "xx"
		elif(frameRate == 3):
			self.sceneFrameRate = "xx"
		elif(frameRate == 4):
			self.sceneFrameRate = "xx"
		elif(frameRate == 5):
			self.sceneFrameRate = "xx"
		elif(frameRate == 6):
			self.sceneFrameRate = 24
		elif(frameRate == 7):
			self.sceneFrameRate = 25
		elif(frameRate == 8):
			self.sceneFrameRate = 30
		else:
			print "ERROR: THIS FRAMERATE IS NOT SUPPORTED"
	
	def processAudio(self, fileIn, offset):
		
		self.audioFileValues = []
		for i in range(1, offset):
			self.audioFileValues.append(0)
			
		sceneFrameRate = "" 

		if fileIn == "blank":

			return 0

		else:
			waveFile = wave.open(fileIn, 'rb')
			if waveFile.getcomptype() == "NONE":
				sceneFPS = self.sceneFrameRate
				waveFrameRate = waveFile.getframerate()
				waveLength = waveFile.getnframes()
				numChannels = waveFile.getnchannels()
				spf = waveFrameRate / sceneFPS

				width = waveFile.getsampwidth()
	
				for i in range(1,waveLength/spf):
					rawdata = waveFile.readframes(spf)
					current_avg = audioop.rms(rawdata, width)
					self.audioFileValues.append(int(current_avg/100))
			
			else:
				print "ERROR: UNSUPPORTED COMPRESSION TYPE"
			
			return self.audioFileValues	
	
	def audioTrackSize(self):
		return len(self.audioFileValues)
		

	def fft(self, a,w):
		i = complex(0,1)
		ni = complex(0,-1)
		
		if (w==1):
			return a
		s =  self.fft([a[z] for z in range(0,len(a),2)], w**2)
		sp = self.fft([a[z] for z in range(1,len(a),2)], w**2)
		n = len(a)
		r=[]
		for j in range(0,(n/2)):
			r.insert(j, (s[j] + (w**j * sp[j])))
			r.insert(j+(n/2), s[j] - (w**j * sp[j]))
		return r
	
	def mult(self, poly1, poly2):
		
		i = complex(0,1)
		ni = complex(0,-1)
		
		a= len(poly1)
		b= len(poly2)
		
		if a > b:
			for x in range(0, a-b):
				poly2.append(0)
		if b > a:
			for x in range(0, b-a):
				poly1.append(0)
		fftval1 = self.fft(poly1,i)
		fftval2 = self.fft(poly2,i)
		multip = [fftval1[x]*fftval2[x] for x in range(0,len(fftval1))]
		inverse = [ (1.0/(len(multip))*x).real for x in self.fft(multip,ni)]
		return inverse
		
		
	def crunchFreqs(self):
		pass
		

def nodeCreator():
	return OpenMayaMPx.asMPxPtr( audioAmp() )

def nodeInitializer():
	nAttr = OpenMaya.MFnNumericAttribute()
	tAttr = OpenMaya.MFnTypedAttribute()
	
	stringSave = OpenMaya.MFnStringData()
	stringSaveCreator = stringSave.create("blank")
	
	
	audioAmp.filePathIn = tAttr.create("file", "fi", OpenMaya.MFnStringData.kString, stringSaveCreator)
	
	tAttr.setStorable(True)
	tAttr.setKeyable(True)
	
	audioAmp.timeIn = nAttr.create("time", "tm", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setStorable(True)
	
	audioAmp.exponentIn = nAttr.create("exponent","in", OpenMaya.MFnNumericData.kFloat,0.0)
	nAttr.setStorable(True)
	
	audioAmp.outputAmp = nAttr.create("amplitude","out", OpenMaya.MFnNumericData.kFloat,0.0)
	nAttr.setStorable(True)
	
	audioAmp.soundSizeOut = nAttr.create("soundSize", "ss", OpenMaya.MFnNumericData.kInt, 0)
	nAttr.setStorable(True)
	
	audioAmp.offsetIn = nAttr.create("offset", "os", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setStorable(True)
	
	
	audioAmp.addAttribute(audioAmp.filePathIn)
	audioAmp.addAttribute(audioAmp.timeIn)
	audioAmp.addAttribute(audioAmp.exponentIn)
	audioAmp.addAttribute(audioAmp.outputAmp)
	audioAmp.addAttribute(audioAmp.soundSizeOut)
	audioAmp.addAttribute(audioAmp.offsetIn)

	audioAmp.attributeAffects(audioAmp.timeIn, audioAmp.outputAmp)
	audioAmp.attributeAffects(audioAmp.filePathIn, audioAmp.outputAmp)
	audioAmp.attributeAffects(audioAmp.offsetIn, audioAmp.outputAmp)


# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer)
	except:
		sys.stderr.write( "Failed to register node: %s" % kPluginNodeName )
		raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( kPluginNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeName )
		raise
	
