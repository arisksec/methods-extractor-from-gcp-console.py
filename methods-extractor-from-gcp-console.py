import requests

headers = {
    "Authorization": "SAPISIDHASH [sapisidhash]",
    "Origin": "https://console.cloud.google.com",
}

cookies = {
    "SID": "",
    "HSID": "",
    "SSID": "",
    "APISID": "",
}

project_id = ""

dataquery_json = '[{"dataSelector":[{"entityType":{"dataEntityType":"MARKETPLACE_BROWSE_PRODUCTS"},"requestParameters":{"@type":"type.googleapis.com/google.internal.cloud.console.clientapi.marketplace.BrowseProductsRequestParameters","solutionScopeId":"API_CLOUD_CONSOLE","selectedFacetValues":[{"facetId":"visibility","facetValueId":"public"}],"query":"","pageToken":"[pagetoken]","locale":"en_US","isPrivateCatalog":false,"responseType":"UNSPECIFIED","projectNumber":"959808076769","projectId":"' + project_id + '"},"queryId":"0","parameters":{"CLIENT_MODS":"anthos_migrate_ui,anthos_payg,context_aware_access"}}]}]'
methods_json = '{"query":"query GetServiceInfoWithApis($projectId: String!, $serviceName: String!) @Signature(bytes: \\"1/lm4Tp46Vgz\\") {\\n  getService(projectId: $projectId, serviceName: $serviceName) {\\n    config {\\n      name\\n      title\\n      legacyName\\n      legacyLearnMoreUrl\\n      legacyRequestQuotaUrl\\n      legacyPricingLink\\n      documentationSummary\\n      isPrivate\\n      isNativeToMonarch\\n      apiVersions\\n      oauthScopes\\n      usage {\\n        requirements\\n      }\\n      apis {\\n        version\\n        name\\n        methods {\\n          name\\n        }\\n        options {\\n          name\\n        }\\n      }\\n    }\\n  }\\n}","variables":{"projectId":"' + project_id + '","serviceName":"[servicename]"}}'

services = []
methods = []

nextPageToken = ""
final_page = False
while not final_page:
    r = requests.post("https://cloudconsole-pa.clients6.google.com/v1/dataquery?key=AIzaSyCI-zsRP85UVOi0DjtiCwWBwQ1djDy741g", cookies=cookies, headers=headers, data=dataquery_json.replace("[pagetoken]", nextPageToken))
    dataquery_reponse = r.json()
    if not "nextPageToken" in dataquery_reponse[0]["dataSelectorResult"]["data"][0]:
        final_page = True
    else:
        nextPageToken = dataquery_reponse[0]["dataSelectorResult"]["data"][0]["nextPageToken"]
    
    for card in dataquery_reponse[0]["dataSelectorResult"]["data"][0]["shelfs"][0]["cards"]:
        services.append(card["serviceId"])

print(len(services))

currentService = 1
for service in services:
    print(f"[{currentService}/{len(services)}]", end="\r")
    currentService+= 1
    r = requests.post("https://cloudconsole-pa.clients6.google.com/graphql/SERVICE_USAGE_GRAPHQL?key=AIzaSyCI-zsRP85UVOi0DjtiCwWBwQ1djDy741g", cookies=cookies, headers=headers, data=methods_json.replace("[servicename]", service))
    methods_reponse = r.json()
    for api in methods_reponse[0]["data"]["getService"]["config"]["apis"]:
        for method in api["methods"]:
            methods.append(api["name"] + "." + method["name"])

with open('methods.txt', "w") as file:
    for method in methods:
        file.write(method + "\n")
