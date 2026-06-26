"use client";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Trash2, Pencil, Plus, Check, X } from "lucide-react";
import {
  Input, Button,
  Table, TableHead, TableBody, TableRow, TableHeader, TableCell,
  EmptyState,
} from "@/components/ui";
import { useSpareParts, useCreateSparePart, useUpdateSparePart, useDeleteSparePart } from "@/hooks/useCatalog";
import type { SparePart } from "@/types/catalog";

function EditRow({ part, onDone }: { part: SparePart; onDone: () => void }) {
  const update = useUpdateSparePart();
  const { register, handleSubmit } = useForm({ defaultValues: { name: part.name, unit_price: Number(part.unit_price) } });
  return (
    <TableRow>
      <TableCell className="font-mono">{part.catalog_code}</TableCell>
      <TableCell>
        <Input className="h-8 text-small" {...register("name")} />
      </TableCell>
      <TableCell>
        <Input type="number" step="0.01" className="h-8 w-24 text-small" {...register("unit_price", { valueAsNumber: true })} />
      </TableCell>
      <TableCell>
        <div className="flex gap-1">
          <button onClick={handleSubmit(d => update.mutate({ id: part.id, ...d }, { onSuccess: onDone }))}
            className="text-[#065F46] hover:opacity-70"><Check size={14} /></button>
          <button onClick={onDone} className="text-mid-gray hover:opacity-70"><X size={14} /></button>
        </div>
      </TableCell>
    </TableRow>
  );
}

export function SparePartsTab() {
  const { data = [], isLoading } = useSpareParts();
  const create = useCreateSparePart();
  const remove = useDeleteSparePart();
  const [editing, setEditing] = useState<string | null>(null);

  const { register, handleSubmit, reset } = useForm<{
    catalog_code: string; name: string; unit_price: number;
  }>();

  return (
    <div className="space-y-5">
      {/* Add form */}
      <form
        className="flex flex-wrap items-end gap-3"
        onSubmit={handleSubmit(d => create.mutate(d, { onSuccess: () => reset() }))}
      >
        <Input label="Cód. Catálogo" className="w-36" {...register("catalog_code", { required: true })} />
        <Input label="Nombre" className="w-64" {...register("name", { required: true })} />
        <Input label="Precio Unit." type="number" step="0.01" className="w-28"
          {...register("unit_price", { required: true, valueAsNumber: true })} />
        <Button size="sm" type="submit" loading={create.isPending}>
          <Plus size={14} /> Agregar
        </Button>
      </form>

      {/* Table */}
      {isLoading ? (
        <p className="text-small text-mid-gray">Cargando...</p>
      ) : data.length === 0 ? (
        <EmptyState title="Sin repuestos registrados" className="py-6" />
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableHeader>Código</TableHeader>
              <TableHeader>Nombre</TableHeader>
              <TableHeader>Precio Unit.</TableHeader>
              <TableHeader className="w-20" />
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map(p =>
              editing === p.id ? (
                <EditRow key={p.id} part={p} onDone={() => setEditing(null)} />
              ) : (
                <TableRow key={p.id}>
                  <TableCell className="font-mono font-medium">{p.catalog_code}</TableCell>
                  <TableCell>{p.name}</TableCell>
                  <TableCell>${p.unit_price}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <button onClick={() => setEditing(p.id)} className="text-mid-gray hover:text-dark-gray"><Pencil size={14} /></button>
                      <button onClick={() => remove.mutate(p.id)} className="text-mid-gray hover:text-[#CC0000]"><Trash2 size={14} /></button>
                    </div>
                  </TableCell>
                </TableRow>
              )
            )}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
