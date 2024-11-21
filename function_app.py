import json
import urllib
from typing import Any

import azure.functions as fns
import logging

app = fns.FunctionApp(http_auth_level=fns.AuthLevel.ANONYMOUS)

# configuration variables
service_name: str = "sitkum_poi"
service_description: str = "Test service description"
copyright_text: str = "Copyright Joel McCune 2024"

# build path to feature service
service_pth: str = f"services/{service_name}/FeatureServer"
service_layer_pth: str = f"{service_pth}/0"


def get_parameter(req: fns.HttpRequest, param_name: str) -> Any:
    """Try to extract a parameter from a request, either from a URL parameter or the body."""
    # extract submitted parameters from request
    val = req.params.get(param_name)

    # if parameter not located in url parameters
    if not val:

        # try to get the response from the body
        try:
            req_body = req.get_json()

        # if no value provided, do not do anything
        except ValueError:
            pass

        # if parameter passed in POST payload
        else:
            val = req_body.get(param_name)

    # if nothing found value is none
    if not val:
        val = None

    return val


@app.route(route="info")
def server_info(req: fns.HttpRequest) -> fns.HttpResponse:
    """Root server info endpoint."""

    # assemble the dictionary payload for the response
    payload = {
        "currentVersion": 0.1,
        "fullVersion": "0.1.0",
        "owningSystemUrl": "https://azure.app.url",
    }

    # convert the payload to a string
    payload_str = json.dumps(payload, indent=4)

    # assemble the response
    res = fns.HttpResponse(payload_str, status_code=200)

    return res


@app.route(route=service_pth)
def info(req: fns.HttpRequest) -> fns.HttpResponse:
    """Provide service level information for the Feature Service (Geoservice)"""

    # assemble the dictionary payload for the response
    payload = {
        "currentVersion": 0.1,
        "serviceDescription": f"{service_description}",
        "hasStaticData": True,
        "maxRecordCount": 1000,
        "supportedQueryFormats": "JSON",
        "supportedConvertFileFormats": "JSON",
        "supportedFullTextLocales": [
            "neutral",
            "ar-SA",
            "el-GR",
            "en-GB",
            "en-US",
        ],
        "capabilities": "Query",
        "description": "",
        "copyrightText": "",
        "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        "initialExtent": {
            "xmin": -13832297.089522462,
            "ymin": 6098582.19471541,
            "xmax": -13811471.071830537,
            "ymax": 6100341.3632699922,
            "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        },
        "fullExtent": {
            "xmin": -13832297.089522462,
            "ymin": 6098582.19471541,
            "xmax": -13811471.071830537,
            "ymax": 6100341.3632699922,
            "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        },
        "units": "esriMeters",
        "supportsAppend": True,
        "supportsSharedDomains": True,
        "size": 32768,
        "layers": [
            {
                "id": 0,
                "name": service_name,
                "parentLayerId": -1,
                "defaultVisibility": True,
                "subLayerIds": None,
                "minScale": 9244649,
                "maxScale": 0,
                "type": "Feature Layer",
                "geometryType": "esriGeometryPoint",
            }
        ],
    }

    # assemble the response
    res = fns.HttpResponse(json.dumps(payload, indent=4), status_code=200)

    return res


# dict to use for layers and individual layer payloads
layer_dict = {
    "layers": [
        {
            "currentVersion": 0.1,
            "id": 0,
            "name": service_name,
            "type": "Feature Layer",
            "cacheMaxAge": 30,
            "displayField": "",
            "description": service_description,
            "copyrightText": copyright_text,
            "defaultVisibility": True,
            "editingInfo": {
                "lastEditDate": 1731997481705,
                "schemaLastEditDate": 1731995136292,
                "dataLastEditDate": 1731979653122,
            },
            "useStandardizedQueries": True,
            "geometryType": "esriGeometryPoint",
            "minScale": 9244649,
            "maxScale": 0,
            "extent": {
                "xmin": -13832297.089522462,
                "ymin": 6098582.19471541,
                "xmax": -13811471.071830537,
                "ymax": 6100341.3632699922,
                "spatialReference": {"wkid": 102100, "latestWkid": 3857},
            },
            "drawingInfo": {
                "renderer": {
                    "type": "simple",
                    "symbol": {
                        "type": "esriPMS",
                        "url": "RedSphere.png",
                        "imageData": "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",
                        "contentType": "image/png",
                        "width": 15,
                        "height": 15,
                    },
                }
            },
            "hasAttachments": False,
            "htmlPopupType": "esriServerHTMLPopupTypeNone",
            "hasM": False,
            "hasZ": False,
            "objectIdField": "ObjectId",
            "uniqueIdField": {"name": "ObjectId", "isSystemMaintained": True},
            "typeIdField": "",
            "fields": [
                {
                    "name": "name",
                    "type": "esriFieldTypeString",
                    "actualType": "nvarchar",
                    "alias": "name",
                    "sqlType": "sqlTypeNVarchar",
                    "length": 4000,
                    "nullable": True,
                    "editable": True,
                    "domain": None,
                    "defaultValue": None,
                },
                {
                    "name": "type",
                    "type": "esriFieldTypeString",
                    "actualType": "nvarchar",
                    "alias": "type",
                    "sqlType": "sqlTypeNVarchar",
                    "length": 4000,
                    "nullable": True,
                    "editable": True,
                    "domain": None,
                    "defaultValue": None,
                },
                {
                    "name": "lat",
                    "type": "esriFieldTypeDouble",
                    "actualType": "float",
                    "alias": "lat",
                    "sqlType": "sqlTypeFloat",
                    "nullable": True,
                    "editable": True,
                    "domain": None,
                    "defaultValue": None,
                },
                {
                    "name": "lon",
                    "type": "esriFieldTypeDouble",
                    "actualType": "float",
                    "alias": "lon",
                    "sqlType": "sqlTypeFloat",
                    "nullable": True,
                    "editable": True,
                    "domain": None,
                    "defaultValue": None,
                },
                {
                    "name": "ObjectId",
                    "type": "esriFieldTypeOID",
                    "actualType": "int",
                    "alias": "ObjectId",
                    "sqlType": "sqlTypeInteger",
                    "nullable": False,
                    "editable": False,
                    "domain": None,
                    "defaultValue": None,
                },
                {
                    "name": "GlobalID",
                    "type": "esriFieldTypeGlobalID",
                    "alias": "GlobalID",
                    "sqlType": "sqlTypeOther",
                    "length": 38,
                    "nullable": False,
                    "editable": False,
                    "domain": None,
                    "defaultValue": "NEWID() WITH VALUES",
                },
            ],
            "indexes": [
                {
                    "name": "PK__SITKUM_P__9A619291F5D56F1A",
                    "fields": "ObjectId",
                    "isAscending": True,
                    "isUnique": True,
                    "description": "clustered, unique, primary key",
                    "indexType": "Attribute",
                },
                {
                    "name": "user_72591.SITKUM_POI_SITKUM_POI_Shape_sidx",
                    "fields": "Shape",
                    "isAscending": True,
                    "isUnique": False,
                    "description": "Shape Index",
                    "indexType": "Spatial",
                },
                {
                    "name": "GlobalID_Index",
                    "fields": "GlobalID",
                    "isAscending": False,
                    "isUnique": True,
                    "description": "",
                    "indexType": "Attribute",
                },
            ],
            "dateFieldsTimeReference": {
                "timeZone": "UTC",
                "respectsDaylightSaving": False,
            },
            "preferredTimeReference": None,
            "types": [],
            "supportedQueryFormats": "JSON",
            "hasStaticData": True,
            "maxRecordCount": 1000,
            "standardMaxRecordCount": 32000,
            "standardMaxRecordCountNoGeometry": 32000,
            "tileMaxRecordCount": 8000,
            "maxRecordCountFactor": 1,
            "capabilities": "Query",
        }
    ],
}


@app.route(route=f"{service_pth}/layers")
def layers(req: fns.HttpRequest) -> fns.HttpResponse:
    """Provide layers info...infomation on avaialble layers."""
    # build payload with one layer info in a list
    payload_str = json.dumps([layer_dict], indent=4)
    res = fns.HttpResponse(payload_str, status_code=200)
    return res


@app.route(route=service_layer_pth)
def layer(req: fns.HttpRequest) -> fns.HttpResponse:
    """Provide access directly to feature layer."""
    payload_str = json.dumps(layer_dict, indent=4)
    res = fns.HttpResponse(payload_str, status_code=200)
    return res


@app.route(route=f"{service_layer_pth}/query")
def query(req: fns.HttpRequest) -> fns.HttpResponse:

    # log function invocation
    logging.info('Python HTTP trigger function "info" invoked.')

    # try to retrieve name parameter
    where = get_parameter(req, "where")

    # report invocation success but missing parameter if no parameter passed
    if where is None:

        # create the default where clause
        where = "1=1"

        res = fns.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a where clause in the query string or in the request body for a personalized response.",
            status_code=200,
        )

    # report success if parameter value is able to be retrieved
    else:
        res = fns.HttpResponse(
            f"This HTTP triggered function executed successfully.\nwhere clause: {where}"
        )

    return res
