export type SrgType   = "WARRANTY" | "CAMPAIGN";
export type SrgStatus = "PROCESO" | "PENDIENTE" | "PREAPROBADO" | "APROBADO" | "RETORNADO" | "NEGADO";

export interface Srg {
  id:             string;
  ot:             string;
  srg_type:       SrgType;
  status:         SrgStatus;
  concesionaria:  string;
  asesor_id:      string;
  vin:            string;
  placa:          string;
  vehicle_model:  string;
  vehicle_color:  string;
  vehicle_year:   number;
  km_apertura:    number;
  sede:           string;
  // Warranty
  nro_garantia?:      string | null;
  warranty_type_code?: string | null;
  warranty_type_name?: string | null;
  // Campaign
  campaign_code?:      string | null;
  // Dates
  fecha_envio_marca?:  string | null;
  fecha_aprobacion?:   string | null;
  created_at:          string;
}

export interface SrgPart {
  id:             string;
  catalog_code:   string;
  name_es:        string;
  quantity:       number;
  unit_price:     string;
  part_origin:    string;
  invoice_number: string;
  created_at:     string;
}

export type ReceptionState = "PENDIENTE" | "PARCIAL" | "COMPLETA";
export type ReturnState    = "NO_APLICA" | "PENDIENTE" | "PARCIAL" | "COMPLETA";
export type SrgEventType =
  | "PART_REQUESTED"
  | "RECEPTION_REGISTERED"
  | "WORK_REGISTERED"
  | "CORE_RETURN_DECLARED"
  | "RETURN_CONFIRMED"
  | "STATUS_CHANGED";

export type MovementType = Exclude<SrgEventType, "PART_REQUESTED" | "STATUS_CHANGED">;

export interface PartLedger {
  id:                 string;
  catalog_code:       string;
  name_es:            string;
  unit_price:         string;
  part_origin:        string;
  invoice_number:     string;
  created_at:         string;
  requested:          number;
  received:           number;
  used:               number;
  returned_declared:  number;
  returned_confirmed: number;
  pending_reception:  number;
  pending_return:     number;
  reception_state:    ReceptionState;
  return_state:       ReturnState;
  closed:             boolean;
}

export interface SrgEvent {
  id:          string;
  srg_id:      string;
  srg_part_id: string | null;
  actor_id:    string | null;
  actor_role:  string;
  actor_label: string;
  part_label:  string;
  event_type:  SrgEventType;
  quantity:    number | null;
  state_from:  string;
  state_to:    string;
  note:        string;
  location:    string;
  created_at:  string;
}

export interface CampaignBody {
  id:          string;
  srg_id:      string;
  update_name: string;
  image_link:  string;
  modified_by: string;
  updated_at:  string;
}

export interface CatalogParam {
  id:           string;
  param_type:   string;
  code:         string;
  name:         string;
  concesionaria: string;
}

// ── Status transition helpers ──────────────────────────────────────────────
export const STATUS_LABELS: Record<SrgStatus, string> = {
  PROCESO:     "Proceso",
  PENDIENTE:   "Pendiente",
  PREAPROBADO: "Preaprobado",
  APROBADO:    "Aprobado",
  RETORNADO:   "Retornado",
  NEGADO:      "Negado",
};

export const SRG_TYPE_LABELS: Record<SrgType, string> = {
  WARRANTY: "Garantía",
  CAMPAIGN: "Campaña",
};
