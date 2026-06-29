"use client";
import { cn } from "@/lib/utils";
import { Separator } from "@/components/ui";
import { RecentSrgs } from "./RecentSrgs";
import type { DashboardStats } from "@/services/dashboard.service";

function AsesorStatCard({
  label, value, sub, accent,
}: { label: string; value: number; sub?: string; accent?: boolean }) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-lg border border-mist bg-white p-5 shadow-card",
        "transition-shadow duration-200 hover:shadow-panel"
      )}
    >
      <span
        className={cn("absolute inset-x-0 top-0 h-[3px]", accent ? "bg-amber" : "bg-mist")}
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

export function AsesorView({ stats }: { stats: DashboardStats }) {
  const enGestion =
    (stats.by_status.find(s => s.status === "PENDIENTE")?.count ?? 0) +
    (stats.by_status.find(s => s.status === "PREAPROBADO")?.count ?? 0);
  const aprobados = stats.by_status.find(s => s.status === "APROBADO")?.count ?? 0;
  const retornados = stats.by_status.find(s => s.status === "RETORNADO")?.count ?? 0;

  const cards = [
    { label: "Mis SRGs",    value: stats.total,  accent: true },
    { label: "En Gestión",  value: enGestion,    sub: "pendiente + preaprobado" },
    { label: "Aprobados",   value: aprobados,    sub: "por la marca" },
    { label: "Retornados",  value: retornados,   sub: "ciclo completo" },
  ];

  return (
    <>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card, i) => (
          <div key={card.label} className="animate-rise" style={{ animationDelay: `${i * 50}ms` }}>
            <AsesorStatCard {...card} />
          </div>
        ))}
      </div>

      <Separator />

      <div className="animate-rise" style={{ animationDelay: "200ms" }}>
        <h3 className="mb-4 font-display text-h4 text-ink">SRGs Recientes</h3>
        <div className="rounded-lg border border-mist bg-white shadow-card overflow-hidden">
          <RecentSrgs />
        </div>
      </div>
    </>
  );
}
