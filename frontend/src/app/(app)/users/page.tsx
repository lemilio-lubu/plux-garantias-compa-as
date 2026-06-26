"use client";
import { useRouter } from "next/navigation";
import { Plus, Users } from "lucide-react";
import {
  Button, H3, Badge,
  Table, TableHead, TableBody, TableRow, TableHeader, TableCell,
  EmptyState, PageSpinner,
} from "@/components/ui";
import { useUsers, useDeleteUser } from "@/hooks/useUsers";
import { useAuthStore } from "@/store/auth";
import { ROLE_LABELS, CONCESIONARIA_LABELS } from "@/types/auth";
import { Trash2, Pencil } from "lucide-react";

export default function UsersPage() {
  const router  = useRouter();
  const { user: me } = useAuthStore();
  const { data = [], isLoading } = useUsers();
  const remove = useDeleteUser();

  const canCreate = me?.role === "SUPER_ADMIN" || me?.role === "JEFE_TALLER";

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <H3>Usuarios</H3>
          <p className="text-small text-mid-gray mt-0.5">{data.length} registros</p>
        </div>
        {canCreate && (
          <Button onClick={() => router.push("/users/new")}>
            <Plus size={16} /> Nuevo Usuario
          </Button>
        )}
      </div>

      <div className="rounded-lg border border-light-gray bg-white shadow-sm overflow-hidden">
        {isLoading ? (
          <PageSpinner />
        ) : data.length === 0 ? (
          <EmptyState
            icon={Users}
            title="Sin usuarios"
            action={canCreate ? <Button size="sm" onClick={() => router.push("/users/new")}>Nuevo Usuario</Button> : undefined}
          />
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>Nombre</TableHeader>
                <TableHeader>Correo</TableHeader>
                <TableHeader>Rol</TableHeader>
                <TableHeader>Concesionaria</TableHeader>
                <TableHeader>Estado</TableHeader>
                {canCreate && <TableHeader className="w-20" />}
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map(u => (
                <TableRow key={u.id}>
                  <TableCell className="font-medium text-black">{u.full_name}</TableCell>
                  <TableCell className="text-mid-gray">{u.email}</TableCell>
                  <TableCell>{ROLE_LABELS[u.role]}</TableCell>
                  <TableCell>
                    {u.concesionaria
                      ? CONCESIONARIA_LABELS[u.concesionaria as keyof typeof CONCESIONARIA_LABELS]
                      : "—"}
                  </TableCell>
                  <TableCell>
                    <Badge variant={u.is_active ? "aprobado" : "negado"}>
                      {u.is_active ? "Activo" : "Inactivo"}
                    </Badge>
                  </TableCell>
                  {canCreate && (
                    <TableCell>
                      <div className="flex gap-2">
                        <button
                          onClick={() => router.push(`/users/${u.id}/edit`)}
                          className="text-mid-gray hover:text-dark-gray transition-colors"
                        >
                          <Pencil size={14} />
                        </button>
                        {me?.role === "SUPER_ADMIN" && u.id !== me.id && (
                          <button
                            onClick={() => remove.mutate(u.id)}
                            className="text-mid-gray hover:text-[#CC0000] transition-colors"
                          >
                            <Trash2 size={14} />
                          </button>
                        )}
                      </div>
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
