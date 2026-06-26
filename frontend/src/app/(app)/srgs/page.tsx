"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { FileText, Plus, ChevronDown } from "lucide-react";
import {
  Button, Input, Select,
  Table, TableHead, TableBody, TableRow, TableHeader, TableCell,
  EmptyState, PageSpinner,
} from "@/components/ui";
import { SrgStatusBadge, SrgTypeBadge } from "@/modules/srg/SrgStatusBadge";
import { useSrgs } from "@/hooks/useSrgs";
import { useAuthStore } from "@/store/auth";

const STATUS_OPTIONS = [
  { value: "", label: "Todos los estados" },
  { value: "PROCESO",     label: "Proceso" },
  { value: "PENDIENTE",   label: "Pendiente" },
  { value: "PREAPROBADO", label: "Preaprobado" },
  { value: "APROBADO",    label: "Aprobado" },
  { value: "RETORNADO",   label: "Retornado" },
  { value: "NEGADO",      label: "Negado" },
];

const TYPE_OPTIONS = [
  { value: "", label: "Todos los tipos" },
  { value: "WARRANTY", label: "Garantía" },
  { value: "CAMPAIGN", label: "Campaña" },
];

export default function SrgsPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [search, setSearch]     = useState("");
  const [statusF, setStatusF]   = useState("");
  const [typeF, setTypeF]       = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  const { data = [], isLoading } = useSrgs();

  const canCreate = ["ASESOR", "JEFE_TALLER", "SUPER_ADMIN"].includes(user?.role ?? "");

  const filtered = data.filter(srg => {
    const q = search.trim().toLowerCase();
    const matchQ = !q || srg.ot.toLowerCase().includes(q) || srg.vin.toLowerCase().includes(q);
    const matchS = !statusF || srg.status === statusF;
    const matchT = !typeF   || srg.srg_type === typeF;
    return matchQ && matchS && matchT;
  });

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-h4 font-semibold text-black">SRGs</h2>
          <p className="text-small text-mid-gray mt-0.5">{data.length} registros</p>
        </div>
        {canCreate && (
          <div className="relative">
            <Button onClick={() => setMenuOpen(o => !o)}>
              <Plus size={16} /> Nuevo SRG <ChevronDown size={14} />
            </Button>
            {menuOpen && (
              <div className="absolute right-0 top-full mt-1 z-10 w-44 rounded-md border border-light-gray bg-white shadow-card">
                <button
                  className="flex w-full items-center gap-2 px-4 py-2.5 text-small hover:bg-off-white"
                  onClick={() => { setMenuOpen(false); router.push("/srgs/new/warranty"); }}
                >
                  Garantía
                </button>
                <button
                  className="flex w-full items-center gap-2 px-4 py-2.5 text-small hover:bg-off-white"
                  onClick={() => { setMenuOpen(false); router.push("/srgs/new/campaign"); }}
                >
                  Campaña
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <Input
          placeholder="Buscar por OT o VIN..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-64"
        />
        <Select
          options={STATUS_OPTIONS}
          value={statusF}
          onChange={e => setStatusF(e.target.value)}
          className="w-48"
        />
        <Select
          options={TYPE_OPTIONS}
          value={typeF}
          onChange={e => setTypeF(e.target.value)}
          className="w-40"
        />
      </div>

      {/* Table */}
      <div className="rounded-lg border border-light-gray bg-white shadow-sm overflow-hidden">
        {isLoading ? (
          <PageSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState
            icon={FileText}
            title="Sin SRGs"
            description="No se encontraron registros con los filtros aplicados."
          />
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>OT</TableHeader>
                <TableHeader>Tipo</TableHeader>
                <TableHeader>Estado</TableHeader>
                <TableHeader>VIN</TableHeader>
                <TableHeader>Modelo</TableHeader>
                <TableHeader>Fecha</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {filtered.map(srg => (
                <TableRow key={srg.id} onClick={() => router.push(`/srgs/${srg.id}`)}>
                  <TableCell className="font-mono font-medium text-black">{srg.ot}</TableCell>
                  <TableCell><SrgTypeBadge type={srg.srg_type} /></TableCell>
                  <TableCell><SrgStatusBadge status={srg.status} /></TableCell>
                  <TableCell className="font-mono text-mid-gray">{srg.vin}</TableCell>
                  <TableCell>{srg.vehicle_model}</TableCell>
                  <TableCell className="text-mid-gray">
                    {new Date(srg.created_at).toLocaleDateString("es-EC")}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
