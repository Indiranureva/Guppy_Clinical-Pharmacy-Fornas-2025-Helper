"""Domain models for pharmaceutical product profiles."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ActiveIngredient:
    name: str
    strength: float
    unit: str  # mg, g, IU, mcg, etc.
    cas_number: Optional[str] = None
    bcs_class: Optional[str] = None


@dataclass
class StabilityProfile:
    climatic_zone: str  # e.g., 'Zone IVb', 'Zone II'
    real_time_temp_rh: str  # e.g., '30°C/75% RH', '25°C/60% RH'
    real_time_months: int  # months completed
    accelerated_temp_rh: str  # e.g., '40°C/75% RH'
    accelerated_months: int  # months completed
    primary_packaging: str  # e.g., 'PVC/Alu Blister', 'HDPE Bottle', 'Amber Glass'
    significant_change_detected: bool = False


@dataclass
class ManufacturingProfile:
    manufacturer_name: str
    country_of_origin: str  # 'Indonesia' or foreign country
    gmp_certificate_valid: bool
    gmp_certificate_expiry: Optional[str] = None
    validation_batches_count: int = 3
    is_toll_manufacturing: bool = False


@dataclass
class ProductCase:
    product_name: str
    active_ingredients: List[ActiveIngredient]
    dosage_form: str  # e.g., 'Tablet Salut Selaput', 'Kapsul', 'Sirup', 'Injeksi'
    route_of_administration: str  # 'Oral', 'Topikal', 'Parenteral', etc.
    intended_indication: str
    stability: StabilityProfile
    manufacturing: ManufacturingProfile
    is_new_chemical_entity: bool = False
    is_generic_copy: bool = True
    comparator_product: Optional[str] = None
    barcode_2d_present: bool = True
    be_study_completed: bool = False
    biowaiver_claimed: bool = False
    biowaiver_dissolution_f2_valid: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
