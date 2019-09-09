#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
SLiCk : the Slick Layer Combinator
-------------------------------------------------------------------------------

Auto-sets layer visibility (by naming convention) on a copy of the drawing
and exports an Inkscape SVG for each option layer processed.

Copyright (c) 2019 Matt Jernigan

-------------------------------------------------------------------------------
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
-------------------------------------------------------------------------------
"""

import inkex       # Required
import simplestyle # will be needed here for styles support
from copy import deepcopy
import os

__version__ = '0.1'

inkex.localize()

### Helper functions ###

def getLayers (element):
	layers = element.xpath(".//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS)
	return layers

def displayLayer(layer, display):
	if "style" in layer.attrib:
		style = simplestyle.parseStyle(layer.attrib["style"])
	else:
		style = {}

	if display:
		style["display"] = "inline"
	else:
		style["display"] = "none"

	layer.attrib["style"] = simplestyle.formatStyle(style)


### Main function ###

class Combinator (inkex.Effect):
	
	def __init__(self):
		""" define how the options are mapped from the inx file """
		inkex.Effect.__init__(self) # initialize the super class
		
		# Two ways to get debug info:
		# OR just use inkex.debug(string) instead...
			
		# Define your list of parameters defined in the .inx file
		self.OptionParser.add_option("-a", "--all"
			,	action	= "store"
			,	type	= "inkbool"
			,	dest	= "all"
			,	default	= False
			,	help	= "Find and export all option layers"
		)
		self.OptionParser.add_option("-l", "--layers"
			,	action	= "store"
			,	type	= "string"
			,	dest	= "layers"
			,	default	= ""
			,	help	= "Comma-separated list of option layers to export"
		)
		self.OptionParser.add_option("-d", "--directory"
			,	action	= "store"
			,	type	= "string"
			,	dest	= "directory"
			,	default	= None
			,	help	= "Path to save files to (supports ~ on Windows too)"
		)
		

	### -------------------------------------------------------------------
	### This is your main function and is called when the extension is run.
	def effect(self):
		"""
		Turn layer visibility on/off according to naming conventions
		and export a new drawing for each option layer sent or found.
		"""
		
		# Make a copy of the doc to operate on, to leave original undisturbed.
		tempdoc = deepcopy(self.document)
		svg = tempdoc.getroot()

		# Determine the base filename.
		docname = svg.xpath("@sodipodi:docname", namespaces=inkex.NSS)[0]
		filename = docname.rsplit(".", 1)[0]
		if filename.upper().endswith("__MASTER__"):
			filename = filename[:-10]
		if filename == "":
			filename = "slick" # just overly cautious; "default" is the name until save
			inkex.errormsg(_("Warning: no filename found, saving as \"{}_*.svg\".".format(filename)))

		# Cleanup path string.
		#inkex.debug(os.getcwd())
		dirname = self.options.directory
		if dirname == '' or dirname == None:
			dirname = './'
		dirname = os.path.expanduser(dirname)
		dirname = os.path.expandvars(dirname)
		dirname = os.path.abspath(dirname)
		if dirname[-1] != os.path.sep:
			dirname += os.path.sep
		if not os.path.isdir(dirname):
			os.makedirs(dirname)

		# Begin layer work.
		allLayers = getLayers(svg)
		optionLayers = []

		# Get the names of the option layers to cycle through.
		if self.options.all:
			# Search the whole tree for unique layer names in option layers.
			for l in allLayers:
				label = l.xpath("@inkscape:label", namespaces=inkex.NSS)[0]
				#inkex.debug(label)
				# Is this a parent layer of option layers?  eg: --my options parent--
				if label.startswith("--") and label.endswith("--"):
					childLayers = getLayers(l)
					for cl in childLayers:
						# Layer names can have comma-delimited option names; parse them.
						names = cl.xpath("@inkscape:label", namespaces=inkex.NSS)[0].split(",")
						for n in names:
							n = n.strip()
							if n not in optionLayers:
								optionLayers.append(n)
		elif len(self.options.layers.strip()) > 0:
			optionLayers = self.options.layers.split(",")
			#map(str.strip, optionLayers)
			optionLayers = [i.strip() for i in optionLayers]
			#TODO handle empty strings between commas
		optionLayers.sort()

		# Make sure we have work to do.
		#if len(optionLayers) == 0:
		#	inkex.errormsg(_("No option layers found to create exports with."))
		#	exit()
		#
		# Nevermind, we can always process the other layer types (not sure the use case).
		if len(optionLayers) == 0:
			optionLayers = ["none"]

		# Do it.
		# First, manipulate the non-option layers.
		optionParents = []
		for l in allLayers:
			label = l.xpath("@inkscape:label", namespaces=inkex.NSS)[0]

			# Is this an always-hidden layer?  eg: (hide me)
			if label.startswith("(") and label.endswith(")"):
				displayLayer(l, False)

			# Is this an always-shown layer?  eg: Show Me!
			elif label.find("!") >= 0:
				displayLayer(l, True)

			# Is this a parent layer of option layers?  eg: --my options parent--
			if label.startswith("--") and label.endswith("--"):
				optionParents.append(l)

		# Second, cycle through the option layers and save each result.
		for option in optionLayers:
			for p in optionParents:
				childLayers = getLayers(p)
				for cl in childLayers:
					# Layer names can have comma-delimited option names; parse them.
					names = cl.xpath("@inkscape:label", namespaces=inkex.NSS)[0].split(",")
					names = [n.strip() for n in names] # strip any spaces before search
					displayLayer(cl, option in names)

			totalname = filename + "_" + option + ".svg"
			tempdoc.write(dirname + totalname
				,	xml_declaration=True
				,	encoding=self.document.docinfo.encoding
				,	standalone=self.document.docinfo.standalone
				,	pretty_print=True
			)
			inkex.debug("Created file:  " + totalname)

if __name__ == '__main__':
	e = Combinator()
	e.affect()
