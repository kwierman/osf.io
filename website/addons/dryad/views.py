import logging

from flask import request
from framework.flask import redirect
from urllib2 import HTTPError

from website.project.decorators import must_have_addon, must_be_valid_project

from website.util import rubeus

from website.project.views.node import _view_project
from website.project.decorators import must_be_contributor_or_public

from website.addons.dryad.utils import check_dryad_doi, get_dryad_title, get_package_list_as_json, get_dryad_search_results_json_formatted, get_dryad_title, get_dryad_metadata_as_json

logger = logging.getLogger(__name__)

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_validate_doi(node_addon, **kwargs):
    doi = request.args["doi"]
    return check_dryad_doi(doi)

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_set_doi(node_addon, **kwargs):
    try:
        auth = kwargs['auth']
        doi = request.form['doi']
        title = get_dryad_title(doi)
        ret = node_addon.set_doi(doi, title, auth)
        node_addon.save()
        return ret
    except HTTPError:
        return  False

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_settings(node_addon, **kwargs):
    auth = kwargs['auth']
    return node_addon.to_json(auth.user)

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_get_current_metadata(node_addon, **kwargs):
    doi = node_addon.get_doi()
    ret = {'title':get_dryad_title()}
    ret.update(get_dryad_metadata_as_json(doi))
    return ret

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_unset_doi(node_addon, **kwargs):
    try:
        node_addon.dryad_doi_list.remove(doi)
        node_addon.save()
        return {'result':True}
    except HTTPError:
        return {'result':False}

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_list_objects(**kwargs):
    node = kwargs['node']
    pid = kwargs['pid']

    count = int(request.args["count"]) if "count" in request.args else 10
    start = int(request.args["start"]) if "start" in request.args else 0
    return get_package_list_as_json(start, count)

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_search_objects(**kwargs):
    node = kwargs['node']
    pid = kwargs['pid']
    count = int(request.args["count"]) if "count" in request.args else 10
    start = int(request.args["start"]) if "start" in request.args else 0
    query = request.args['query'] if 'query' in request.args else ''
    return get_dryad_search_results_json_formatted(start, count, query)

@must_be_valid_project
@must_have_addon('dryad', 'node')
def dryad_page(**kwargs):
    node = kwargs['node'] or kwargs['project']
    pid = kwargs['pid']
    auth = kwargs['auth']
    dryad_addon = node.get_addon('dryad')
    ret = _view_project(node, auth, primary=True)
    ret.update(dryad_addon.config.to_json())
    return ret

def dryad_addon_folder(node_settings, auth, **kwargs):
    if node_settings.dryad_package_doi is None:
        return []

    node = node_settings.owner
    root = rubeus.build_addon_root(
        node_settings=node_settings,
        name='',
        permissions=auth,
        user=auth.user,
        nodeUrl=node.url,
        nodeApiUrl=node.api_url,
    )
    return [root]


@must_be_contributor_or_public
@must_have_addon('dryad', 'node')
def dryad_root_folder_public(node_addon, auth, **kwargs):
    return dryad_addon_folder(node_addon, auth=auth)
