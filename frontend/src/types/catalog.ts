export type CatalogParamType =
  | "VEHICLE_MODEL"
  | "COLOR"
  | "WARRANTY_TYPE"
  | "CAMPAIGN_CODE";

export const CATALOG_PARAM_LABELS: Record<CatalogParamType, string> = {
  VEHICLE_MODEL: "Modelos de Vehículo",
  COLOR:         "Colores",
  WARRANTY_TYPE: "Tipos de Garantía",
  CAMPAIGN_CODE: "Códigos de Campaña",
};

export interface CatalogParam {
  id:           string;
  param_type:   string;
  code:         string;
  name:         string;
  concesionaria: string;
}

export interface SparePart {
  id:           string;
  catalog_code: string;
  name:         string;
  unit_price:   string;
  concesionaria: string;
}
