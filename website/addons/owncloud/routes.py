# -*- coding: utf-8 -*-
"""Routes for the owncloud addon.
"""

from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from . import views

# Routes that use the web renderer
web_routes = {
    'rules': [

        ##### View file #####
    #     Rule(
    #         [
    #             '/project/<pid>/owncloud/files/<path:path>',
    #             '/project/<pid>/node/<nid>/owncloud/files/<path:path>',
    #         ],
    #         'get',
    #         views.crud.owncloud_view_file,
    #         OsfWebRenderer('../addons/owncloud/templates/owncloud_view_file.mako'),
    #     ),


    #     ##### Download file #####
    #     Rule(
    #         [
    #             '/project/<pid>/owncloud/files/<path:path>/download/',
    #             '/project/<pid>/node/<nid>/owncloud/files/<path:path>/download/',
    #         ],
    #         'get',
    #         views.crud.owncloud_download,
    #         notemplate,
    #     ),
    ],
}

# JSON endpoints
api_routes = {
    'rules': [

        ##### Node settings #####

        Rule(
            ['/project/<pid>/owncloud/config/',
            '/project/<pid>/node/<nid>/owncloud/config/'],
            'get',
            views.owncloud_config_get,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/owncloud/config/',
            '/project/<pid>/node/<nid>/owncloud/config/'],
            'put',
            views.owncloud_config_put,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/owncloud/config/',
            '/project/<pid>/node/<nid>/owncloud/config/'],
            'delete',
            views.owncloud_deauthorize,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/owncloud/config/import-auth/',
            '/project/<pid>/node/<nid>/owncloud/config/import-auth/'],
            'put',
            views.owncloud_import_user_auth,
            json_renderer
        ),
    ],

    ## Your routes here

    'prefix': '/api/v1'
}
