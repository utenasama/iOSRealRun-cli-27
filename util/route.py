# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
import ast
import math

def parse_route(content):
    tmp = ast.literal_eval("[{}]".format(content))
    if len(tmp) < 2:
        raise ValueError("路线至少需要两个坐标点")
    for i in tmp:
        i["lat"] = float(i["lat"])
        i["lng"] = float(i["lng"])
        if not (math.isfinite(i["lat"]) and -90 <= i["lat"] <= 90
                and math.isfinite(i["lng"]) and -180 <= i["lng"] <= 180):
            raise ValueError("路线包含无效坐标")
    return tmp
