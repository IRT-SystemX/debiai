import modules.dataProviders.webDataProvider.http.api as api

from modules.dataProviders.webDataProvider.useCases.models import get_models_info
from modules.dataProviders.webDataProvider.useCases.selections import (
    get_project_selections,
)

from utils.utils import timeNow


def get_all_projects_from_data_provider(url, name):
    projects = api.get_projects(url)
    project_list = []

    if not projects:
        return

    for project_id in projects:
        if "nbSamples" not in projects[project_id]:
            projects[project_id]["nbSamples"] = None

        if "nbModels" not in projects[project_id]:
            projects[project_id]["nbModels"] = None

        if "nbSelections" not in projects[project_id]:
            projects[project_id]["nbSelections"] = None

        if "name" not in projects[project_id]:
            projects[project_id]["name"] = project_id

        project_list.append(
            {
                "id": project_id,
                "dataProvider": name,
                "name": projects[project_id]["name"],
                "nbModels": projects[project_id]["nbModels"],
                "nbSamples": projects[project_id]["nbSamples"],
                "nbSelections": projects[project_id]["nbSelections"],
                "creationDate": timeNow(),
                "updateDate": timeNow(),
            }
        )

    return project_list


def get_single_project_from_data_provider(url, data_provider_name, id_project):
    project = api.get_project(url, id_project)

    # Check the project columns
    project_columns = get_project_columns(project)

    # Add selections
    selections = get_project_selections(url, id_project)

    # Add models
    models = get_models_info(url, id_project)

    # Check nbSamples
    if "nbSamples" in project:
        nbSamples = project["nbSamples"]
    else:
        nbSamples = None

    # Converting views to DebiAI projects
    return {
        "id": id_project,
        "name": project["name"],
        "dataProvider": data_provider_name,
        "columns": project_columns,
        "resultStructure": project["expectedResults"],
        "nbModels": len(models),
        "nbSamples": nbSamples,
        "nbSelections": len(selections),
        "creationDate": timeNow(),
        "updateDate": timeNow(),
        "selections": selections,
        "models": models,
    }


def get_project_columns(project):
    project_columns = []
    # Expected project["columns"] example :
    # [
    #     { "name": "storage", "category": "other" },
    #     { "name": "age", "category": "context" },
    #     { "name": "path", "category": "input" },
    #     { "name": "label", "category": "groundtruth" },
    #     { "name": "type" }, # category is not specified, it will be "other"
    # ]
    if "columns" in project:
        for column in project["columns"]:
            col = {"name": column["name"]}

            if "category" in column:
                col["category"] = column["category"]
            else:
                col["category"] = "other"

            if "type" in column:
                col["type"] = column["type"]
            else:
                col["type"] = "auto"

            project_columns.append(col)

    return project_columns


def delete_project(url, project_id):
    api.delete_project(url, project_id)
