import { api } from "@/lib/api";
import type { Audit } from "@/types/audit";

export const auditService = {
  list:   ()         => api.get<Audit[]>("/audits/").then(r => r.data),
  get:    (id: string) => api.get<Audit>(`/audits/${id}/`).then(r => r.data),
  create: (data: unknown) => api.post<Audit>("/audits/", data).then(r => r.data),
  update: (id: string, data: unknown) => api.patch<Audit>(`/audits/${id}/`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/audits/${id}/`),
};
