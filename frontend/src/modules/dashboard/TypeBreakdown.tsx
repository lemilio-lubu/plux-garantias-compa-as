import type { DashboardStats } from "@/services/dashboard.service";

interface DonutProps { pct: number; color: string; }

function MiniDonut({ pct, color }: DonutProps) {
  const r  = 20;
  const cx = 24;
  const cy = 24;
  const circumference = 2 * Math.PI * r;
  const dash = (pct / 100) * circumference;

  return (
    <svg width={48} height={48} viewBox="0 0 48 48" className="-rotate-90">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#E5E5E5" strokeWidth={6} />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke={color}
        strokeWidth={6}
        strokeDasharray={`${dash} ${circumference - dash}`}
        strokeLinecap="round"
      />
    </svg>
  );
}

export function TypeBreakdown({ stats }: { stats: DashboardStats }) {
  const warranty = stats.by_type["WARRANTY"] ?? 0;
  const campaign = stats.by_type["CAMPAIGN"] ?? 0;
  const total    = warranty + campaign || 1;

  const wPct = Math.round((warranty / total) * 100);
  const cPct = Math.round((campaign / total) * 100);

  return (
    <div className="space-y-4">
      {[
        { label: "Garantías", count: warranty, pct: wPct, color: "#6EE7B7" },
        { label: "Campañas",  count: campaign, pct: cPct, color: "#C7D2FE" },
      ].map(({ label, count, pct, color }) => (
        <div key={label} className="flex items-center gap-4">
          <MiniDonut pct={pct} color={color} />
          <div>
            <p className="text-small font-medium text-dark-gray">{label}</p>
            <p className="text-h4 font-semibold text-black leading-tight">{count}</p>
            <p className="text-caption text-mid-gray">{pct}% del total</p>
          </div>
        </div>
      ))}

      {/* Combined mini bar */}
      <div className="pt-2">
        <div className="flex h-2 w-full overflow-hidden rounded-full bg-off-white">
          <div className="h-full bg-[#6EE7B7] transition-all duration-500" style={{ width: `${wPct}%` }} />
          <div className="h-full bg-[#C7D2FE] transition-all duration-500" style={{ width: `${cPct}%` }} />
        </div>
        <div className="mt-1 flex justify-between text-caption text-mid-gray">
          <span>Garantías</span><span>Campañas</span>
        </div>
      </div>
    </div>
  );
}
