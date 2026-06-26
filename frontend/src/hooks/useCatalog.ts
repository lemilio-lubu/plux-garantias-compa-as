import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { catalogService } from "@/services/catalog.service";
import { useAuthStore } from "@/store/auth";

const KEYS = {
  params:     (type: string, c?: string) => ["catalog", "params", type, c] as const,
  parts:      (c?: string)               => ["catalog", "parts", c] as const,
};

export function useCatalogParams(type: string) {
  const { user } = useAuthStore();
  const c = user?.concesionaria || undefined;
  return useQuery({ queryKey: KEYS.params(type, c), queryFn: () => catalogService.getParams(type, c), enabled: !!type });
}

export function useCreateCatalogParam(type: string) {
  const qc = useQueryClient();
  const { user } = useAuthStore();
  return useMutation({
    mutationFn: (data: { code: string; name: string }) =>
      catalogService.createParam({ ...data, param_type: type, concesionaria: user?.concesionaria ?? "" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["catalog", "params", type] }),
  });
}

export function useDeleteCatalogParam(type: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => catalogService.deleteParam(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["catalog", "params", type] }),
  });
}

export function useSpareParts() {
  const { user } = useAuthStore();
  const c = user?.concesionaria || undefined;
  return useQuery({ queryKey: KEYS.parts(c), queryFn: () => catalogService.getSpareParts(c) });
}

export function useCreateSparePart() {
  const qc = useQueryClient();
  const { user } = useAuthStore();
  return useMutation({
    mutationFn: (data: { catalog_code: string; name: string; unit_price: number }) =>
      catalogService.createSparePart({ ...data, concesionaria: user?.concesionaria ?? "" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["catalog", "parts"] }),
  });
}

export function useUpdateSparePart() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: { id: string; name?: string; unit_price?: number }) =>
      catalogService.updateSparePart(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["catalog", "parts"] }),
  });
}

export function useDeleteSparePart() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => catalogService.deleteSparePart(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["catalog", "parts"] }),
  });
}
