import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { auditService } from "@/services/audit.service";

const KEYS = {
  all:    ["audits"] as const,
  list:   ()         => ["audits", "list"] as const,
  detail: (id: string) => ["audits", "detail", id] as const,
};

export function useAudits() {
  return useQuery({ queryKey: KEYS.list(), queryFn: auditService.list });
}

export function useAudit(id: string) {
  return useQuery({ queryKey: KEYS.detail(id), queryFn: () => auditService.get(id), enabled: !!id });
}

export function useCreateAudit() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => auditService.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useUpdateAudit(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => auditService.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.detail(id) });
      qc.invalidateQueries({ queryKey: KEYS.all });
    },
  });
}

export function useDeleteAudit() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => auditService.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}
