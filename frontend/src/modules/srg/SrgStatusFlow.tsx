"use client";
import { useState } from "react";
import { Button, Input } from "@/components/ui";
import { useTransitionStatus } from "@/hooks/useSrgs";
import { useAuthStore } from "@/store/auth";
import type { Srg, SrgStatus } from "@/types/srg";

interface TransitionButton {
  label:      string;
  status:     SrgStatus;
  variant:    "primary" | "secondary" | "destructive";
  needsFecha?: boolean;
}

function getTransitions(srg: Srg): TransitionButton[] {
  switch (srg.status) {
    case "PROCESO":
      if (srg.srg_type === "CAMPAIGN") {
        return [
          { label: "Enviar a Marca",  status: "PENDIENTE", variant: "primary" },
          { label: "Aprobar",         status: "APROBADO",  variant: "primary", needsFecha: true },
        ];
      }
      return [{ label: "Enviar a Marca", status: "PENDIENTE", variant: "primary" }];

    case "PENDIENTE":
      return [
        { label: "Preaprobado",        status: "PREAPROBADO", variant: "primary" },
        { label: "Marcar Retornado",   status: "RETORNADO",   variant: "secondary" },
        { label: "Marcar Negado",      status: "NEGADO",      variant: "destructive" },
      ];

    case "PREAPROBADO":
      return [
        { label: "Aprobar",            status: "APROBADO",  variant: "primary", needsFecha: true },
        { label: "Marcar Retornado",   status: "RETORNADO", variant: "secondary" },
        { label: "Marcar Negado",      status: "NEGADO",    variant: "destructive" },
      ];

    case "RETORNADO":
      return [{ label: "Reabrir en Proceso", status: "PROCESO", variant: "secondary" }];

    default:
      return [];
  }
}

export function SrgStatusFlow({ srg }: { srg: Srg }) {
  const { user } = useAuthStore();
  const transition = useTransitionStatus(srg.id);
  const [fecha, setFecha] = useState("");
  const [pendingStatus, setPendingStatus] = useState<SrgStatus | null>(null);

  const canTransition = user?.role === "ASESOR" || user?.role === "JEFE_TALLER" || user?.role === "SUPER_ADMIN";
  const buttons = getTransitions(srg);

  if (!canTransition || buttons.length === 0) return null;

  function handleTransition(btn: TransitionButton) {
    if (btn.needsFecha) {
      setPendingStatus(btn.status);
      return;
    }
    transition.mutate({ new_status: btn.status });
  }

  if (pendingStatus) {
    return (
      <div className="flex items-end gap-3 rounded-md border border-light-gray bg-off-white p-4">
        <Input
          label="Fecha de aprobación"
          type="date"
          value={fecha}
          onChange={e => setFecha(e.target.value)}
          className="w-48"
        />
        <Button
          variant="primary"
          size="sm"
          disabled={!fecha}
          loading={transition.isPending}
          onClick={() => transition.mutate({ new_status: pendingStatus, fecha_aprobacion: fecha })}
        >
          Confirmar
        </Button>
        <Button variant="ghost" size="sm" onClick={() => setPendingStatus(null)}>
          Cancelar
        </Button>
      </div>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      {buttons.map(btn => (
        <Button
          key={btn.status}
          variant={btn.variant}
          size="sm"
          loading={transition.isPending}
          onClick={() => handleTransition(btn)}
        >
          {btn.label}
        </Button>
      ))}
    </div>
  );
}
