from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import yaml
import os
from pathlib import Path

@dataclass
class FieldSettings:
    name: str
    field_type: str
    required: bool = False
    choices: Optional[List[str]] = None
    description: Optional[str] = None
    is_metadata: bool = False

@dataclass
class DatasetSettings:
    name: str
    fields: List[FieldSettings]
    guidelines: Optional[str] = None
    allow_extra_metadata: bool = True
    metadata_schema: Dict[str, Any] = field(default_factory=dict)

class SettingsManager:
    def __init__(self, settings_dir: str = "dataset_configs"):
        self.settings_dir = Path(settings_dir)
        self.settings_dir.mkdir(exist_ok=True)

    def create_settings(self, settings: DatasetSettings) -> Dict[str, Any]:
        """
        Convert DatasetSettings to Argilla-compatible settings dictionary.
        """
        field_definitions = {}
        for field in settings.fields:
            field_def = {
                "type": field.field_type,
                "required": field.required
            }
            if field.choices:
                field_def["choices"] = field.choices
            if field.description:
                field_def["description"] = field.description
            
            if field.is_metadata:
                settings.metadata_schema[field.name] = field_def
            else:
                field_definitions[field.name] = field_def

        return {
            "fields": field_definitions,
            "metadata_schema": settings.metadata_schema,
            "guidelines": settings.guidelines,
        }

    def save_settings(self, settings: DatasetSettings, filename: str) -> str:
        """
        Save dataset settings to a YAML file.
        """
        filepath = self.settings_dir / f"{filename}.yaml"
        
        # Convert to dictionary format
        settings_dict = {
            "name": settings.name,
            "fields": [vars(f) for f in settings.fields],
            "guidelines": settings.guidelines,
            "allow_extra_metadata": settings.allow_extra_metadata,
            "metadata_schema": settings.metadata_schema
        }
        
        with open(filepath, 'w') as f:
            yaml.dump(settings_dict, f)
        
        return str(filepath)

    def load_settings(self, filename: str) -> DatasetSettings:
        """
        Load dataset settings from a YAML file.
        """
        filepath = self.settings_dir / f"{filename}.yaml"
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        fields = [
            FieldSettings(**field_data)
            for field_data in data["fields"]
        ]
        
        return DatasetSettings(
            name=data["name"],
            fields=fields,
            guidelines=data.get("guidelines"),
            allow_extra_metadata=data.get("allow_extra_metadata", True),
            metadata_schema=data.get("metadata_schema", {})
        )

    def list_available_settings(self) -> List[str]:
        """
        List all available settings configurations.
        """
        return [
            f.stem for f in self.settings_dir.glob("*.yaml")
        ]

# Example settings templates
def create_qa_dataset_settings(
    name: str,
    include_context: bool = True,
    include_keywords: bool = True
) -> DatasetSettings:
    """
    Create settings for a Q&A dataset with common fields.
    """
    fields = [
        FieldSettings(
            name="prompt",
            field_type="text",
            required=True,
            description="The question or prompt"
        ),
        FieldSettings(
            name="response",
            field_type="text",
            required=True,
            description="The answer or response"
        )
    ]
    
    if include_context:
        fields.append(
            FieldSettings(
                name="context",
                field_type="text",
                required=False,
                description="Additional context for the Q&A pair"
            )
        )
    
    if include_keywords:
        fields.append(
            FieldSettings(
                name="keywords",
                field_type="text",
                required=False,
                description="Keywords or tags"
            )
        )
    
    # Add metadata fields
    metadata_fields = [
        FieldSettings(
            name="source",
            field_type="string",
            required=False,
            is_metadata=True,
            description="Source of the Q&A pair"
        ),
        FieldSettings(
            name="date",
            field_type="string",
            required=False,
            is_metadata=True,
            description="Date of creation"
        )
    ]
    
    return DatasetSettings(
        name=name,
        fields=fields + metadata_fields,
        guidelines="Dataset for Q&A pairs with optional context and keywords"
    ) 