import { cn } from "@/lib/utils";
import { STATUS_LABELS, type SrgStatus } from "@/types/srg";
import type { StatusCount } from "@/services/dashboard.service";

const STATUS_COLORS: Record<string, string> = {
  PROCESO:     "bg-status-proceso",
  PENDIENTE:   "bg-status-pendiente",
  PREAPROBADO: "bg-status-preaprobado",
  APROBADO:    "bg-status-aprobado",
  RETORNADO:   "bg-status-retornado",
  NEGADO:      "bg-status-negado",
};

const STATUS_TEXT: Record<string, string> = {
  PROCESO:     "text-status-proceso",
  PENDIENTE:   "text-status-pendiente",
  PREAPROBADO: "text-status-preaprobado",
  APROBADO:    "text-status-aprobado",
  RETORNADO:   "text-status-retornado",
  NEGADO:      "text-status-negado",
};

// Ensure all statuses are shown even with 0 count
const ALL_STATUSES: SrgStatus[] = [
  "PROCESO", "PENDIENTE", "PREAPROBADO", "APROBADO", "RETORNADO", "NEGADO",
];

export function StatusChart({ data, total }: { data: StatusCount[]; total: number }) {
  const countMap = Object.fromEntries(data.map(d => [d.status, d.count]));
  const max = Math.max(...ALL_STATUSES.map(s => countMap[s] ?? 0), 1);

  return (
    <div className="space-y-3">
      {ALL_STATUSES.map(status => {
        const count = countMap[status] ?? 0;
        const pct   = Math.round((count / max) * 100);
        const share = total > 0 ? Math.round((count / total) * 100) : 0;

        return (
          <div key={status} className="flex items-center gap-3">
            {/* Label */}
            <span
              className={cn(
                "w-24 shrink-0 text-caption font-medium uppercase tracking-wide",
                STATUS_TEXT[status]
              )}
            >
              {STATUS_LABELS[status]}
            </span>

            {/* Bar */}
            <div className="flex-1 overflow-hidden rounded-sm bg-paper h-2.5">
              <div
                className={cn("h-full rounded-sm transition-all duration-500", STATUS_COLORS[status])}
                style={{ width: `${pct}%` }}
              />
            </div>

            {/* Count + share */}
            <div className="w-20 shrink-0 text-right data">
              <span className="text-small font-semibold text-ink">{count}</span>
              <span className="ml-1 text-caption text-steel">({share}%)</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
