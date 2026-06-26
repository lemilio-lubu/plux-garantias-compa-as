import { Fragment } from "react";
import { Check, RotateCcw, Ban } from "lucide-react";
import { cn } from "@/lib/utils";
import { STATUS_LABELS, type Srg, type SrgStatus } from "@/types/srg";

// The happy-path sequence every SRG advances through. RETORNADO and NEGADO are
// off-path terminal states shown separately below the track.
const MAIN_FLOW: SrgStatus[] = ["PROCESO", "PENDIENTE", "PREAPROBADO", "APROBADO"];

function fmt(d?: string | null): string {
  if (!d) return "";
  return new Date(d).toLocaleDateString("es-EC", { day: "2-digit", month: "short" });
}

export function SrgStatusTrack({ srg }: { srg: Srg }) {
  const isOffPath = srg.status === "RETORNADO" || srg.status === "NEGADO";
  const currentIdx = MAIN_FLOW.indexOf(srg.status);

  // A timestamp is known for two of the transitions.
  const stepDate: Partial<Record<SrgStatus, string | null>> = {
    PENDIENTE: srg.fecha_envio_marca,
    APROBADO: srg.fecha_aprobacion,
  };

  return (
    <div>
      <p className="eyebrow text-steel mb-4">Trazabilidad del estado</p>

      <div className="flex items-start">
        {MAIN_FLOW.map((st, i) => {
          const done = !isOffPath && i < currentIdx;
          const current = !isOffPath && i === currentIdx;
          const reached = done || current;
          return (
            <Fragment key={st}>
              <div className="flex w-[72px] shrink-0 flex-col items-center gap-1.5 text-center">
                <span
                  className={cn(
                    "flex h-8 w-8 items-center justify-center rounded-full border-2 transition-colors",
                    current && "border-amber bg-amber text-ink shadow-amber",
                    done && "border-ink bg-ink text-white",
                    !reached && "border-mist bg-white text-steel"
                  )}
                >
                  {done ? (
                    <Check size={15} strokeWidth={2.5} />
                  ) : (
                    <span className="font-mono text-caption font-semibold">{i + 1}</span>
                  )}
                </span>
                <span className={cn("eyebrow leading-tight", reached ? "text-ink" : "text-steel/60")}>
                  {STATUS_LABELS[st]}
                </span>
                <span className="data h-3 text-[10px] leading-none text-steel">{fmt(stepDate[st])}</span>
              </div>

              {i < MAIN_FLOW.length - 1 && (
                <span
                  className={cn(
                    "mt-[15px] h-0.5 flex-1 rounded-full transition-colors",
                    done ? "bg-ink" : "bg-mist"
                  )}
                  aria-hidden
                />
              )}
            </Fragment>
          );
        })}
      </div>

      {isOffPath && (
        <div
          className={cn(
            "mt-5 flex items-center gap-2.5 rounded-md border px-3 py-2.5 text-small font-medium",
            srg.status === "RETORNADO"
              ? "border-status-retornado/30 bg-[#FBEEF0] text-status-retornado"
              : "border-status-negado/30 bg-paper text-status-negado"
          )}
        >
          {srg.status === "RETORNADO" ? <RotateCcw size={15} /> : <Ban size={15} />}
          {srg.status === "RETORNADO"
            ? "Retornado por la marca — requiere corrección y reenvío."
            : "Negado por la marca — solicitud cerrada sin aprobación."}
        </div>
      )}
    </div>
  );
}
