# -*- coding: utf-8 -*-

import logging

import numpy as np
import ROOT
import sys

class MplGraph:

	def __init__(self, root_object):
		if not isinstance(root_object, ROOT.TGraph): 
			raise TypeError(str(root_object.ClassName()) + ' does not inherit from TGraph.')
		self.name = root_object.GetName()
		self.root_object = root_object
		# self.classname = root_object.ClassName()
		self.title = root_object.GetTitle()
		self.xlabel = root_object.GetXaxis().GetTitle()
		self.ylabel = root_object.GetYaxis().GetTitle()
		# Number of bins without underflow/overflow bin
		self.x = np.zeros((root_object.GetN()))
		self.y = np.zeros((root_object.GetN()))

		for i in xrange(root_object.GetN()):
			tmpX, tmpY = ROOT.Double(0), ROOT.Double(0)
			root_object.GetPoint(i, tmpX, tmpY)
			self.x[i] = tmpX
			self.y[i] = tmpY
		self.xerr = np.array([root_object.GetErrorX(i) for i in xrange(root_object.GetN())])
		self.xerrl = np.array([root_object.GetErrorXlow(i) for i in xrange(root_object.GetN())])
		self.xerru = np.array([root_object.GetErrorXhigh(i) for i in xrange(root_object.GetN())])
		self.yerr = np.array([root_object.GetErrorY(i) for i in xrange(root_object.GetN())])
		self.yerrl = np.array([root_object.GetErrorYlow(i) for i in xrange(root_object.GetN())])
		self.yerru = np.array([root_object.GetErrorYhigh(i) for i in xrange(root_object.GetN())])

	@property
	def xbinedges(self):
		return np.concatenate((self.xl, self.xu[-1:]))

	@property
	def xl(self):
		return self.x - self.xerrl

	@property
	def xu(self):
		return self.x + self.xerru

	@property
	def yl(self):
		return self.y - self.yerrl

	@property
	def yu(self):
		return self.y + self.yerru


class MplObject1D(object):
	"""Simple representation of 1D or 2D Root histogram to be used for matplotlib plotting."""

	def __init__(self, root_object):

		# lists of ROOT classes which can be converted
		histos_1d = ['TH1D', 'TH1F', 'TProfile']
		self.name = root_object.GetName()
		self.root_object = root_object
		self.title = root_object.GetTitle()
		self.xlabel = root_object.GetXaxis().GetTitle()
		self.ylabel = root_object.GetYaxis().GetTitle()

		if root_object.ClassName() in histos_1d:
			#labeled bins
			self.xlabels = np.array([root_object.GetXaxis().GetBinLabel(i) for i in xrange(1, root_object.GetNbinsX() +1)])
			#if GetBinLabel is empty, the returned strings have length 0. Sum of Zeroes is 0, so set self.xlabels to None
			self.xlabels = self.xlabels if(sum(np.array([len(i) for i in self.xlabels]))) else None

			# bin center
			self.x = np.array([root_object.GetXaxis().GetBinCenter(i) for i in xrange(1, root_object.GetNbinsX() +1)])
			# lower bin edge
			self.xl = np.array([root_object.GetXaxis().GetBinLowEdge(i) for i in xrange(1, root_object.GetNbinsX() +1)])
			# upper bin edge
			self.xu = np.array([root_object.GetXaxis().GetBinUpEdge(i) for i in xrange(1, root_object.GetNbinsX() +1)])
			self.xerr = self.x - self.xl
			# bin content
			self.y = np.array([root_object.GetBinContent(i) for i in xrange(1, root_object.GetNbinsX() +1)])
			# bin content
			self.yerr = np.array([root_object.GetBinError(i) for i in xrange(1, root_object.GetNbinsX() +1)])
			# lower bin error
			self.yerrl = np.array([root_object.GetBinErrorLow(i) for i in xrange(1, root_object.GetNbinsX() +1)])
			# upper bin error
			self.yerru = np.array([root_object.GetBinErrorUp(i) for i in xrange(1, root_object.GetNbinsX() +1)])
		elif isinstance(root_object, ROOT.TGraph): 
			self.x = np.zeros((root_object.GetN()))
			self.y = np.zeros((root_object.GetN()))
			for i in xrange(root_object.GetN()):
				tmpX, tmpY = ROOT.Double(0), ROOT.Double(0)
				root_object.GetPoint(i, tmpX, tmpY)
				self.x[i] = tmpX
				self.y[i] = tmpY
			self.xerr = np.array([root_object.GetErrorX(i) for i in xrange(root_object.GetN())])
			self.xl = np.array([self.x[i] - root_object.GetErrorXlow(i) for i in xrange(root_object.GetN())])
			self.xu = np.array([self.x[i] + root_object.GetErrorXhigh(i) for i in xrange(root_object.GetN())])
			self.yerr = np.array([root_object.GetErrorY(i) for i in xrange(root_object.GetN())])
			self.yerrl = np.array([root_object.GetErrorYlow(i) for i in xrange(root_object.GetN())])
			self.yerru = np.array([root_object.GetErrorYhigh(i) for i in xrange(root_object.GetN())])
		else:
			raise TypeError(str(root_object.ClassName()) + ' cannot be converted to an MPLObject1d.')


	@property
	def xerrl(self):
		return self.x - self.xl

	@property
	def xerru(self):
		return self.xu - self.x

	@property
	def xbinwidth(self):
		return self.xu -self.xl

	@property
	def xbinedges(self):
		return np.concatenate((self.xl, self.xu[-1:]))

	@property
	def ybinwidth(self):
		return self.yu - self.yl

	@property
	def ybinedges(self):
		return np.concatenate((self.yl, self.yu[-1:]))

	@property
	def yl(self):
		return self.bincontents - self.binerrorsl

	@property
	def yu(self):
		return self.bincontents + self.binerrorsu
