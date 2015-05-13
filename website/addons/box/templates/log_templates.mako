<script type="text/html" id="box_file_added">
added file
<a class="overflow log-file-link" data-bind="click: NodeActions.addonFileRedirect">
    {{ params.fullPath.replace(/^\//, '') }}</a> to
Box in
<a class="log-node-title-link overflow" data-bind="attr: {href: nodeUrl}">{{ nodeTitle }}</a>
</script>

<script type="text/html" id="box_folder_created">
created folder
<span class="overflow log-folder">{{ params.fullPath.replace(/^\//, '') }}</span> in
Box in
<a class="log-node-title-link overflow" data-bind="attr: {href: nodeUrl}">{{ nodeTitle }}</a>
</script>

<script type="text/html" id="box_file_updated">
updated file
<a class="overflow log-file-link" data-bind="click: NodeActions.addonFileRedirect">
    {{ params.fullPath.replace(/^\//, '') }}</a> to
Box in
<a class="log-node-title-link overflow" data-bind="attr: {href: nodeUrl}">{{ nodeTitle }}</a>
</script>


<script type="text/html" id="box_file_removed">
removed {{ params.path.match(/\/$/) ? 'folder' : 'file' }} <span class="overflow">
    {{ params.name.replace(/^\//, '') }}</span> from
Box in
<a class="log-node-title-link overflow" data-bind="attr: {href: nodeUrl}">{{ nodeTitle }}</a>
</script>


<script type="text/html" id="box_folder_selected">
linked Box folder
<span class="overflow">
    {{ params.folder === 'All Files' ? '/ (Full Box)' : (params.folder || '').replace('All Files','')}}
</span> to
<a class="log-node-title-link overflow" data-bind="attr: {href: nodeUrl}">{{ nodeTitle }}</a>
</script>


<script type="text/html" id="box_node_deauthorized">
deauthorized the Box addon for
<a class="log-node-title-link overflow"
    data-bind="attr: {href: nodeUrl}">{{ nodeTitle }}</a>
</script>


<script type="text/html" id="box_node_authorized">
authorized the Box addon for
<a class="log-node-title-link overflow"
    data-bind="attr: {href: nodeUrl}">{{ nodeTitle }}</a>
</script>
