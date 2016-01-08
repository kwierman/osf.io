# -*- coding: utf-8 -*-
from framework.routing import Rule, json_renderer
from website.addons.dryad import views
from website.routes import OsfWebRenderer

TEMPLATE_DIR = '../addons/dryad/templates/'


api_routes = {'rules':
    [
        Rule(
            [
                '/project/<pid>/dryad/settings',
                '/project/<pid>/node/<nid>/dryad/settings',
            ],
            'get',
            views.dryad_settings,
            json_renderer,
        ),

        Rule(
            [
                '/project/<pid>/dryad/validate',
                '/project/<pid>/node/<nid>/dryad/validate',
            ],
            'get',
            views.dryad_validate_doi,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/set',
                '/project/<pid>/node/<nid>/dryad/set',
            ],
            'post',
            views.dryad_set_doi,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/unset',
                '/project/<pid>/node/<nid>/dryad/unset',
            ],
            'get',
            views.dryad_unset_doi,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/metadata',
                '/project/<pid>/node/<nid>/dryad/metadata',
            ],
            'get',
            views.dryad_get_current_metadata,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/browse',
                '/project/<pid>/node/<nid>/dryad/browse',
            ],
            'get',
            views.dryad_list_objects,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dryad/search',
                '/project/<pid>/node/<nid>/dryad/search',
            ],
            'get',
            views.dryad_search_objects,
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
    ]
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
