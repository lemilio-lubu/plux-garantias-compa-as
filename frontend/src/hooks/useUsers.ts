import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { userService } from "@/services/user.service";

const KEYS = {
  all:    ["users"] as const,
  list:   ()         => ["users", "list"] as const,
  detail: (id: string) => ["users", "detail", id] as const,
};

export function useUsers() {
  return useQuery({ queryKey: KEYS.list(), queryFn: userService.list });
}

export function useUser(id: string) {
  return useQuery({ queryKey: KEYS.detail(id), queryFn: () => userService.get(id), enabled: !!id });
}

export function useCreateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => userService.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useUpdateUser(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: unknown) => userService.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.detail(id) });
      qc.invalidateQueries({ queryKey: KEYS.all });
    },
  });
}

export function useDeleteUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => userService.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useChangePassword(id: string) {
  return useMutation({
    mutationFn: (data: { current_password: string; new_password: string }) =>
      userService.changePassword(id, data),
  });
}
