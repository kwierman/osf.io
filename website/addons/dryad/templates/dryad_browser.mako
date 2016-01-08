<div class="panel panel-default">
    <div class="panel-heading clearfix">
        <h3 class="panel-title">Package Chooser</h3>
        <div class="help-block">
            <p data-bind="text: message, attr.class: messageClass"></p>
        </div>
    </div>
    <div id="DryadBrowserScope" class="panel-body">
        <div class="row col-xs-12">
            <form data-bind="submit: search">
                <input id="search_terms"
                    type="text"
                    data-bind="value: searchTerms, enterkey: search"
                    placeholder="Search Archive"></input>
                    <button class="btn btn-default">Search</button>
                </form>
                <div class="pull-right">
                    Viewing
                    <span data-bind="text: firstIndex"></span> -
                    <span data-bind="text: lastIndex"></span>
                    of
                    <span data-bind="text: totalResults"></span>
                </div>
            </div>
            <div class="row col-xs-12">
                <span class = "pull-right">
                    <!-- Feel free to correct the line wrapping-->
                    <button data-bind="click: getNext,
                        css: { 'btn-success active':
                        lastIndex() != totalResults(),
                        'disabled':
                        lastIndex() === totalResults()}"
                        class="btn">
                        Next
                    </button>
                </span>
                <span class = "pull-left">
                    <button data-bind="click: getPrevious,
                        css: { 'btn-success active':
                        firstIndex() != 0,
                        'disabled': firstIndex() ==0 }"
                        class="btn">
                        Previous
                    </button>
                </span>
            </div>
            <div class="row col-xs-12">
                <hr/>
                <div id="spinner-loading"
                    class="spinner-loading-wrapper">
                    <div class="logo-spin logo-lg"></div>
                    <p class="m-t-sm fg-load-message">
                        Loading Dryad Archive...
                    </p>
                </div>
                <div class="result_wrapper">
                    <div data-bind="foreach: packages">
                        <div class="panel panel-default">
                            <div class="panel-heading clearfix"
                                data-bind="click: $parent.clickPackage">
                                <span data-bind="text: title"
                                    class="panel-title">
                                </span>
                                <span class="pull-right">
                                    <small>(Click to Expand)</small>
                                </span>
                            </div>
                            <div data-bind="visible: isVisible"
                                class="panel-body">
                                <div class="row">
                                    <div class="col-sm-4">
                                        <a data-bind="attr: {href: ident}">
                                            Link to Dryad Profile
                                        </a>
                                    </div>
                                    <div class="col-sm-8">
                                        <button data-bind="click:
                                            $parent.setDOI"
                                            class="btn btn-success">
                                            Set Current Package to This
                                        </button>
                                    </div>
                                </div>
                                <hr/>
                                <div data-bind="click:
                                    $parent.clickPackage">
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>Authors</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text: authors">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>Date Submitted</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text:
                                                date_submitted">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>Date Available</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text:
                                                date_available">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>Subjects</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text: subjects">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>Description</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text:
                                                description">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>
                                                Scientific Names
                                            </strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text:
                                                scientific_names">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>Temporal Info</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text:
                                                temporal_info">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>References</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text:
                                                references">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <strong>Files</strong>
                                        </div>
                                        <div class="col-sm-8">
                                            <em data-bind="text: files">
                                            </em>
                                        </div>
                                    </div>
                                    <hr/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <hr/>
            </div>
            <div class="row col-xs-12">
                <span class = "pull-right">
                    <button data-bind="click: getNext, css: {
                        'btn-success active':
                        lastIndex() != totalResults(),
                        'disabled':lastIndex()==totalResults()}"
                        class="btn">
                        Next
                    </button>
                </span>
                <span class = "pull-left">
                    <button data-bind="click: getPrevious, css: {
                        'btn-success active': firstIndex() != 0,
                        'disabled': firstIndex() ==0 }" class="btn">
                        Previous
                    </button>
                </span>
            </div>
        </div>
    </div>
</div>
