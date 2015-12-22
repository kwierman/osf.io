# -*- coding: utf-8 -*-
from framework.routing import Rule, json_renderer
from website.addons.dryad import views
from website.routes import OsfWebRenderer

TEMPLATE_DIR = '../addons/dryad/templates/'


api_routes = {'rules':
    [
        Rule(
            [
                '/project/<pid>/dryad/validate',
                '/project/<pid>/node/<nid>/dryad/validate',
            ],
            'get',
            views.validate_dryad_doi,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/set',
                '/project/<pid>/node/<nid>/dryad/set',
            ],
            'post',
            views.set_dryad_doi,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/unset',
                '/project/<pid>/node/<nid>/dryad/unset',
            ],
            'get',
            views.unset_dryad_doi,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/browse',
                '/project/<pid>/node/<nid>/dryad/browse',
            ],
            'get',
            views.list_dryad_objects,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/search',
                '/project/<pid>/node/<nid>/dryad/search',
            ],
            'get',
            views.search_dryad_objects,
            json_renderer,
        ),
    ],  
    'prefix': '/api/v1'
}

page_routes = {'rules':
    [
        Rule(
            [
                '/project/<pid>/dryad/',
                '/project/<pid>/node/<nid>/dryad/',
            ],
            'get',
            views.dryad_page,
            OsfWebRenderer('../addons/dryad/templates/dryad_page.mako'),
        ),
    ],
    'prefix': '/api/v1'
}

hgrid_routes = {'rules':
    [


        Rule(
            [
                '/project/<pid>/dryad/hgrid/root/',
                '/project/<pid>/node/<nid>/dryad/hgrid/root/',
            ],
            'get',
            views.dryad_addon_folder,
            json_renderer,
        ),
    ],
    'prefix': '/api/v1'
}
