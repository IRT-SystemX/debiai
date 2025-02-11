import modules.dataProviders.DataProviderException as DataProviderException
import modules.dataProviders.dataProviderManager as data_provider_manager
import modules.dataProviders.pythonDataProvider.PythonDataProvider as PythonDataProvider


# Project
def post_project(data):
    # Ask a data provider to create a project
    dataProviderId = "Python module Data Provider"
    projectName = data["projectName"]

    # Check project name
    if len(projectName) > 100:
        return "Project name too long", 400

    # Create project
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        project = data_provider.create_project(projectName)

        # Adding data provider id to project
        project["dataProviderId"] = dataProviderId

        return project, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


# Blocklevel
def post_blocklevels(dataProviderId, projectId, blocklevels):
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.update_block_structure(projectId, blocklevels)
        return blocklevels, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


# Expected_results
def post_resultsStructure(dataProviderId, projectId, resultStructure):
    # Add the expected results structure
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.update_results_structure(projectId, resultStructure)
        return resultStructure, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_block_tree(dataProviderId, projectId, data):
    # Add data to a project from a tree
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return data_provider.add_block_tree(projectId, data), 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


# Add model results
def add_results_dict(dataProviderId, projectId, modelId, data):
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.add_results_dict(projectId, modelId, data)
        return "Results added", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
