import { cn } from "@/lib/utils";
import type { DashboardStats } from "@/services/dashboard.service";

interface StatCardProps {
  label:    string;
  value:    number;
  sub?:     string;
  accent?:  boolean;
}

function StatCard({ label, value, sub, accent }: StatCardProps) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-lg border border-mist bg-white p-5 shadow-card",
        "transition-shadow duration-200 hover:shadow-panel"
      )}
    >
      {/* Lit top edge marks the primary gauge */}
      <span
        className={cn(
          "absolute inset-x-0 top-0 h-[3px]",
          accent ? "bg-amber" : "bg-mist"
        )}
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

export function StatsCards({ stats }: { stats: DashboardStats }) {
  const aprobados = stats.by_status.find(s => s.status === "APROBADO")?.count ?? 0;
  const pendientes = (stats.by_status.find(s => s.status === "PENDIENTE")?.count ?? 0) +
                    (stats.by_status.find(s => s.status === "PREAPROBADO")?.count ?? 0);

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <StatCard label="Total SRGs"  value={stats.total}                   accent />
      <StatCard label="Garantías"   value={stats.by_type["WARRANTY"] ?? 0} sub="registros" />
      <StatCard label="Campañas"    value={stats.by_type["CAMPAIGN"] ?? 0} sub="registros" />
      <StatCard label="Aprobados"   value={aprobados}
                sub={pendientes > 0 ? `${pendientes} en gestión` : "al día"} />
    </div>
  );
}
