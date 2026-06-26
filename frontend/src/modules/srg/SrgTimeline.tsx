"use client";
import { useSrgEvents } from "@/hooks/useSrgs";
import type { SrgEvent, SrgEventType } from "@/types/srg";

export const EVENT_LABEL: Record<SrgEventType, string> = {
  PART_REQUESTED:       "solicitó repuesto",
  RECEPTION_REGISTERED: "recibió en bodega",
  WORK_REGISTERED:      "instaló",
  CORE_RETURN_DECLARED: "devolvió core",
  RETURN_CONFIRMED:     "confirmó devolución",
  STATUS_CHANGED:       "cambió el estado",
};

export function describeEvent(e: SrgEvent): string {
  if (e.event_type === "STATUS_CHANGED") {
    return `${EVENT_LABEL[e.event_type]}: ${e.state_from} → ${e.state_to}`;
  }
  const qty = e.quantity ? `${e.quantity}× ` : "";
  return `${EVENT_LABEL[e.event_type]} ${qty}${e.part_label ?? ""}`.trim();
}

export function SrgTimeline({ srgId }: { srgId: string }) {
  const { data: events = [], isLoading } = useSrgEvents(srgId);

  if (isLoading) return <p className="text-small text-mid-gray">Cargando trazabilidad...</p>;
  if (events.length === 0) return <p className="text-small text-mid-gray">Sin eventos registrados todavía.</p>;

  return (
    <ul className="space-y-3">
      {events.map((e, i) => (
        <li key={e.id} className="animate-rise flex gap-3" style={{ animationDelay: `${Math.min(i, 8) * 40}ms` }}>
          <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-amber" aria-hidden />
          <div className="min-w-0">
            <p className="text-small text-black">
              <span className="font-medium">{e.actor_label || e.actor_role || "Sistema"}</span>{" "}
              <span className="text-mid-gray">{describeEvent(e)}</span>
            </p>
            <p className="text-caption text-mid-gray">{new Date(e.created_at).toLocaleString("es-EC")}</p>
          </div>
        </li>
      ))}
    </ul>
  );
}
