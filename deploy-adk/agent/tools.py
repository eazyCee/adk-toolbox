import os
from google.adk.tools.toolbox_tool import ToolboxTool

TOOLBOX_URL = os.environ.get('TOOLBOX_URL')
toolbox_tools = ToolboxTool(TOOLBOX_URL)
toolset = toolbox_tools.get_toolset("my-toolset")
