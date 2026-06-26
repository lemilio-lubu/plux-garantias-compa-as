"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { ClipboardCheck } from "lucide-react";
import {
  H3, Select,
  Table, TableHead, TableBody, TableRow, TableHeader, TableCell,
  EmptyState, PageSpinner,
} from "@/components/ui";
import { useGlobalEvents } from "@/hooks/useSrgs";
import { EVENT_LABEL, describeEvent } from "@/modules/srg/SrgTimeline";

const TYPE_OPTIONS = [
  { value: "", label: "Todos los eventos" },
  ...Object.entries(EVENT_LABEL).map(([value, label]) => ({
    value,
    label: label.charAt(0).toUpperCase() + label.slice(1),
  })),
];

export default function EventsPage() {
  const router = useRouter();
  const [type, setType] = useState("");
  const { data = [], isLoading } = useGlobalEvents(type ? { event_type: type } : undefined);

  return (
    <div className="space-y-6">
      <div>
        <H3>Trazabilidad</H3>
        <p className="mt-0.5 text-small text-mid-gray">{data.length} eventos registrados</p>
      </div>

      <Select options={TYPE_OPTIONS} value={type} onChange={(e) => setType(e.target.value)} className="w-64" />

      <div className="overflow-hidden rounded-lg border border-light-gray bg-white shadow-sm">
        {isLoading ? (
          <PageSpinner />
        ) : data.length === 0 ? (
          <EmptyState icon={ClipboardCheck} title="Sin eventos" description="No hay actividad con el filtro aplicado." />
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>Fecha</TableHeader>
                <TableHeader>Responsable</TableHeader>
                <TableHeader>Rol</TableHeader>
                <TableHeader>Evento</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((e) => (
                <TableRow key={e.id} onClick={() => router.push(`/srgs/${e.srg_id}`)}>
                  <TableCell className="text-mid-gray">{new Date(e.created_at).toLocaleString("es-EC")}</TableCell>
                  <TableCell className="font-medium text-black">{e.actor_label || "Sistema"}</TableCell>
                  <TableCell className="text-mid-gray">{e.actor_role}</TableCell>
                  <TableCell>{describeEvent(e)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
