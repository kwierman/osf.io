'use strict';

var ko = require('knockout');
var bootbox = require('bootbox');
require('knockout.punches');
var Raven = require('raven-js');
var $osf = require('js/osfHelpers');

function ViewModel(url, nodeSettings) {
    var self = this;
    self.nodeSettings = nodeSettings;
    self.url = url;
    self.urls = ko.observable();
    self.inSearchMode = false;
    self.doi = ko.observable("");
    self.totalResults = ko.observable(0);
    self.firstIndex = ko.observable(0);
    self.lastIndex = ko.observable(0);
    self.packages = ko.observableArray();
    self.searchTerms  = ko.observable("");

    self.message = ko.observable("");
    self.messageClass = ko.observable("");

    self.messages = {
        browseError: ko.pureComputed(function() {
            return 'Could not retrieve settings. Please refresh the page or ' +
                'contact <a href="mailto: support@osf.io">support@osf.io</a> if the ' +
                'problem persists.';
        }),
        searchError: ko.pureComputed(function(){
            return 'DOI Successfully Validated: '+self.doi();
        }),
        noResultsError: ko.pureComputed(function(){
            return 'Could Not Validate DOI: '+self.doi();
        }),
        communicationFailure: ko.pureComputed(function(){
            return "Failed to Communicate with Dryad Servers. Try Again later.";
        }),
    };

    $.getJSON(self.url).done(function(response){
        self.urls(response.urls);
        self.browseTo(20,0);
    }).fail(function(xhr, textStatus, error){
        self.changeMessage(self.messages.browseError(),
        'text-danger');
        Raven.captureMessage(self.messages.browseError(), {
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

ViewModel.prototype.browseTo = function(count, start_n){
  var self = this;
  $('#spinner-loading').show();
  $('.result_wrapper').hide();
  $.get(self.urls().dryad_list_objects, {'count': count,'start': start_n})
      .done(function (response) {
          self.firstIndex(response.start);
          self.totalResults(response.total);
          self.lastIndex(response.end);
          ko.utils.arrayForEach(response.package_list,
            function (d_pack) {
              d_pack["isVisible"] = ko.observable(false);
            });
          self.packages(response.package_list);
          $('#spinner-loading').hide();
          $('.result_wrapper').show();
      })
      .fail(function (xhr, status, error) {
          $('#spinner-loading').hide();
          $('.result_wrapper').show();
      self.changeMessage(self.messages.browseError(), 'text-warning',3000);

        Raven.captureMessage(self.messages.browseError(),
          {
              url: self.urls.dryad_browse,
              textStatus: status,
              error: error
          });
      });
};

ViewModel.prototype.searchTo = function(query, count, start){
    var self = this;
    self.inSearchMode = true;
    $('#spinner-loading').show();
    $('.result_wrapper').hide();
    $.get(self.urls.dryad_search,
        {'query': self.searchTerms(),
        'count': count,
        'start': start
        }
    )
    .done(function (response) {
        self.firstIndex(response.start);
        self.totalResults(response.total);
        self.lastIndex(response.start+count);

        ko.utils.arrayForEach(response.package_list,
            function (d_pack) {
                d_pack["isVisible"] = ko.observable(false);
            }
        );
        self.packages(response.package_list);
        $('#spinner-loading').hide();
        $('.result_wrapper').show();
    })
    .fail(function (xhr, status, error) {
        self.changeMessage(self.messages.searchError(), 'text-danger',3000);
        Raven.captureMessage(self.messages.searchError(),
        {
            url: self.urls.dryad_search,
            textStatus: status,
            error: error
        });
    });
};


ViewModel.prototype.getNext = function() {
    var self = this;
    var count = self.lastIndex() - self.firstIndex();
    var start_n = self.lastIndex()+1;
    if(self.inSearchMode){
      self.searchTo(self, searchTerms, count, start_n);
    }
    else{
      self.browseTo(count, start_n);
    }
};

ViewModel.prototype.getPrevious = function() {
    var self = this;
    var count = self.lastIndex() - self.firstIndex();
    var start_n = self.firstIndex()-count-1;
    if(self.inSearchMode){
      self.searchTo(self, searchTerms, count, start_n);
    }
    else{
      self.browseTo(count, start_n);
    }
};

ViewModel.prototype.search = function() {
  var self = this;
  self.searchTo(self.searchTerms(), 20,0);
};

ViewModel.prototype.setDOI = function(dryad_package) {
    var self= this;
    self.nodeSettings.viewModel.doi(dryad_package.doi);
    self.nodeSettings.viewModel.setDOI().done(function(){
        self.nodeSettings.viewModel.refreshMetadata();
    });
};

ViewModel.prototype.clickPackage = function(dryad_package) {
    dryad_package.isVisible(!dryad_package.isVisible());
};

var DryadBrowser =  function (selector, url, nodeSettings) {
    var self = this;
    self.selector = selector;
    self.viewModel = new ViewModel(url, nodeSettings);
    $osf.applyBindings(self.viewModel, selector);
};

module.exports = {
    DryadBrowser: DryadBrowser,
    _DryadBrowserViewModel: ViewModel
};
