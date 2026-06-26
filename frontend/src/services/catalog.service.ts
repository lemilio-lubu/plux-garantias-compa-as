import { api } from "@/lib/api";
import type { CatalogParam, SparePart } from "@/types/catalog";

export const catalogService = {
  // ── Params ──────────────────────────────────────────────────────────────
  getParams: (type: string, concesionaria?: string) =>
    api.get<CatalogParam[]>("/catalog/params/", { params: { type, concesionaria } }).then(r => r.data),

  createParam: (data: { param_type: string; code: string; name: string; concesionaria: string }) =>
    api.post<CatalogParam>("/catalog/params/", data).then(r => r.data),

  deleteParam: (id: string) => api.delete(`/catalog/params/${id}/`),

  // ── Spare parts ─────────────────────────────────────────────────────────
  getSpareParts: (concesionaria?: string) =>
    api.get<SparePart[]>("/catalog/spare-parts/", { params: { concesionaria } }).then(r => r.data),

  createSparePart: (data: { catalog_code: string; name: string; unit_price: number; concesionaria: string }) =>
    api.post<SparePart>("/catalog/spare-parts/", data).then(r => r.data),

  updateSparePart: (id: string, data: Partial<{ name: string; unit_price: number }>) =>
    api.patch<SparePart>(`/catalog/spare-parts/${id}/`, data).then(r => r.data),

  deleteSparePart: (id: string) => api.delete(`/catalog/spare-parts/${id}/`),
};
