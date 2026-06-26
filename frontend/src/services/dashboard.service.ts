import { api } from "@/lib/api";

export interface StatusCount    { status: string; count: number; }
export interface TypeStatusCount { srg_type: string; status: string; count: number; }

export interface DashboardStats {
  concesionaria: string;
  total:         number;
  by_status:     StatusCount[];
  by_type:       Record<string, number>;
  breakdown:     TypeStatusCount[];
}

export const dashboardService = {
  get: (concesionaria?: string) =>
    api
      .get<DashboardStats>("/dashboard/", { params: concesionaria ? { concesionaria } : {} })
      .then(r => r.data),
};
