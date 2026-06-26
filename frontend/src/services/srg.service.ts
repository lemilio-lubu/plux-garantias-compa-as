import { api } from "@/lib/api";
import type {
  Srg,
  SrgPart,
  PartLedger,
  SrgEvent,
  CampaignBody,
  CatalogParam,
} from "@/types/srg";

// ── SRG ──────────────────────────────────────────────────────────────────

export interface SrgFilters {
  ot?:            string;
  vin?:           string;
  sede?:          string;
  concesionaria?: string;
}

export const srgService = {
  list:   (f?: SrgFilters)   => api.get<Srg[]>("/srgs/", { params: f }).then(r => r.data),
  get:    (id: string)       => api.get<Srg>(`/srgs/${id}/`).then(r => r.data),
  delete: (id: string)       => api.delete(`/srgs/${id}/`),

  createWarranty: (data: unknown) =>
    api.post<Srg>("/srgs/warranty/", data).then(r => r.data),

  createCampaign: (data: unknown) =>
    api.post<Srg>("/srgs/campaign/", data).then(r => r.data),

  update: (id: string, data: unknown) =>
    api.patch<Srg>(`/srgs/${id}/`, data).then(r => r.data),

  transition: (id: string, payload: { new_status: string; fecha_aprobacion?: string }) =>
    api.post<Srg>(`/srgs/${id}/transition/`, payload).then(r => r.data),

  // Parts ledger & movements
  getParts: (id: string) => api.get<PartLedger[]>(`/srgs/${id}/parts/`).then(r => r.data),
  addPart:  (id: string, data: unknown) => api.post<SrgPart>(`/srgs/${id}/parts/`, data).then(r => r.data),
  registerMovement: (id: string, partId: string, data: unknown) =>
    api.post<SrgEvent>(`/srgs/${id}/parts/${partId}/movements/`, data).then(r => r.data),

  // Traceability
  getEvents:      (id: string) => api.get<SrgEvent[]>(`/srgs/${id}/events/`).then(r => r.data),
  getGlobalEvents: (params?: { concesionaria?: string; event_type?: string }) =>
    api.get<SrgEvent[]>("/events/", { params }).then(r => r.data),

  // Campaign body
  getCampaignBody:    (id: string)              => api.get<CampaignBody>(`/srgs/${id}/campaign-body/`).then(r => r.data),
  upsertCampaignBody: (id: string, data: unknown) => api.post<CampaignBody>(`/srgs/${id}/campaign-body/`, data).then(r => r.data),
};

// ── Catalog ────────────────────────────────────────────────────────────────

export const catalogService = {
  getParams: (type: string, concesionaria?: string) =>
    api.get<CatalogParam[]>("/catalog/params/", { params: { type, concesionaria } }).then(r => r.data),
};
