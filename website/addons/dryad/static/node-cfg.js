'use strict';

var DryadConfig = require('./dryadNodeConfig').DryadNodeConfig;

var api_url = window.contextVars.node.urls.api;
var url = api_url+'dryad/settings';

var config = new DryadConfig('#dryadScope', url);
