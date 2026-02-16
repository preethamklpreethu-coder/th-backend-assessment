"""Pydantic models for email extraction output."""

from typing import Optional

from pydantic import BaseModel, Field


class ExtractedShipment(BaseModel):
    """Structured extraction result for one email."""

    id: str = Field(..., description="Email ID from input")
    product_line: Optional[str] = Field(None, description="pl_sea_import_lcl or pl_sea_export_lcl")
    origin_port_code: Optional[str] = Field(None, description="5-letter UN/LOCODE")
    origin_port_name: Optional[str] = Field(None, description="Canonical port name from reference")
    destination_port_code: Optional[str] = Field(None, description="5-letter UN/LOCODE")
    destination_port_name: Optional[str] = Field(None, description="Canonical port name from reference")
    incoterm: Optional[str] = Field(None, description="FOB, CIF, CFR, etc.")
    cargo_weight_kg: Optional[float] = Field(None, description="Weight in kg, 2 decimal places")
    cargo_cbm: Optional[float] = Field(None, description="Volume in CBM, 2 decimal places")
    is_dangerous: bool = Field(False, description="True if DG/hazardous cargo")
