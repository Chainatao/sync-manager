# Standard Property Schema for Sync Manager
# Based on your existing property.py model

from pydantic import BaseModel, HttpUrl, Field, field_validator, model_validator
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime


# ========================================
# DEVELOPER & DEVELOPMENT MODELS
# ========================================

class DeveloperBase(BaseModel):
    """Base model for real estate developers"""
    name: str = Field(..., description="Developer company name")
    description: Optional[str] = Field(None, description="Developer description")
    website: Optional[HttpUrl] = Field(None, description="Developer website")
    logo_url: Optional[HttpUrl] = Field(None, description="Developer logo URL")
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    
    # Additional metadata
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional developer data")


class DevelopmentBase(BaseModel):
    """Base model for real estate developments/projects"""
    name: str = Field(..., description="Development/Project name")
    developer_id: Optional[int] = Field(None, description="FK to developer (optional)")
    
    description: Optional[str] = Field(None, description="Development description")
    location: Optional[str] = Field(None, description="Development location")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State/Province")
    country: Optional[str] = Field(None, description="Country")
    
    # Development details
    total_units: Optional[int] = Field(None, ge=0, description="Total number of units")
    available_units: Optional[int] = Field(None, ge=0, description="Available units")
    completion_date: Optional[datetime] = Field(None, description="Expected completion date")
    
    # Media
    images: Optional[List[HttpUrl]] = Field(default_factory=list, description="Development images")
    website: Optional[HttpUrl] = Field(None, description="Development website")
    
    # Additional metadata
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional development data")


class PoolType(str, Enum):
    communal = "communal"
    private = "private"
    undefined = "undefined"


class Orientation(str, Enum):
    north = "o-n"
    northeast = "o-ne"
    east = "o-e"
    southeast = "o-se"
    south = "o-s"
    southwest = "o-so"
    west = "o-o"
    northwest = "o-no"


class PropertyFeature(str, Enum):
    # --- Estado / Status ---
    alquilado = "alquilado"
    reservado = "reservado"

    # --- Equipamiento / Interior ---
    aire_acondicionado = "aire_acondicionado"
    amueblado = "amueblado"
    sin_amueblar = "sin_amueblar"
    cocina_amueblada = "cocina_amueblada"
    barbacoa = "barbacoa"
    balcon = "balcon"
    calefaccion = "calefaccion"
    calefaccion_central = "calefaccion_central"
    chimenea = "chimenea"
    terraza = "terraza"
    ascensor = "ascensor"
    electrodomesticos = "electrodomesticos"
    aerotermia = "aerotermia"
    domotica = "domotica"
    escaparate = "escaparate"
    jardin = "jardin"
    lavadero = "lavadero"
    parquet = "parquet"
    piscina = "piscina"
    pista_padel = "pista_padel"
    pista_tenis = "pista_tenis"
    porche = "porche"
    portero_automatico = "portero_automatico"
    preinstalacion_aire_acondicionado = "preinstalacion_aire_acondicionado"
    puerta_blindada = "puerta_blindada"
    salida_humos = "salida_humos"
    solarium = "solarium"
    sotano = "sotano"
    gimnasio = "gimnasio"
    parque_infantil = "parque_infantil"
    zonas_verdes_comunes = "zonas_verdes_comunes"
    garaje_aparcamiento = "garaje_aparcamiento"
    trastero = "trastero"
    cerca_tiendas = "cerca_tiendas"
    jacuzzi = "jacuzzi"
    suelo_radiante_banos = "suelo_radiante_banos"
    calefaccion_suelo_radiante = "calefaccion_suelo_radiante"
    alarma = "alarma"
    reformado = "reformado"

    # --- Ubicación / Location ---
    campo = "campo"
    cerca_playa = "cerca_playa"
    cerca_golf = "cerca_golf"
    urbano = "urbano"
    off_plan = "off_plan"
    precio_reducido = "precio_reducido"
    primera_linea = "primera_linea"

    # --- Vistas / Views ---
    vistas_montana = "vistas_montana"
    vistas_piscina = "vistas_piscina"
    vistas_abiertas = "vistas_abiertas"
    vistas_jardin = "vistas_jardin"
    vistas_mar = "vistas_mar"
    vistas_ciudad = "vistas_ciudad"
    vistas_salinas = "vistas_salinas"
    vistas_campo_golf = "vistas_campo_golf"


FEATURE_LABELS_ES = {
    "aire_acondicionado": "Aire acondicionado",
    "amueblado": "Amueblado",
    "sin_amueblar": "Sin amueblar",
    "cocina_amueblada": "Cocina amueblada",
    "barbacoa": "Barbacoa",
    "balcon": "Balcón",
    "calefaccion": "Calefacción",
    "calefaccion_central": "Calefacción central",
    "chimenea": "Chimenea",
    "terraza": "Terraza",
    "ascensor": "Ascensor",
    "electrodomesticos": "Electrodomésticos",
    "aerotermia": "Aerotermia",
    "domotica": "Domótica",
    "escaparate": "Escaparate",
    "jardin": "Jardín",
    "lavadero": "Lavadero",
    "parquet": "Parquet",
    "piscina": "Piscina",
    "pista_padel": "Pista de pádel",
    "pista_tenis": "Pista de tenis",
    "porche": "Porche",
    "portero_automatico": "Portero automático",
    "preinstalacion_aire_acondicionado": "Preinstalación aire acondicionado",
    "puerta_blindada": "Puerta blindada",
    "salida_humos": "Salida de humos",
    "solarium": "Solárium",
    "sotano": "Sótano",
    "gimnasio": "Gimnasio",
    "parque_infantil": "Parque infantil",
    "zonas_verdes_comunes": "Zonas verdes comunes",
    "garaje_aparcamiento": "Garaje / Aparcamiento",
    "trastero": "Trastero",
    "cerca_tiendas": "Cerca de tiendas",
    "jacuzzi": "Jacuzzi",
    "vistas_montana": "Vistas a la montaña",
    "vistas_salinas": "Vistas a las salinas",
    "vistas_campo_golf": "Vistas al campo de golf",
    "suelo_radiante_banos": "Suelo radiante en baños",
    "calefaccion_suelo_radiante": "Calefacción por suelo radiante",
    "alarma": "Alarma",
    "reformado": "Reformado",
    "campo": "Campo",
    "cerca_playa": "Cerca de la playa",
    "cerca_golf": "Cerca del Golf",
    "off_plan": "Off-plan",
    "precio_reducido": "Precio reducido",
    "primera_linea": "Primera línea",
    "urbano": "Urbano",
    "vistas_piscina": "Vistas a la piscina",
    "vistas_abiertas": "Vistas abiertas",
    "vistas_jardin": "Vistas al jardín",
    "vistas_mar": "Vistas al mar",
    "vistas_ciudad": "Vistas de la ciudad"
}

PROPERTY_TYPE_MAPPING = {
    "apartments": "Apartamento",
    "commercial real estate": "Commercial",
    "finca": "Villa",
    "house": "Villa",
    "land plot": "Parcela",
    "penthouse": "Ático",
    "townhouse": "Duplex",
    "villa": "Villa",
    "villa, vinca": "Villa",
    "villa, house": "Villa",
    "apartamento": "Apartamento",
    "duplex": "Duplex",
    "parcela": "Parcela",
    "villa, finca": "Villa",
}


class MultilingualText(BaseModel):
    """Multilingual text support"""
    en: Optional[str] = Field(None, description="English text")
    es: Optional[str] = Field(None, description="Spanish text")
    pl: Optional[str] = Field(None, description="Polish text")
    uk: Optional[str] = Field(None, description="Ukrainian text")
    ru: Optional[str] = Field(None, description="Russian text")

    @model_validator(mode="after")
    def ensure_some_translation(self):
        if not any([self.en, self.es, self.pl, self.uk, self.ru]):
            raise ValueError("At least one language version must be provided.")
        return self


class StandardProperty(BaseModel):
    """
    Standard Property Schema for Sync Manager
    
    This is the canonical format used internally. All sources transform
    their data to this format, and all targets read from this format.
    
    Based on your existing property.py model with extensions for:
    - Developer/Development relational references
    - Source/Target tracking
    - Sync management fields
    """
    
    # ========================================
    # IDENTIFIERS & REFERENCES
    # ========================================
    
    # External ID (REQUIRED - from source)
    external_id: str = Field(..., description="Unique ID from source system")
    
    # Internal references
    id: Optional[str] = Field(None, description="Sync Manager internal ID")
    target_reference: Optional[str] = Field(None, description="Target website's reference")
    source_reference: Optional[str] = Field(None, description="Source reference")
    
    # RELATIONAL: Developer & Development (Foreign Keys to other tables)
    developer_id: Optional[int] = Field(None, description="FK to developers table (optional)")
    development_id: Optional[int] = Field(None, description="FK to developments table (optional)")
    
    # Legacy fields (for backward compatibility when no relational data)
    developer_name: Optional[str] = Field(None, description="Developer name (legacy, use developer_id)")
    development_name: Optional[str] = Field(None, description="Development name (legacy, use development_id)")
    
    # ========================================
    # BASIC INFORMATION
    # ========================================
    
    title: MultilingualText = Field(..., description="Title in multiple languages")
    description: Optional[MultilingualText] = Field(None, description="Description in multiple languages")
    property_type: Optional[str] = Field(None, description="Normalized property type")
    operation: Optional[str] = Field(None, description="Sale, Rent, Temporary rent, New build, Resale")
    
    # ========================================
    # PRICING
    # ========================================
    
    price: Optional[int] = Field(None, gt=0, description="Price in local currency")
    currency: Optional[str] = Field(None, description="Currency code, e.g. USD, EUR, MXN")
    
    # ========================================
    # PROPERTY DETAILS
    # ========================================
    
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    
    # Areas (in square meters)
    constr_area_m2: Optional[int] = Field(None, gt=0, description="Total constructed area in m²")
    util_area_m2: Optional[int] = Field(None, gt=0, description="Usable area in m²")
    plot_area_m2: Optional[int] = Field(None, gt=0, description="Plot area in m²")
    garden_area_m2: Optional[int] = Field(None, gt=0, description="Garden area in m²")
    terrace_area_m2: Optional[int] = Field(None, gt=0, description="Terrace area in m²")
    solarium_area_m2: Optional[int] = Field(None, gt=0, description="Solarium area in m²")
    
    # Building info
    year_built: Optional[int] = Field(None, ge=0)
    delivery_date: Optional[datetime] = Field(None, description="Expected delivery date")
    
    # Additional details
    pools: Optional[List[PoolType]] = Field(
        default=None,
        description="List of pool types (communal, private, undefined)"
    )
    parking_spaces: Optional[int] = Field(None, ge=0)
    floor_number: Optional[int] = Field(None, ge=0)
    orientation: Optional[Orientation] = Field(
        default=None,
        description="Property orientation (e.g. north, southeast)"
    )
    
    # Energy certificates
    energy_certificate: Optional[str] = Field(None, description="Energy certificate rating")
    emission_certificate: Optional[str] = Field(None, description="Emission certificate rating")
    
    # Features
    features: Optional[List[PropertyFeature]] = Field(
        default_factory=list,
        description="List of property features"
    )
    
    # ========================================
    # LOCATION
    # ========================================
    
    location: Optional[str] = Field(None, description="Full location string for geocoding")
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # ========================================
    # MEDIA
    # ========================================
    
    images: Optional[List[HttpUrl]] = Field(default_factory=list, description="Property images")
    plans: Optional[List[HttpUrl]] = Field(default_factory=list, description="Floor plans")
    
    # ========================================
    # URLS & SOURCE INFO
    # ========================================
    
    url_source: Optional[HttpUrl] = Field(None, description="URL of property on source website")
    url_target: Optional[HttpUrl] = Field(None, description="URL of property on target website")
    preview_url: Optional[HttpUrl] = Field(None, description="Preview URL for unpublished property")
    source_name: Optional[str] = Field(None, description="Name of the source (e.g., 'ym_website')")
    
    # ========================================
    # STATUS FLAGS
    # ========================================
    
    is_activated: bool = Field(default=False, description="Is property activated?")
    is_hidden: bool = Field(default=False, description="Is property hidden?")
    is_sold: bool = Field(default=False, description="Is property sold?")
    is_featured: bool = Field(default=False, description="Is property featured?")
    
    # ========================================
    # TIMESTAMPS
    # ========================================
    
    created_at: Optional[datetime] = Field(
        default=None,
        description="When property was created"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="When property was last updated"
    )
    
    # ========================================
    # SYNC METADATA (Added for Sync Manager)
    # ========================================
    
    sync_metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional sync-related metadata"
    )
    
    # ========================================
    # VALIDATORS
    # ========================================
    
    @field_validator("currency")
    @classmethod
    def upper_currency(cls, v):
        if v:
            return v.upper()
        return v
    
    @field_validator("operation")
    @classmethod
    def normalize_operation(cls, v):
        if not v:
            return v
        v = v.lower()
        if "obra nueva" in v or "new build" in v or "new built" in v:
            return "new_build"
        elif "reventa" in v or "resale" in v:
            return "resale"
        return v
    
    @field_validator("property_type")
    @classmethod
    def normalize_property_type(cls, v):
        if not v:
            return None
        v_lower = v.lower().strip()
        if v_lower in PROPERTY_TYPE_MAPPING:
            return PROPERTY_TYPE_MAPPING[v_lower]
        return v
    
    @model_validator(mode="before")
    @classmethod
    def set_development_if_missing(cls, values):
        """Set development from source_reference if missing"""
        if isinstance(values, dict):
            development_name = values.get("development_name")
            development_id = values.get("development_id")
            source_ref = values.get("source_reference")
            
            # Only set development_name if no relational ID and no name
            if not development_id and not development_name and source_ref:
                values["development_name"] = source_ref
        
        return values
    
    @model_validator(mode="after")
    def ensure_minimum_data(self):
        """Ensure minimum required data exists"""
        # For sync manager, we're more lenient - just need external_id and title
        # Other validations can be added based on your needs
        return self
    
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "external_id": "PROP001",
                "title": {
                    "en": "Luxury Villa in Madrid",
                    "es": "Villa de Lujo en Madrid"
                },
                "property_type": "Villa",
                "operation": "sale",
                "price": 850000,
                "currency": "EUR",
                "bedrooms": 5,
                "bathrooms": 3,
                "constr_area_m2": 350,
                "plot_area_m2": 500,
                "city": "Madrid",
                "country": "Spain",
                "developer_id": 1,
                "development_id": 5,
                "images": [
                    "https://example.com/img1.jpg",
                    "https://example.com/img2.jpg"
                ],
                "features": ["piscina", "jardin", "aire_acondicionado"],
                "source_name": "ym_website"
            }
        }


# ========================================
# RELATIONAL MODELS (Optional - Future Use)
# ========================================

class Developer(BaseModel):
    """
    Developer entity (stored in separate developers table)
    Properties can reference this via developer_id
    """
    id: Optional[int] = Field(None, description="Developer ID")
    name: str = Field(..., description="Developer name")
    description: Optional[MultilingualText] = None
    website: Optional[HttpUrl] = None
    logo_url: Optional[HttpUrl] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    country: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Premium Developments SA",
                "website": "https://premiumdev.com",
                "country": "Spain"
            }
        }


class Development(BaseModel):
    """
    Development/Project entity (stored in separate developments table)
    Properties can reference this via development_id
    """
    id: Optional[int] = Field(None, description="Development ID")
    name: str = Field(..., description="Development name")
    developer_id: Optional[int] = Field(None, description="FK to developer")
    
    description: Optional[MultilingualText] = None
    
    # Location
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Development info
    total_units: Optional[int] = Field(None, ge=0)
    completion_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    
    # Media
    images: Optional[List[HttpUrl]] = Field(default_factory=list)
    master_plan_url: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    
    # Amenities
    amenities: Optional[List[str]] = Field(default_factory=list)
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 5,
                "name": "Sunset Gardens",
                "developer_id": 1,
                "city": "Marbella",
                "country": "Spain",
                "total_units": 120,
                "completion_date": "2025-06-01T00:00:00Z",
                "amenities": ["pool", "gym", "security_24h"]
            }
        }
