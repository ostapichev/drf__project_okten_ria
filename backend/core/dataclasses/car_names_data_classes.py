from dataclasses import dataclass


@dataclass
class BrandCarDataClass:
    id: int
    brand_name: str


@dataclass
class ModelCarDataClass:
    id: int
    model_name: str
    brand: BrandCarDataClass
