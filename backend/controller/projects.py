#############################################################################
# Imports
#############################################################################
import modules.dataProviders.DataProviderException as DataProviderException
import modules.dataProviders.dataProviderManager as data_provider_manager

#############################################################################
# PROJECTS Management
#############################################################################


def ping():
    return "Online v0.15.1", 200


def get_projects():
    # return a list of project overviews
    data_providers_list = data_provider_manager.get_data_provider_list()
    projectOverviews = []
    for data_provider in data_providers_list:
        try:
            projects = data_provider.get_projects()

            if projects is not None:
                # Adding data provider id to projects
                for project in projects:
                    project["dataProviderId"] = data_provider.name

                projectOverviews.extend(projects)

        except DataProviderException.DataProviderException as e:
            print("Warning get DP projects : " + e.message)

    return projectOverviews, 200


def get_project(dataProviderId, projectId):
    # return the info about datasets, models, selections & tags
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        project = data_provider.get_project(projectId)

        # Adding data provider id to project
        project["dataProviderId"] = dataProviderId

        return project, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def delete_project(dataProviderId, projectId):
    # Delete a project
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        data_provider.delete_project(projectId)
        return "Project deleted", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
