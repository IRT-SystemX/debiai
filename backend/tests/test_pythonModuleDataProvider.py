import requests
import ujson as json

PYTHON_DATA_PROVIDER_ID = "Python module Data Provider"
appUrl = "http://localhost:3000/"
test_project_name = "test_create_project"
test_project_id = None

# ============== PROJECTS =================


def test_get_projects():
    url = appUrl + "projects"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    assert type(json.loads(resp.text)) is list


def test_get_bad_project():
    projectId = "I_DO_NOT_EXIST"
    url = (
        appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + projectId
    )
    resp = requests.request("GET", url, headers={}, data={})
    assert resp.status_code == 404

    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 404


def test_create_project_noName():
    # create
    url = appUrl + "projects"
    resp = requests.post(url=url, headers={}, json={})
    assert resp.status_code == 400


def test_create_project():
    global test_project_id
    # delete if exists
    projectId = test_project_name
    url = (
        appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + projectId
    )
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200 or resp.status_code == 404

    # create
    url = appUrl + "projects"
    resp = requests.post(url=url, headers={}, json={"projectName": test_project_name})
    assert resp.status_code == 200

    # Get Id
    data = json.loads(resp.text)
    test_project_id = data["id"]
    assert test_project_id is not None
    assert len(test_project_id) > 0
    assert type(test_project_id) is str

    # Test can't create same project
    resp = requests.post(url=url, headers={}, json={"projectName": test_project_name})
    assert resp.status_code == 400
    assert "already exists" in resp.text


def test_get_project():
    # Find back
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("GET", url, headers={}, json={})
    assert resp.status_code == 200
    proj = json.loads(resp.text)
    assert type(proj) is dict
    assert type(proj["columns"]) is list
    assert proj["models"] == []
    assert len(proj["name"]) > 0
    assert proj["name"] == test_project_name


def test_remove_project():
    # Project exists back
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("GET", url, headers={}, json={})
    assert resp.status_code == 200

    # remove
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200

    # Dont Find back
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("GET", url, headers={}, json={})
    assert resp.status_code == 404

    # Cant remove again
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 404


def test_project_nameTooLong():
    testProjectName = "a" * 256
    url = appUrl + "projects"
    payload = {"projectName": testProjectName, "blockLevelInfo": []}
    headers = {"content-type": "application/json"}
    resp = requests.post(url=url, headers=headers, json=payload)
    assert resp.status_code == 400


# ============== DATA TEST =================


# # testProjectId = ""

# def test_get_Block():
#     global testProjectId
#     # create Project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects"
#     resp = requests.post(url=url, headers={}, json={})
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     testProjectId = data["id"]
#     print(testProjectId)
#     assert len(testProjectId) > 0

#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks"
#     resp = requests.get(url=url, json={}, headers={})
#     print(resp.text)
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     blocks = data["blocks"]
#     assert blocks == []


# def test_post_block_badProjectName():
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/IDONTEXIST/blocks"
#     payload = {
#         "parentId": "",
#         "blockName": "block1",
#         "groundThruthList": {"toto": "tata"},
#         "inputList": {"toto": "tata"},
#         "contextList": {"toto": "tata"},
#     }
#     headers = {"content-type": "application/json"}
#     resp = requests.post(url=url, json=payload, headers=headers)
#     assert resp.status_code == 404


# def test_post_block_badParents():
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks"

#     payload = {
#         "parentId": "IDONTEXIST",
#         "blockName": "poorBlock",
#         "groundThruthList": {"toto": "tata"},
#         "inputList": {"toto": "tata"},
#         "contextList": {"toto": "tata"},
#     }
#     headers = {"content-type": "application/json"}

#     resp = requests.post(url=url, json=payload, headers=headers)
#     assert resp.status_code == 404


# def test_post_block():
#     blockName = "My first block"
#     # ADD first block
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks"
#     payload = {
#         "blockName": blockName,
#         "parentId": "",
#         "groundThruthList": {"toto": "tata"},
#         "inputList": {"toto": "tata"},
#         "contextList": {"toto": "tata"},
#     }
#     resp = requests.post(
#         url=url, json=payload, headers={"content-type": "application/json"}
#     )
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     blockTestId = data["blockId"]
#     assert len(blockTestId) > 0

#     # Get
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks"
#     resp = requests.get(url=url, json={}, headers={})
#     print(resp.text)
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     blocks = data["blocks"]
#     assert len(blocks) == 1
#     myBlock = blocks[0]
#     assert myBlock["name"] == blockName

#     # add block to the block
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks"
#     payload = {
#         "blockName": "The very second Second",
#         "parentId": blockTestId,
#         "groundThruthList": {"toto": "tata"},
#         "inputList": {"toto": "tata"},
#         "contextList": {"toto": "tata"},
#     }
#     headers = {"content-type": "application/json"}
#     resp = requests.post(url=url, json=payload, headers=headers)
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     secBlockId = data["blockId"]
#     assert len(secBlockId) > 0

#     # Get depth
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks?depth=1"
#     resp = requests.get(url=url, json={}, headers={})
#     print(resp.text)
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     blocks = data["blocks"]
#     assert len(blocks) == 1
#     block = data["blocks"][0]
#     assert type(block["childrenInfoList"]) is list
#     assert len(block["childrenInfoList"]) == 1

#     # Delete
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks/" + secBlockId
#     resp = requests.delete(url=url, json={}, headers={})
#     assert resp.status_code == 200

#     # Get depth
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks?depth=1"
#     resp = requests.get(url=url, json={}, headers={})
#     print(resp.text)
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     blocks = data["blocks"]
#     assert len(blocks) == 1
#     block = data["blocks"][0]
#     assert type(block["childrenInfoList"]) is list
#     assert len(block["childrenInfoList"]) == 0

#     # Delete Again
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks/" + secBlockId
#     resp = requests.delete(url=url, json={}, headers={})
#     assert resp.status_code == 404

#     # Delete First
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks/" + blockTestId
#     resp = requests.delete(url=url, json={}, headers={})
#     assert resp.status_code == 200

#     # Get
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks"
#     resp = requests.get(url=url, json={}, headers={})
#     print(resp.text)
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     blocks = data["blocks"]
#     assert len(blocks) == 0


# def test_delete_block_badProj():
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/IDONTEXIST/blocks/TODELETE"
#     resp = requests.delete(url=url)
#     assert resp.status_code == 404


# def test_delete_block_badBlock():
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId + "/blocks/IDONTEXIST"
#     resp = requests.delete(url=url)
#     assert resp.status_code == 404

#     # remove project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + testProjectId
#     resp = requests.request("DELETE", url, headers={}, data={})
#     assert resp.status_code == 200


# # ============== DATASETS TEST =================


# def test_post_dataset_badProject():
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/IDONTEXIST/datasets/"

#     payload = {"datasetName": "Greate dataset", "blockIdList": []}
#     headers = {"content-type": "application/json"}

#     resp = requests.post(url=url, json=payload, headers=headers)
#     assert resp.status_code == 404


# def test_post_dataset_badBlocks():
#     # Create project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects"
#     payload = {"projectName": "My greate project with dataset",
#                "blockLevelInfo": []}
#     headers = {"content-type": "application/json"}
#     resp = requests.post(url=url, headers=headers, json=payload)
#     assert resp.status_code == 200
#     pId = json.loads(resp.text)["id"]

#     # Add dataset
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId + "/datasets"

#     payload = {
#         "datasetName": "I am a dataset",
#         "blockIdList": ["toto", "IDONTEXIST", "tutu"],
#     }
#     headers = {"content-type": "application/json"}

#     resp = requests.post(url=url, json=payload, headers=headers)
#     assert resp.status_code == 404

#     # remove project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId
#     resp = requests.request("DELETE", url, headers={}, data={})
#     assert resp.status_code == 200


# def test_post_dataset():
#     # Create project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects"
#     payload = {"projectName": "My greate project with dataset",
#                "blockLevelInfo": []}
#     headers = {"content-type": "application/json"}
#     resp = requests.post(url=url, headers=headers, json=payload)
#     assert resp.status_code == 200
#     pId = json.loads(resp.text)["id"]

#     # Get
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId
#     resp = requests.request("GET", url, headers={}, data={})
#     assert resp.status_code == 200
#     proj = json.loads(resp.text)
#     print(proj)
#     assert type(proj) is dict
#     assert proj["datasets"] == []

#     # create dataset
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId + "/datasets"
#     payload = {"datasetName": "I am a dataset",
#                "blockIdList": []}  # empty blocks ref
#     headers = {"content-type": "application/json"}
#     resp = requests.post(url=url, json=payload, headers=headers)
#     assert resp.status_code == 200
#     print(resp.text)
#     datasetId = json.loads(resp.text)["id"]

#     # get Dataset with project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId
#     resp = requests.request("GET", url, headers={}, data={})
#     assert resp.status_code == 200
#     proj = json.loads(resp.text)
#     assert type(proj) is dict
#     assert len(proj["datasets"]) == 1
#     assert proj["datasets"][0]["id"] == datasetId

#     # delete dataset
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId + "/datasets/" + datasetId
#     resp = requests.delete(url=url, json={}, headers={})
#     assert resp.status_code == 200

#     # Delete again
#     resp = requests.delete(url=url, json={}, headers={})
#     assert resp.status_code == 404

#     # remove project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId
#     resp = requests.request("DELETE", url, headers={}, data={})
#     assert resp.status_code == 200


# def test_post_dataset_withCreatedBlock():
#     # Create project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects"
#     payload = {"projectName": "My greate project with dataset",
#                "blockLevelInfo": []}
#     headers = {"content-type": "application/json"}
#     resp = requests.post(url=url, headers=headers, json=payload)
#     assert resp.status_code == 200
#     pId = json.loads(resp.text)["id"]

#     # ADD  block
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId + "/blocks"
#     payload = {
#         "blockName": "My first block",
#         "parentId": "",
#         "groundThruthList": {"toto": "tata"},
#         "inputList": {"toto": "tata"},
#         "contextList": {"toto": "tata"},
#     }
#     resp = requests.post(
#         url=url, json=payload, headers={"content-type": "application/json"}
#     )
#     assert resp.status_code == 200
#     data = json.loads(resp.text)
#     blockTestId = data["blockId"]
#     assert len(blockTestId) > 0

#     # addadataset
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId + "/datasets"
#     payload = {"datasetName": "dataset with blocks",
#                "blockIdList": [blockTestId]}
#     headers = {"content-type": "application/json"}

#     resp = requests.post(url=url, json=payload, headers=headers)
#     print(resp.text)
#     assert resp.status_code == 200

#     # remove project
#     url = appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + pId
#     resp = requests.request("DELETE", url, headers={}, data={})
#     assert resp.status_code == 200
