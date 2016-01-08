<%inherit file="project/project_base.mako"/>
<h1>Dryad Browser</h1>

<div class="col-sm-4">
    <%include file="dryad/templates/dryad_status.mako"/>
</div><!-- end col-sm-4 -->

<div  class="col-sm-8">
    <%include file="dryad/templates/dryad_browser.mako"/>
</div><!-- end col-sm-8 -->

<!-- The rest of this page is saved for the eventual v2 integration -->

<%def name="javascript_bottom()">
    <% import json %>
    ${parent.javascript_bottom()}
    <script src=${"/static/public/js/dryad-browser-page.js" | webpack_asset}>
    </script>
</%def>
