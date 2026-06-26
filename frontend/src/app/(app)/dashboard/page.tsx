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
import { useDashboard }  from "@/hooks/useDashboard";
import { useAuthStore }  from "@/store/auth";
import { CONCESIONARIA_LABELS } from "@/types/auth";

const CONCESIONARIA_OPTIONS = [
  { value: "",              label: "Todas las concesionarias" },
  { value: "SURMOTOR",      label: "Surmotor" },
  { value: "GRANDA_CENTENO",label: "Granda Centeno" },
  { value: "SHYRIS",        label: "Shyris" },
];

export default function DashboardPage() {
  const { user } = useAuthStore();
  const isSuperAdmin = user?.role === "SUPER_ADMIN";
  const [selectedC, setSelectedC] = useState<string>(isSuperAdmin ? "" : (user?.concesionaria ?? ""));

  const { data: stats, isLoading, isError } = useDashboard(selectedC || undefined);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="eyebrow text-amber-dark mb-1">Vista general</p>
          <h2 className="font-display text-h3 text-ink">Dashboard</h2>
          <p className="text-small text-steel mt-0.5">
            {isSuperAdmin
              ? "Vista consolidada de todas las concesionarias"
              : CONCESIONARIA_LABELS[user?.concesionaria as keyof typeof CONCESIONARIA_LABELS] ?? ""}
          </p>
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

      {/* Loading / error */}
      {isLoading && <PageSpinner />}
      {isError && (
        <p className="rounded-md border border-light-gray bg-off-white p-4 text-small text-mid-gray">
          No se pudieron cargar las estadísticas. Verificá la conexión con el backend.
        </p>
      )}

      {stats && (
        <>
          {/* KPI cards */}
          <StatsCards stats={stats} />

          {/* Charts row */}
          <div className="grid gap-4 lg:grid-cols-3">
            {/* Status distribution — 2/3 width */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Distribución por Estado</CardTitle>
              </CardHeader>
              <CardContent>
                <StatusChart data={stats.by_status} total={stats.total} />
              </CardContent>
            </Card>

            {/* Type breakdown — 1/3 width */}
            <Card>
              <CardHeader>
                <CardTitle>Por Tipo</CardTitle>
              </CardHeader>
              <CardContent>
                <TypeBreakdown stats={stats} />
              </CardContent>
            </Card>
          </div>

          {/* Breakdown table — WARRANTY vs CAMPAIGN per status */}
          {stats.breakdown.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Desglose Detallado</CardTitle>
              </CardHeader>
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

          {/* Recent SRGs */}
          <div>
            <h3 className="mb-4 font-display text-h4 text-ink">SRGs Recientes</h3>
            <div className="rounded-lg border border-mist bg-white shadow-card overflow-hidden">
              <RecentSrgs />
            </div>
          </div>
        </>
      )}
    </div>
  );
}
