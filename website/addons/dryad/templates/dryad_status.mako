<div  id="DryadStatusScope" class="panel panel-default">
    <div class="panel-heading clearfix">
        <h3 class="panel-title">
            Current Package
        </h3>
    </div>
    <div id="dryad-node-spinner-loading" class="spinner-loading-wrapper">
        <div class="logo-spin logo-lg"></div>
        <p class="m-t-sm fg-load-message">
            Loading Current Package...
        </p>
    </div>
    <div id="dryad-node-details" class="panel-body">
        <div class="row">
            <div class="col-sm-4">
                <strong>Title</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: title"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Link</strong>
            </div>
            <div class="col-sm-8">
                <a data-bind="attr: {href: ident}">
                    Click here
                </a>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>DOI</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: doi"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Authors</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: authors"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Date Submitted</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: dateSubmitted"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Date Available</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: dateAvailable"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Description</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: description"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Subject List</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: subjects"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Scientific Names</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: scientificNames"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Temporal Info</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: temporalInfo"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Referenced DOIs</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: references"></em>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-sm-4">
                <strong>Associated Files</strong>
            </div>
            <div class="col-sm-8">
                <em data-bind="text: files"></em>
            </div>
        </div>

    </div><!-- end panel-body-->
    <span class="help-block">
        <p data-bind="text: message, attr.class: messageClass"></p>
    </span>
</div><!-- end panel -->
