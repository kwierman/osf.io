'use strict';

var ko = require('knockout');
require('knockout.punches');
var Raven = require('raven-js');
var $osf = require('js/osfHelpers');

function ViewModel(url) {
    var self = this;
    self.url = url;
    self.urls = ko.observable();
    self.doi = ko.observable("");
    self.title = ko.observable("");
    self.ident= ko.observable("");
    self.authors= ko.observable("");
    self.dateSubmitted= ko.observable("");
    self.dateAvailable= ko.observable("");
    self.description= ko.observable("");
    self.subjects= ko.observable("");
    self.scientificNames= ko.observable("");
    self.temporalInfo= ko.observable("");
    self.references= ko.observable("");
    self.files= ko.observable("");

    self.message = ko.observable("");
    self.messageClass = ko.observable("");

    self.messages = {
        userSettingsError: ko.pureComputed(function() {
            return 'Could not retrieve settings. Please refresh the page or ' +
                'contact <a href="mailto: support@osf.io">support@osf.io</a> if the ' +
                'problem persists.';
        }),
        noSettingsWarning: ko.pureComputed(function() {
            return "Dryad package has not yet been set."
        }),
        validateSuccess: ko.pureComputed(function(){
            return 'DOI Successfully Validated: '+self.doi();
        }),
        validateFailure: ko.pureComputed(function(){
            return 'Could Not Validate DOI: '+self.doi();
        }),
        communicationFailure: ko.pureComputed(function(){
            return "Failed to Communicate with Dryad Servers. Try Again later.";
        }),
        setDOISuccess: ko.pureComputed(function(){
            return "DOI Successfully set: "+self.doi();
        }),
        setDOIFailure: ko.pureComputed(function(){
            return "Failed to Set DOI: "+self.doi();
        })
    };

    //init the module
    $.getJSON(self.url).done(function(response){
        self.urls(response.urls);
        if(response.dryad_package_doi){
            self.refreshMetadata();
        }
        else{
            $('#dryad-node-spinner-loading').hide();
            $('#dryad-node-details').hide();
            self.changeMessage(self.messages.noSettingsWarning(),
            'text-warning',
            3000);
        }
    }).fail(function(xhr, textStatus, error){
        self.changeMessage(self.messages.userSettingsError(),
        'text-danger');
        Raven.captureMessage(self.messages.userSettingsError(), {
            url: self.url,
            textStatus: textStatus,
            error: error
        });
    });

}


ViewModel.prototype.changeMessage = function(text, css, timeout) {
    var self = this;
    if (typeof text === 'function') {
        text = text();
    }
    self.message(text);
    var cssClass = css || 'text-info';
    self.messageClass(cssClass);
    if (timeout) {
        // Reset message after timeout period
        setTimeout(function() {
            self.message('');
            self.messageClass('text-info');
        }, timeout);
    }
};


ViewModel.prototype.validateDOI = function() {
    var ret = $.Deferred();
    var self=this;
    var doi = self.doi();
    $.getJSON(self.urls().dryad_validate_doi,
        {'doi' : doi }
        ).done(function(result){
            if(result){
                self.changeMessage(self.messages.validateSuccess(),
                'text-success',
                3000);
                ret.resolve(self.messages.validateSuccess());
            }
            else{
                self.changeMessage(self.messages.validateFailure(),
                'text-danger',3000);
                Raven.captureMessage(self.messages.validateFailure(), {
                    url: self.urls().dryad_validate_doi,
                });
                ret.reject(self.messages.validateFailure());
            }
    }).fail(function(xhr, textStatus, error){
        self.changeMessage(self.messages.communicationFailure(),
        'text-danger',3000);
        Raven.captureMessage(self.messages.communicationFailure(), {
            url: self.urls().dryad_validate_doi,
            textStatus: textStatus,
            error: error
        });
        ret.reject(self.messages.communicationFailure());
    });
    return ret;
};

ViewModel.prototype.setDOI = function() {
    var self = this;
    var doi = self.doi();
    var ret = $.Deferred();
    self.validateDOI().done(function(){
        $.post(self.urls().dryad_set_doi,
                {'doi': doi }
            )
            .done(function (response) {
                if (response){
                    self.changeMessage(self.messages.setDOISuccess(),
                    'test-success',
                    3000);
                    ret.resolve(self.messages.setDOISuccess());
                }
                else{
                    ret.reject(self.messages.setDOIFailure());
                }
            })
            .fail(function (xhr, status, error) {
                self.changeMessage(self.messages.setDOIFailure(),
                'text-danger',
                3000);
                ret.reject(self.messages.setDOIFailure());
                Raven.captureMessage(self.messages.setDOIFailure(), {
                    url: self.urls().dryad_set_doi,
                    textStatus: status,
                    error: error
                });
        });
    });
    return ret;
};

ViewModel.prototype.refreshMetadata = function(){
    var self = this;
    $('#dryad-node-spinner-loading').show();
    $('#dryad-node-details').hide();
    $.get(self.urls().dryad_get_current_metadata)
        .done(function (response) {
            self.doi(response.doi);
            self.title(response.title);
            self.ident(response.ident);
            self.authors(response.authors);
            self.dateSubmitted(response.date_submitted);
            self.dateAvailable(response.date_available);
            self.description(response.description);
            self.subjects(response.subjects);
            self.scientificNames(response.scientificNames);
            self.temporalInfo(response.temporalInfo);
            self.references(response.references);
            self.files(response.files);
            $('#dryad-node-spinner-loading').hide();
            $('#dryad-node-details').show();
    })
    .fail(function (xhr, status, error) {
        self.changeMessage(self.messages.userSettingsError(),
        'text-danger',3000);
        $('#dryad-node-spinner-loading').hide();
        $('#dryad-node-details').show();
        Raven.captureMessage(self.messages.userSettingsError(), {
            url: self.urls().dryad_meta,
            textStatus: status,
            error: error
        });
    });
};

var DryadNodeConfig =  function (selector, url) {
    var self = this;
    self.selector = selector;
    self.viewModel = new ViewModel(url);
    $osf.applyBindings(self.viewModel, self.selector);
};

module.exports = {
    DryadNodeConfig: DryadNodeConfig,
    _DryadNodeConfigViewModel: ViewModel
};
