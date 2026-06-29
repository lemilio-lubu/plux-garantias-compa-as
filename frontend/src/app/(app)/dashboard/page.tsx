"use client";
import { useState } from "react";
import {
  Card, CardHeader, CardTitle, CardContent,
  Select, PageSpinner, Separator,
} from "@/components/ui";
import { StatsCards }    from "@/modules/dashboard/StatsCards";
import { StatusChart }   from "@/modules/dashboard/StatusChart";
import { TypeBreakdown } from "@/modules/dashboard/TypeBreakdown";
import { RecentSrgs }    from "@/modules/dashboard/RecentSrgs";
import { AsesorView }    from "@/modules/dashboard/AsesorView";
import { BodegueroView } from "@/modules/dashboard/BodegueroView";
import { useDashboard }  from "@/hooks/useDashboard";
import { useAuthStore }  from "@/store/auth";
import { CONCESIONARIA_LABELS } from "@/types/auth";

const CONCESIONARIA_OPTIONS = [
  { value: "",               label: "Todas las concesionarias" },
  { value: "SURMOTOR",       label: "Surmotor" },
  { value: "GRANDA_CENTENO", label: "Granda Centeno" },
  { value: "SHYRIS",         label: "Shyris" },
];

const ROLE_META: Record<string, { eyebrow: string; title: string }> = {
  SUPER_ADMIN: { eyebrow: "Vista general",        title: "Dashboard" },
  JEFE_TALLER: { eyebrow: "Vista general",        title: "Dashboard" },
  ASESOR:      { eyebrow: "Mis SRGs",             title: "Mi Actividad" },
  BODEGUERO:   { eyebrow: "Operaciones de Bodega", title: "Panel Bodega" },
};

export default function DashboardPage() {
  const { user } = useAuthStore();
  const role       = user?.role ?? "JEFE_TALLER";
  const isSuperAdmin = role === "SUPER_ADMIN";
  const isManager    = role === "SUPER_ADMIN" || role === "JEFE_TALLER";
  const isAsesor     = role === "ASESOR";
  const isBodeguero  = role === "BODEGUERO";

  const [selectedC, setSelectedC] = useState<string>(
    isSuperAdmin ? "" : (user?.concesionaria ?? "")
  );

  const { data: stats, isLoading, isError } = useDashboard(selectedC || undefined);
  const meta = ROLE_META[role] ?? ROLE_META.JEFE_TALLER;

  const subtitle = isAsesor
    ? "Tu actividad personal de garantías y campañas"
    : isBodeguero
    ? "SRGs con actividad activa en bodega"
    : isSuperAdmin
    ? "Vista consolidada de todas las concesionarias"
    : CONCESIONARIA_LABELS[user?.concesionaria as keyof typeof CONCESIONARIA_LABELS] ?? "";

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="eyebrow text-amber-dark mb-1">{meta.eyebrow}</p>
          <h2 className="font-display text-h3 text-ink">{meta.title}</h2>
          <p className="text-small text-steel mt-0.5">{subtitle}</p>
        </div>

        {isSuperAdmin && (
          <Select
            options={CONCESIONARIA_OPTIONS}
            value={selectedC}
            onChange={e => setSelectedC(e.target.value)}
            className="w-56"
          />
        )}
      </div>

      {isLoading && <PageSpinner />}
      {isError && (
        <p className="rounded-md border border-light-gray bg-off-white p-4 text-small text-mid-gray">
          No se pudieron cargar las estadísticas. Verificá la conexión con el backend.
        </p>
      )}

      {stats && (
        <>
          {/* ASESOR — personal activity */}
          {isAsesor && <AsesorView stats={stats} />}

          {/* BODEGUERO — warehouse action panel */}
          {isBodeguero && <BodegueroView stats={stats} />}

          {/* JEFE_TALLER / SUPER_ADMIN — full operational view */}
          {isManager && (
            <>
              <StatsCards stats={stats} />

              <div className="grid gap-4 lg:grid-cols-3">
                <Card className="lg:col-span-2">
                  <CardHeader><CardTitle>Distribución por Estado</CardTitle></CardHeader>
                  <CardContent>
                    <StatusChart data={stats.by_status} total={stats.total} />
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader><CardTitle>Por Tipo</CardTitle></CardHeader>
                  <CardContent><TypeBreakdown stats={stats} /></CardContent>
                </Card>
              </div>

              {stats.breakdown.length > 0 && (
                <Card>
                  <CardHeader><CardTitle>Desglose Detallado</CardTitle></CardHeader>
                  <CardContent>
                    <div className="grid gap-6 sm:grid-cols-2">
                      {(["WARRANTY", "CAMPAIGN"] as const).map(type => {
                        const rows = stats.breakdown.filter(b => b.srg_type === type);
                        if (rows.length === 0) return null;
                        return (
                          <div key={type}>
                            <p className="mb-3 text-caption font-medium uppercase tracking-wide text-mid-gray">
                              {type === "WARRANTY" ? "Garantías" : "Campañas"}
                            </p>
                            <div className="space-y-1.5">
                              {rows.map(row => (
                                <div key={row.status} className="flex justify-between text-small">
                                  <span className="text-dark-gray">{row.status}</span>
                                  <span className="font-semibold text-black">{row.count}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>
                </Card>
              )}

              <Separator />

              <div>
                <h3 className="mb-4 font-display text-h4 text-ink">SRGs Recientes</h3>
                <div className="rounded-lg border border-mist bg-white shadow-card overflow-hidden">
                  <RecentSrgs />
                </div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
}
