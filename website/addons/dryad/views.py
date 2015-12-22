import logging

from flask import request
from framework.flask import redirect
from urllib2 import HTTPError

from website.project.decorators import must_have_addon, must_be_valid_project
from website.project.views.node import _view_project

from website.util import rubeus

from website.project.decorators import must_be_contributor_or_public

logger = logging.getLogger(__name__)

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_validate_doi(node_addon, **kwargs):
    doi = request.args["doi"]
    return {'result':check_dryad_doi(doi)}

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_set_doi(node_addon, **kwargs):
    try:
        auth = kwargs['auth']
        doi = kwargs['doi']
        title = get_dryad_title(doi)
        ret = node_addon.set_doi(doi, title, auth)
        node_addon.save()
        return {'result':ret}
    except AddonError:
        return  {'result':False}

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_unset_doi(node_addon, **kwargs):
    try:
        doi = request.args["doi"]
        node_addon.dryad_doi_list.remove(doi)
        node_addon.save()
        return {'result':True}
    except AddonError:
        return {'result':False}

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_list_objects(**kwargs):
    node = kwargs['node']
    pid = kwargs['pid']
    auth = kwargs['auth']

    count = int(request.args["count"]) if "count" in request.args else 10
    start = int(request.args["start"]) if "start" in request.args else 0
    return get_file_list_as_json(count, start)

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_search_objects(**kwargs):
    node = kwargs['node']
    pid = kwargs['pid']
    auth = kwargs['auth']

    count = int(request.args["count"]) if "count" in request.args else 10
    start = int(request.args["start"]) if "start" in request.args else 0
    query = request.args['query'] if 'query' in request.args else ''
    return get_dryad_search_results_as_json(count, start, query)



@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_page(**kwargs):
    node = kwargs['node']
    pid = kwargs['pid']
    auth = kwargs['auth']
    dryad_addon = node.get_addon('dryad')
    ret.update(dryad.config.to_json())
    ret.update(_view_project(node, auth, primary=True))
    return ret

def dryad_addon_folder(node_settings, auth, **kwargs):
    # Quit if no dataset linked
    if node_settings.dryad_package_doi is None:
        return []

    node = node_settings.owner
    urls = {
        'download': 'http://api.datadryad.org/mn/object/' + node_settings.dryad_package_doi.replace('/http://dx.doi.org/', 'doi:') + '/bitstream',
        'view': 'http://api.datadryad.org/mn/object/' + node_settings.dryad_package_doi.replace('/http://dx.doi.org/', 'doi:')
    }

    root = rubeus.build_addon_root(
        node_settings=node_settings,
        name=node_settings.folder_name,
        doi=node_settings.dryad_package_doi,
        permissions=auth,
        nodeUrl=node.url,
        nodeApiUrl=node.api_url,
        urls=urls
    )

    return [root]

@must_be_contributor_or_public
@must_have_addon('dryad', 'node')
def dryad_root_folder_public(node_addon, auth, **kwargs):
    return dryad_addon_folder(node_addon, auth=auth)
