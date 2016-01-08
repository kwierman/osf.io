<div id="${addon_short_name}Scope" class="scripted">
    <h4 class="addon-title">
        <img class="addon-icon" src="${addon_icon_url}"></img>
        ${addon_full_name}
    </h4>
    <span  class=" pull-right">
        <p><strong>Set Package DOI:</strong>
            <form data-bind="submit: setDOI">
                <input id="dryaddoitext" type="text" data-bind="value: doi"
                    placeholder="doi:10.5061/dryad.XXXX">
                <button class="btn btn-success addon-settings-submit">
                    Save
                </button>
            </form>

            </br>
            <!-- ko if: urls() -->
                <strong>OR:</strong>
                <!-- This is a kludge since web_url_for is not defined-->
                <a data-bind="attr: {href: urls().dryad_page }">
                    Browse/Search Dryad for your package
                </a>
            <!-- /ko -->
         </p>
    </span>
    <div class="help-block">
        <p data-bind="text: message, attr.class: messageClass"></p>
    </div>
</div>
