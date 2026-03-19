import os
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FileDownloaderInput(BaseModel):
    """Input schema for FileDownloaderTool."""
    url: str = Field(..., description="The URL of the file to download.")
    filename: str = Field(..., description="The name of the file to save as (including extension).")

class FileDownloaderTool(BaseTool):
    name: str = "file_downloader"
    description: str = (
        "Useful for downloading images or videos from a URL and saving them to the local 'assets/' directory."
    )
    args_schema: Type[BaseModel] = FileDownloaderInput

    def _run(self, url: str, filename: str) -> str:
        # Absolute path as requested
        assets_dir = "/Users/phurikorn/Desktop/Research/hello_ai/assets"
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
        
        filepath = os.path.join(assets_dir, filename)
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return f"Successfully downloaded {filename} to {filepath}"
        except Exception as e:
            return f"Failed to download {url}. Error: {str(e)}"
