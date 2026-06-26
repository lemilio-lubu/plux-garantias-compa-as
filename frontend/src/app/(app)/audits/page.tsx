"use client";
import { useRouter } from "next/navigation";
import { Plus, ClipboardCheck } from "lucide-react";
import {
  Button, H3,
  Table, TableHead, TableBody, TableRow, TableHeader, TableCell,
  EmptyState, PageSpinner,
} from "@/components/ui";
import { useAudits, useDeleteAudit } from "@/hooks/useAudits";
import { useAuthStore } from "@/store/auth";
import { Trash2 } from "lucide-react";

export default function AuditsPage() {
  const router  = useRouter();
  const { user } = useAuthStore();
  const { data = [], isLoading } = useAudits();
  const remove  = useDeleteAudit();

  const canCreate = user?.role === "AUDITOR";
  const canDelete = user?.role === "AUDITOR";

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <H3>Auditorías</H3>
          <p className="text-small text-mid-gray mt-0.5">{data.length} registros</p>
        </div>
        {canCreate && (
          <Button onClick={() => router.push("/audits/new")}>
            <Plus size={16} /> Nueva Auditoría
          </Button>
        )}
      </div>

      <div className="rounded-lg border border-light-gray bg-white shadow-sm overflow-hidden">
        {isLoading ? (
          <PageSpinner />
        ) : data.length === 0 ? (
          <EmptyState
            icon={ClipboardCheck}
            title="Sin auditorías"
            description="Creá la primera auditoría seleccionando un SRG."
            action={canCreate ? <Button size="sm" onClick={() => router.push("/audits/new")}>Nueva Auditoría</Button> : undefined}
          />
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>OT Factura</TableHeader>
                <TableHeader>Observaciones</TableHeader>
                <TableHeader>Concesionaria</TableHeader>
                <TableHeader>Fecha</TableHeader>
                {canDelete && <TableHeader className="w-12" />}
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map(a => (
                <TableRow key={a.id} onClick={() => router.push(`/audits/${a.id}`)}>
                  <TableCell className="font-mono font-medium text-black">{a.ot_factura}</TableCell>
                  <TableCell className="max-w-xs truncate">{a.observations}</TableCell>
                  <TableCell>{a.concesionaria}</TableCell>
                  <TableCell className="text-mid-gray">
                    {new Date(a.created_at).toLocaleDateString("es-EC")}
                  </TableCell>
                  {canDelete && (
                    <TableCell>
                      <button
                        onClick={e => { e.stopPropagation(); remove.mutate(a.id); }}
                        className="text-mid-gray hover:text-[#CC0000] transition-colors"
                      >
                        <Trash2 size={14} />
                      </button>
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
