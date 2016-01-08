'use strict';

var DryadBrowser = require('dryadBrowser').DryadBrowser;
// The node config is loaded here to show the
var DryadNodeConfig = require('addons/dryad/static/dryadNodeConfig.js').DryadNodeConfig;

var api_url = window.contextVars.node.urls.api;
var url = api_url+'dryad/settings';
var node_config = new DryadNodeConfig('#DryadStatusScope',url);
// the node config is use here so that the browser can refresh the current package

new DryadBrowser('#DryadBrowserScope',
    url,
    node_config);
