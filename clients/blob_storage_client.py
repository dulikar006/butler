import os
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import BytesIO

class BLBStorage:

    def __init__(self):
        self.account_name = os.environ['BlobStorageAccountName']
        self.account_key = os.environ['BlobStorageAccountKey']
        self.connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"
        self.container_name = "raw"

    def get_container_client(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(self.container_name)
        return container_client

    def upload_file(self, file_path, blob_name=None):
        """
        Uploads a file to Azure Blob Storage. Automatically detects file type by extension.
        :param file_path: Local path of the file to be uploaded.
        :param blob_name: (Optional) Name of the blob to be created in the container.
        """
        container_client = self.get_container_client()
        _, file_extension = os.path.splitext(file_path)

        if blob_name is None:
            blob_name = os.path.basename(file_path)

        # Get a BlobClient object
        blob_client = container_client.get_blob_client(blob_name)

        if file_extension in ['.csv', '.xlsx']:
            # Handle file as DataFrame
            if file_extension == '.csv':
                df = pd.read_csv(file_path)
                output = BytesIO()
                df.to_csv(output, index=False)
                blob_client.upload_blob(output.getvalue(), overwrite=True)
            elif file_extension == '.xlsx':
                df = pd.read_excel(file_path, engine='openpyxl')
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                blob_client.upload_blob(output.getvalue(), overwrite=True)
        else:
            # Handle binary files (e.g., images, PDFs)
            with open(file_path, "rb") as file:
                blob_client.upload_blob(file, overwrite=True)

    def download_file(self, blob_name, download_path):
        """
        Downloads a file from Azure Blob Storage and automatically saves it based on file type.
        :param blob_name: Name of the blob to be downloaded.
        :param download_path: Local path where the file will be saved.
        """
        container_client = self.get_container_client()
        _, file_extension = os.path.splitext(download_path)

        # Get a BlobClient object
        blob_client = container_client.get_blob_client(blob_name)

        # Download the file
        download_stream = blob_client.download_blob()

        if file_extension in ['.csv', '.xlsx']:
            # Handle DataFrame files
            if file_extension == '.csv':
                df = pd.read_csv(BytesIO(download_stream.readall()))
                df.to_csv(download_path, index=False)
            elif file_extension == '.xlsx':
                df = pd.read_excel(BytesIO(download_stream.readall()), engine='openpyxl')
                df.to_excel(download_path, index=False)
        else:
            # Handle binary files
            with open(download_path, "wb") as file:
                file.write(download_stream.readall())

    def upload_dataframe(self, df, blob_name):
        """
        Uploads a pandas DataFrame to Azure Blob Storage as CSV or Excel, determined by the blob name extension.
        :param df: DataFrame to be uploaded.
        :param blob_name: Name of the blob to be created, with file extension to determine format.
        """
        container_client = self.get_container_client()
        _, file_extension = os.path.splitext(blob_name)

        # Get a BlobClient object
        blob_client = container_client.get_blob_client(blob_name)

        # Convert DataFrame based on file extension
        if file_extension == '.csv':
            output = BytesIO()
            df.to_csv(output, index=False)
            blob_client.upload_blob(output.getvalue(), overwrite=True)
        elif file_extension == '.xlsx':
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            blob_client.upload_blob(output.getvalue(), overwrite=True)
        else:
            raise ValueError(f"Unsupported file extension for DataFrame: {file_extension}")

    def download_dataframe(self, blob_name):
        """
        Downloads a blob from Azure Blob Storage and returns it as a pandas DataFrame.
        Automatically detects format from file extension.
        :param blob_name: Name of the blob to be downloaded.
        :return: DataFrame loaded from the blob.
        """
        container_client = self.get_container_client()
        _, file_extension = os.path.splitext(blob_name)

        # Get a BlobClient object
        blob_client = container_client.get_blob_client(blob_name)

        # Download the file
        download_stream = blob_client.download_blob()

        # Load the blob as a DataFrame
        if file_extension == '.csv':
            return pd.read_csv(BytesIO(download_stream.readall()))
        elif file_extension == '.xlsx':
            return pd.read_excel(BytesIO(download_stream.readall()), engine='openpyxl')
        else:
            raise ValueError(f"Unsupported file extension for DataFrame: {file_extension}")
