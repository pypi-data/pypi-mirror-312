# NexusflowAI Python API library

[![PyPI version](https://img.shields.io/pypi/v/nexusflowai?pypiBaseUrl=https://pypi.org)](https://pypi.org/project/nexusflowai/)

Welcome to the NexusflowAI API by [Nexusflow.ai](https://nexusflow.ai/)!

```bash
pip install nexusflowai
```

This package is based on and extends from the [OpenAI Python Library](https://github.com/openai/openai-python). Cheers to the OpenAI team for an amazing API library and SDK!


# Usage
## Completions
```python
from nexusflowai import NexusflowAI


nf = NexusflowAI(api_key="<api key>")


response = nf.completions.create(
    model="nexus-tool-use-20240816",
    prompt="""Function:
def get_weather(city_name: str):
\"\"\"
\"\"\"


User Query: i am in berkeley.<human_end>Call:""",
    stop=["<bot_end>"],
    max_tokens=10,
)
print(response)
```

## ChatCompletions with Tools
```python
from nexusflowai import NexusflowAI


nf = NexusflowAI(api_key="<api key>")


response = nf.chat.completions.create(
    model="nexus-tool-use-20240816",
    messages=[
        {
            "role": "user",
            "content": "i am in berkeley.",
        },
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "",
                        },
                    },
                    "required": ["city_name"],
                    "additionalProperties": False,
                }
            }
        }
    ],
)
print(response)
```


## ChatCompletions with Structured Outputs
```python
from typing import List, Dict, Tuple

from pydantic import BaseModel, Field

from nexusflowai import NexusflowAI


nf = NexusflowAI(api_key="<api key>")


class GasDistributionNetwork(BaseModel):
    networkID: str = Field(
        ...,
        description="The identifier for the gas distribution network.",
        title="Network ID",
    )
    pipelineValues: Dict[str, Tuple[int, int]] = Field(
        description="The mapping with key pipeline_1, pipeline_2, etc ... to tuple of (total length in kilometers, maximum amount of gas that can be distributed in cubic meters).",
        title="Pipeline Values",
    )
    maintenanceSchedules: List[str] = Field(
        ...,
        description="The schedule detailing when maintenance activities are to be performed.",
        title="Maintenance Schedule",
    )


response = nf.chat.completions.create(
    model="nexus-tool-use-20240816",
    messages=[
        {
            "role": "user",
            "content": """I am currently working on a project that involves mapping out a gas distribution network for a new residential area. The network is quite extensive and includes several pipelines that distribute natural gas to various sectors of the community. I need to create a JSON object that captures the essential details of this network. The information I have includes a unique identifier for the network, which is 'GDN-4521'. The total length of the pipeline_1 is 275 kilometers with a capacity 500,000 cubic meters. Pipeline 2 is 17 kilometers long and has a capacity of 12,000 cubic meters. Additionally, there is a detailed maintenance schedule, which includes quarterly inspections in January, April, July, and October.""",
        },
    ],
    response_format=GasDistributionNetwork,
)
print(response.raw_prompt)
print(response.choices[0].message.parsed)
```
