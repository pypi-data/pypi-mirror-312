import json
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator

from moonai.missions.output_format import OutputFormat


class MissionOutput(BaseModel):
    """Class that represents the result of a mission."""

    description: str = Field(description="Description of the mission")
    name: Optional[str] = Field(description="Name of the mission", default=None)
    expected_output: Optional[str] = Field(
        description="Expected output of the mission", default=None
    )
    summary: Optional[str] = Field(description="Summary of the mission", default=None)
    raw: str = Field(description="Raw output of the mission", default="")
    pydantic: Optional[BaseModel] = Field(
        description="Pydantic output of mission", default=None
    )
    json_dict: Optional[Dict[str, Any]] = Field(
        description="JSON dictionary of mission", default=None
    )
    agent: str = Field(description="Agent that executed the mission")
    output_format: OutputFormat = Field(
        description="Output format of the mission", default=OutputFormat.RAW
    )

    @model_validator(mode="after")
    def set_summary(self):
        """Set the summary field based on the description."""
        excerpt = " ".join(self.description.split(" ")[:10])
        self.summary = f"{excerpt}..."
        return self

    @property
    def json(self) -> Optional[str]:
        if self.output_format != OutputFormat.JSON:
            raise ValueError(
                """
                Invalid output format requested.
                If you would like to access the JSON output,
                please make sure to set the output_json property for the mission
                """
            )

        return json.dumps(self.json_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert json_output and pydantic_output to a dictionary."""
        output_dict = {}
        if self.json_dict:
            output_dict.update(self.json_dict)
        elif self.pydantic:
            output_dict.update(self.pydantic.model_dump())
        return output_dict

    def __str__(self) -> str:
        if self.pydantic:
            return str(self.pydantic)
        if self.json_dict:
            return str(self.json_dict)
        return self.raw
