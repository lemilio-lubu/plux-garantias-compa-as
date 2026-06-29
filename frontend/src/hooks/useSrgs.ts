import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { srgService, type SrgFilters } from "@/services/srg.service";
import { catalogService } from "@/services/catalog.service";

const KEYS = {
  all:      ["srgs"] as const,
  list:     (f?: SrgFilters) => ["srgs", "list", f] as const,
  detail:   (id: string)     => ["srgs", "detail", id] as const,
  parts:    (id: string)     => ["srgs", "parts", id] as const,
  events:   (id: string)     => ["srgs", "events", id] as const,
  globalEvents: (p?: object) => ["events", p] as const,
  body:     (id: string)     => ["srgs", "campaign-body", id] as const,
  catalog:  (type: string, c?: string) => ["catalog", type, c] as const,
};

export function useSrgs(filters?: SrgFilters) {
  return useQuery({ queryKey: KEYS.list(filters), queryFn: () => srgService.list(filters) });
}

// Live options for collaborative views: poll every 5s and treat as always
// stale so other users' changes (receptions, status, events) show up without
// a manual refresh. Polling pauses automatically while the tab is hidden.
const LIVE = { refetchInterval: 5000, staleTime: 0 } as const;

export function useSrg(id: string) {
  return useQuery({ queryKey: KEYS.detail(id), queryFn: () => srgService.get(id), enabled: !!id, ...LIVE });
}

export function useCreateWarrantySrg() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => srgService.createWarranty(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useCreateCampaignSrg() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => srgService.createCampaign(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useTransitionStatus(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: { new_status: string; fecha_aprobacion?: string }) =>
      srgService.transition(id, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.detail(id) });
      qc.invalidateQueries({ queryKey: KEYS.all });
    },
  });
}

export function useDeleteSrg() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => srgService.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useSrgParts(srgId: string) {
  return useQuery({ queryKey: KEYS.parts(srgId), queryFn: () => srgService.getParts(srgId), enabled: !!srgId, ...LIVE });
}

export function useAddPart(srgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => srgService.addPart(srgId, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.parts(srgId) });
      qc.invalidateQueries({ queryKey: KEYS.events(srgId) });
    },
  });
}

export function useRegisterMovement(srgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ partId, ...data }: { partId: string; event_type: string; quantity: number; note?: string; location?: string }) =>
      srgService.registerMovement(srgId, partId, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.parts(srgId) });
      qc.invalidateQueries({ queryKey: KEYS.events(srgId) });
    },
  });
}

export function useSrgEvents(srgId: string) {
  return useQuery({ queryKey: KEYS.events(srgId), queryFn: () => srgService.getEvents(srgId), enabled: !!srgId, ...LIVE });
}

export function useGlobalEvents(params?: { concesionaria?: string; event_type?: string }) {
  return useQuery({ queryKey: KEYS.globalEvents(params), queryFn: () => srgService.getGlobalEvents(params), ...LIVE });
}

export function useCampaignBody(srgId: string) {
  return useQuery({ queryKey: KEYS.body(srgId), queryFn: () => srgService.getCampaignBody(srgId), enabled: !!srgId });
}

export function useUpsertCampaignBody(srgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => srgService.upsertCampaignBody(srgId, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.body(srgId) }),
  });
}

export function useCatalogParams(type: string, concesionaria?: string) {
  return useQuery({
    queryKey: KEYS.catalog(type, concesionaria),
    queryFn: () => catalogService.getParams(type, concesionaria),
    enabled: !!type,
  });
}
