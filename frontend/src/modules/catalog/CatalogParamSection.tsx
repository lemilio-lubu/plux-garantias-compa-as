"use client";
import { useForm } from "react-hook-form";
import { Trash2, Plus } from "lucide-react";
import {
  Input, Button,
  Table, TableHead, TableBody, TableRow, TableHeader, TableCell,
  EmptyState,
} from "@/components/ui";
import { useCatalogParams, useCreateCatalogParam, useDeleteCatalogParam } from "@/hooks/useCatalog";
import type { CatalogParamType } from "@/types/catalog";

interface Props { type: CatalogParamType; label: string; }

export function CatalogParamSection({ type, label }: Props) {
  const { data = [], isLoading } = useCatalogParams(type);
  const create = useCreateCatalogParam(type);
  const remove = useDeleteCatalogParam(type);

  const { register, handleSubmit, reset } = useForm<{ code: string; name: string }>();

  return (
    <div className="space-y-4">
      {/* Add form */}
      <form
        className="flex flex-wrap items-end gap-3"
        onSubmit={handleSubmit(d => create.mutate(d, { onSuccess: () => reset() }))}
      >
        <Input label="Código" className="w-32" {...register("code", { required: true })} />
        <Input label="Nombre" className="w-64" {...register("name", { required: true })} />
        <Button size="sm" type="submit" loading={create.isPending}>
          <Plus size={14} /> Agregar
        </Button>
      </form>

      {/* List */}
      {isLoading ? (
        <p className="text-small text-mid-gray">Cargando...</p>
      ) : data.length === 0 ? (
        <EmptyState title={`Sin ${label} registrados`} className="py-6" />
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableHeader>Código</TableHeader>
              <TableHeader>Nombre</TableHeader>
              <TableHeader className="w-16" />
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map(p => (
              <TableRow key={p.id}>
                <TableCell className="font-mono font-medium">{p.code}</TableCell>
                <TableCell>{p.name}</TableCell>
                <TableCell>
                  <button
                    onClick={() => remove.mutate(p.id)}
                    className="text-mid-gray hover:text-[#CC0000] transition-colors"
                  >
                    <Trash2 size={14} />
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
