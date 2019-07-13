# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import flask
from flask import Response
import octoprint.printer
from octoprint.events import Events
import json


PLUGIN_KEY_PREFIX = "DisplayLayerProgress_"

class DisplayLayerProgressAPIPlugin(octoprint.plugin.SettingsPlugin,
                                    octoprint.plugin.AssetPlugin,
                                    octoprint.plugin.TemplatePlugin,
									# my stuff
									octoprint.plugin.BlueprintPlugin,
									octoprint.plugin.EventHandlerPlugin
									):

	_lastEvent = None
	_displayLayerPayload = None


	def __init__(self):
		# init your variables
		pass

	# REST - APIs

	# GET http://localhost:5000/plugin/DisplayLayerProgressAPI/echo?text=123
	# -H X-Api-Key: 57FECA453FE94D46851EFC94BC9B5265
	@octoprint.plugin.BlueprintPlugin.route("/echo", methods=["GET"])
	def myEcho(self):
		if not "text" in flask.request.values:
			return flask.make_response("Expected a text to echo back.", 400)
		return flask.request.values["text"]


	@octoprint.plugin.BlueprintPlugin.route("/lastEvent", methods=["GET"])
	def lastEvent(self):
		response = ""
		currentData = self._lastEvent
		if currentData is not None:
			response = json.dumps(currentData)
		return Response(response, mimetype='application/json')

	@octoprint.plugin.BlueprintPlugin.route("/printerState", methods=["GET"])
	def printerState(self):
		response = ""
		currentData = self._printer.get_current_data()
		if currentData is not None:
			response = json.dumps(currentData)
		return Response(response, mimetype='application/json')

	@octoprint.plugin.BlueprintPlugin.route("/displayLayerProgressInfo", methods=["GET"])
	def displayLayerProgressInfo(self):
		response = ""
		if self._displayLayerPayload is not None:
			response = json.dumps(self._displayLayerPayload)

		return Response(response, mimetype='application/json')

	# start/stop event-hook
	def on_event(self, event, payload):

		self._lastEvent = event

		'''
            eventKey = PLUGIN_KEY_PREFIX + updateReason
            eventPayload = dict(
                totalLayer = self._layerTotalCount,
                currentLayer = self._currentLayer,
                lastLayerDuration = lastLayerDuration,
                averageLayerDuration = averageLayerDuration,
                currentHeight = self._currentHeight,
                totalHeightWithExtrusion = self._totalHeightWithExtrusion,
                feedrate = self._feedrate,
                feedrateG0 = self._feedrateG0,
                feedrateG1 = self._feedrateG1,
                fanspeed = self._fanSpeed,
                progress = self._progress,
                printTimeLeft = printTimeLeft,
                printTimeLeftInSeconds = printTimeLeftInSeconds,
            )
		'''


		## handle DisplayLayerProgressValues
		if event.startswith(PLUGIN_KEY_PREFIX):
			self._displayLayerPayload = payload


	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin
	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/DisplayLayerProgressAPI.js"],
			css=["css/DisplayLayerProgressAPI.css"],
			less=["less/DisplayLayerProgressAPI.less"]
		)

	##~~ Softwareupdate hook
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			DisplayLayerProgressAPI=dict(
				displayName="DisplayLayerProgressAPI Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OllisGit",
				repo="OctoPrint-DisplayLayerProgressAPI",
				current=self._plugin_version,

				# update method: pip
				#pip="https://github.com/OllisGit/OctoPrint-DisplayLayerProgressAPI/archive/{target_version}.zip"
				pip = "https://github.com/OllisGit/OctoPrint-DisplayLayerProgressAPI/releases/latest/download/master.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
##__plugin_name__ = "Displaylayerprogressapi Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = DisplayLayerProgressAPIPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

