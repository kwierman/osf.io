from . import model
from . import routes
from . import views

MODELS = [
    model.AddonOwncloudUserSettings,
    model.AddonOwncloudNodeSettings,
]
USER_SETTINGS_MODEL = model.AddonOwncloudUserSettings
NODE_SETTINGS_MODEL = model.AddonOwncloudNodeSettings
ROUTES = [routes.api_routes, routes.web_routes]
SHORT_NAME = 'owncloud'
FULL_NAME = 'ownCloud'
OWNERS = ['user', 'node']
VIEWS = []
CONFIGS = ['node']

CATEGORIES = ['storage']

HAS_HGRID_FILES = True
GET_HGRID_DATA = views.hgrid.owncloud_hgrid_data
