import re
import pandas as pd
import requests
import json

from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_symbols import (
    ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
    ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS,
    ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES,
    ENDPOINT_URL_PROJECTS_ALL,
    ENDPOINT_URL_PROJECTS_CREATE,
)


def getProjectList(config: ConfigHandler):
    """
    Retrieves a list of projects from the server and returns it as a DataFrame.

    Args:
        config: Configuration object that contains necessary connection settings.

    Returns:
        pd.DataFrame: DataFrame containing the list of projects.

    Raises:
        Exception: If the request to the server fails.
    """
    headers = connection_get_headers(config)

    response = requests.get(
        config.config_get_nemo_url() + ENDPOINT_URL_PROJECTS_ALL, headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    return df


def getProjectID(config: ConfigHandler, projectname: str):
    """
    Retrieves the project ID for a given project name.

    Args:
        config: Configuration object that contains necessary connection settings.
        projectname (str): The name of the project for which to retrieve the ID.

    Returns:
        str: The ID of the specified project.

    Raises:
        Exception: If the project name is not found or if multiple projects match the given name.
    """
    df = getProjectList(config)
    crmproject = df[df["displayName"] == projectname]
    if len(crmproject) != 1:
        raise Exception(f"could not identify project name {projectname}")
    project_id = crmproject["id"].to_list()[0]
    return project_id


def getProjectProperty(config: ConfigHandler, projectname: str, propertyname: str):
    """
    Retrieves a specified property for a given project from the server.

    Args:
        config: Configuration object that contains necessary connection settings.
        projectname (str): The name of the project for which to retrieve the property.
        propertyname (str): The name of the property to retrieve.

    Returns:
        str: The value of the specified property for the given project.

    Raises:
        Exception: If the request to the server fails.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    ENDPOINT_URL = (
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES.format(
            projectId=project_id, request=propertyname
        )
    )

    response = requests.get(ENDPOINT_URL, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )

    return response.text[1:-1]  # cut off leading and trailing "


def getImportedColumns(config: ConfigHandler, projectname: str) -> pd.DataFrame:
    """
    Fetches and returns the imported columns metadata for a given project in the form of a pandas DataFrame.

    Args:
        config (ConfigHandler): Configuration handler instance to access settings and credentials.
        projectname (str): The name of the project for which the imported columns metadata is requested.

    Returns:
        pd.DataFrame: A DataFrame containing the imported columns metadata.

    Raises:
        Exception: If the project ID cannot be retrieved or the HTTP request fails.

    Process:
        1. Initializes request headers using `connection_get_headers`.
        2. Retrieves the project ID using `getProjectID`.
        3. Sends an HTTP GET request to the configured NEMO API endpoint for imported columns.
        4. Parses the JSON response and normalizes it into a pandas DataFrame.
        5. Handles errors such as missing project ID or failed requests.
    """
    try:

        # initialize reqeust
        headers = connection_get_headers(config)
        project_id = getProjectID(config, projectname)
        response = requests.get(
            config.config_get_nemo_url()
            + ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS.format(
                projectId=project_id
            ),
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )
        resultjs = json.loads(response.text)
        df = pd.json_normalize(resultjs)
        return df

    except Exception as e:
        if project_id == None:
            raise Exception("process stopped, no project_id available")
        raise Exception("process aborted")


def createProject(config: ConfigHandler, projectname: str, description: str):
    """
    Creates a new project using the specified configuration and project name.

    This function sends a POST request to the NEMO API to create a project with
    the given name. The project is initialized with default settings and a
    specific structure, ready for further processing.

    Args:
        config (ConfigHandler): An object that provides the necessary configuration
                                for connecting to the NEMO API, such as headers and URL.
        projectname (str): The name of the project to be created.

    Raises:
        Exception: If the request to create the project fails, an exception is raised
                   with the HTTP status code and error details.

    Returns:
        None: The function does not return any value. If the project is created
              successfully, it completes without errors.

    Example:
        config = ConfigHandler()  # Assume this is initialized with necessary details
        createProject(config, "MyProject")
    """
    headers = connection_get_headers(config)
    ENDPOINT_URL = config.config_get_nemo_url() + ENDPOINT_URL_PROJECTS_CREATE
    table_name = re.sub(r"[^A-Z0-9_]", "_", projectname.upper()).strip()
    if not table_name.startswith("PROJECT_"):
        table_name = "PROJECT_" + table_name

    data = {
        "autoDataRefresh": True,
        "displayName": projectname,
        "description": description,
        "type": "IndividualData",
        "status": "Active",
        "tableName": table_name,
        "importErrorType": "NoError",
        "id": "",
        "s3DataSourcePath": "",
        "showInitialConfiguration": True,
        "tenant": config.config_get_tenant(),
        "type": "0",
    }

    response = requests.post(ENDPOINT_URL, headers=headers, json=data)

    if response.status_code != 201:
        raise Exception(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )


def createImportedColumn(
    config: ConfigHandler,
    projectname: str,
    displayName: str,
    dataType: str,
    importName: str = None,
    internalName: str = None,
    description: str = None,
) -> None:
    """
    Creates an imported column in the specified project within the system.

    This function constructs a new imported column using provided metadata
    and posts it to the appropriate endpoint for persistence. If `importName`
    or `internalName` is not provided, it generates them based on the `displayName`.

    Args:
        config (ConfigHandler): Configuration handler containing system-specific details.
        projectname (str): The name of the project where the column will be created.
        displayName (str): The display name of the column.
        dataType (str): The data type of the column (e.g., "string", "integer").
        importName (str, optional): The import name for the column. Defaults to a sanitized version of `displayName`.
        internalName (str, optional): The internal name for the column. Defaults to a sanitized version of `displayName`.
        description (str, optional): A brief description of the column's purpose or content.

    Raises:
        Exception: If the HTTP request to create the column fails, an exception is raised with status code and error details.

    Returns:
        None: The function does not return a value; it creates the column via a POST request.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    if not importName:
        importName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()
    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()

    data = {
        "categorialType": True,
        "columnType": "ExportedColumn",
        "containsSensitiveData": False,
        "dataType": dataType,
        "description": description,
        "displayName": displayName,
        "importName": importName,
        "internalName": internalName,
        "id": "",
        "unit": "",
        "tenant": config.config_get_tenant(),
        "projectId": project_id,
    }

    response = requests.post(
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
        headers=headers,
        json=data,
    )
    if response.status_code != 201:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
