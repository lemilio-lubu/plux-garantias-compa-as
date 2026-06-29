"use client";
import { useRouter } from "next/navigation";
import { Package } from "lucide-react";
import { cn } from "@/lib/utils";
import { EmptyState, PageSpinner } from "@/components/ui";
import { SrgStatusBadge } from "@/modules/srg/SrgStatusBadge";
import { useSrgs } from "@/hooks/useSrgs";
import type { DashboardStats } from "@/services/dashboard.service";

function BodStatCard({
  label, value, sub, topColor,
}: { label: string; value: number; sub?: string; topColor?: string }) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-lg border border-mist bg-white p-5 shadow-card",
        "transition-shadow duration-200 hover:shadow-panel"
      )}
    >
      <span
        className={cn("absolute inset-x-0 top-0 h-[3px]", topColor ?? "bg-mist")}
        aria-hidden
      />
      <p className="eyebrow text-steel">{label}</p>
      <p className="mt-3 font-display text-[40px] font-semibold leading-none tracking-tight text-ink data">
        {value}
      </p>
      {sub && <p className="mt-2 text-caption text-steel">{sub}</p>}
    </div>
  );
}

export function BodegueroView({ stats }: { stats: DashboardStats }) {
  const router = useRouter();
  const { data: srgs = [], isLoading } = useSrgs();

  const proceso    = stats.by_status.find(s => s.status === "PROCESO")?.count ?? 0;
  const pendientes = stats.by_status.find(s => s.status === "PENDIENTE")?.count ?? 0;
  const aprobados  = stats.by_status.find(s => s.status === "APROBADO")?.count ?? 0;
  const activos    = proceso + pendientes + aprobados;

  // PENDIENTE: parts arriving; APROBADO: cores may need return confirmation.
  const actionable = srgs
    .filter(s => s.status === "PENDIENTE" || s.status === "APROBADO")
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 10);

  const cards = [
    { label: "SRGs Activos",      value: activos,    topColor: "bg-amber",              sub: "en concesionaria" },
    { label: "En Proceso",         value: proceso,    topColor: "bg-mist",               sub: "sin acción bodega aún" },
    { label: "Enviados a Marca",   value: pendientes, topColor: "bg-amber",              sub: "repuestos en camino" },
    { label: "Aprobados",          value: aprobados,  topColor: "bg-status-aprobado",    sub: "posibles devoluciones" },
  ];

  return (
    <>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card, i) => (
          <div key={card.label} className="animate-rise" style={{ animationDelay: `${i * 50}ms` }}>
            <BodStatCard {...card} />
          </div>
        ))}
      </div>

      <div className="animate-rise" style={{ animationDelay: "220ms" }}>
        <div className="mb-4 flex items-baseline justify-between">
          <h3 className="font-display text-h4 text-ink">SRGs con Actividad de Bodega</h3>
          <p className="text-caption text-steel">Estado PENDIENTE o APROBADO</p>
        </div>

        {isLoading ? (
          <PageSpinner />
        ) : actionable.length === 0 ? (
          <div className="rounded-lg border border-mist bg-white shadow-card">
            <EmptyState icon={Package} title="Sin actividad de bodega pendiente" className="py-8" />
          </div>
        ) : (
          <div className="rounded-lg border border-mist bg-white shadow-card overflow-hidden">
            <table className="w-full text-small">
              <thead>
                <tr className="border-b border-mist bg-off-white">
                  {["OT", "VIN", "Modelo", "Estado", "Fecha"].map(h => (
                    <th
                      key={h}
                      className="px-4 py-3 text-left text-caption font-medium uppercase tracking-wide text-steel"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-mist">
                {actionable.map(srg => (
                  <tr
                    key={srg.id}
                    onClick={() => router.push(`/srgs/${srg.id}`)}
                    className="cursor-pointer transition-colors duration-100 hover:bg-off-white"
                  >
                    <td className="px-4 py-3 font-mono font-medium text-black">{srg.ot}</td>
                    <td className="px-4 py-3 font-mono text-mid-gray">{srg.vin}</td>
                    <td className="px-4 py-3 text-dark-gray">{srg.vehicle_model}</td>
                    <td className="px-4 py-3"><SrgStatusBadge status={srg.status} /></td>
                    <td className="px-4 py-3 text-mid-gray">
                      {new Date(srg.created_at).toLocaleDateString("es-EC")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
