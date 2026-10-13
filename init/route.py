# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
import config

from util import route

def get_route(path=None):
    with (config.BASE_DIR / (path or config.config.routeConfig)).open(encoding="utf-8") as myFile:
        loc = route.parse_route(myFile.read())
    return loc  
