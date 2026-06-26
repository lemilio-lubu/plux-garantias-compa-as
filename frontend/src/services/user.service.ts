import { api } from "@/lib/api";
import type { User } from "@/types/auth";

export const userService = {
  list:   ()         => api.get<User[]>("/users/").then(r => r.data),
  get:    (id: string) => api.get<User>(`/users/${id}/`).then(r => r.data),
  create: (data: unknown) => api.post<User>("/users/", data).then(r => r.data),
  update: (id: string, data: unknown) => api.patch<User>(`/users/${id}/`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/users/${id}/`),
  changePassword: (id: string, data: { current_password: string; new_password: string }) =>
    api.post(`/users/${id}/change-password/`, data),
};
