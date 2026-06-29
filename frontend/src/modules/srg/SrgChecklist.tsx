"use client";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Package, Plus, Check, Minus } from "lucide-react";
import { Button, Input, EmptyState } from "@/components/ui";
import { useSrgParts, useAddPart, useRegisterMovement } from "@/hooks/useSrgs";
import { useAuthStore } from "@/store/auth";
import { cn } from "@/lib/utils";
import type { Srg, PartLedger, ReceptionState, ReturnState } from "@/types/srg";
import type { SparePart } from "@/types/catalog";
import { SparePartPicker } from "./SparePartPicker";

const RECEPTION_STYLE: Record<ReceptionState, { label: string; cls: string }> = {
  PENDIENTE: { label: "Recepción pendiente", cls: "border-mist text-steel" },
  PARCIAL:   { label: "Recepción parcial",   cls: "border-amber/50 bg-amber/10 text-[#8a6500]" },
  COMPLETA:  { label: "Recibido completo",   cls: "border-status-aprobado/40 bg-status-aprobado/10 text-status-aprobado" },
};

const RETURN_STYLE: Record<ReturnState, { label: string; cls: string }> = {
  NO_APLICA: { label: "Sin instalar aún",     cls: "border-mist text-steel" },
  PENDIENTE: { label: "Devolución pendiente", cls: "border-mist text-steel" },
  PARCIAL:   { label: "Devolución parcial",   cls: "border-amber/50 bg-amber/10 text-[#8a6500]" },
  COMPLETA:  { label: "Devolución completa",  cls: "border-status-aprobado/40 bg-status-aprobado/10 text-status-aprobado" },
};

function StateBadge({ label, cls, done }: { label: string; cls: string; done?: boolean }) {
  return (
    <span className={cn("inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-caption font-medium", cls, done && "animate-pop")}>
      {done && <Check size={11} strokeWidth={3} />}
      {label}
    </span>
  );
}

function Bar({ pct, complete }: { pct: number; complete: boolean }) {
  return (
    <div className="h-2 overflow-hidden rounded-full bg-mist">
      <div
        className={cn("h-full rounded-full progress-fill", complete ? "bg-status-aprobado" : "bg-amber")}
        style={{ transform: `scaleX(${Math.max(0, Math.min(pct, 1))})` }}
      />
    </div>
  );
}

function Chip({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md bg-off-white px-2.5 py-1.5">
      <p className="text-caption text-mid-gray uppercase tracking-wide">{label}</p>
      <p className="data text-small font-medium text-black">{value}</p>
    </div>
  );
}

function MoveControl({
  label, icon, max, pending, onSubmit,
}: {
  label: string; icon: React.ReactNode; max: number; pending: boolean;
  onSubmit: (qty: number) => void;
}) {
  const [qty, setQty] = useState(1);
  const clamped = Math.max(1, Math.min(qty || 1, max));
  return (
    <div className="flex items-end gap-2">
      <Input
        label={`${label} (máx ${max})`}
        type="number"
        min={1}
        max={max}
        value={qty}
        onChange={(e) => setQty(Number(e.target.value))}
        className="h-9 w-28"
      />
      <Button size="sm" loading={pending} onClick={() => onSubmit(clamped)} className="h-9">
        {icon}
      </Button>
    </div>
  );
}

function ReturnConfirmControl({
  max, pending, onSubmit,
}: {
  max: number; pending: boolean;
  onSubmit: (qty: number, location: string) => void;
}) {
  const [qty, setQty] = useState(1);
  const [location, setLocation] = useState("");
  const clamped = Math.max(1, Math.min(qty || 1, max));
  const canSubmit = location.trim().length > 0;
  return (
    <div className="rounded-lg border border-amber/30 bg-amber/5 p-3 space-y-2">
      <p className="text-caption font-medium text-[#8a6500] uppercase tracking-wide">Confirmar devolución</p>
      <div className="flex flex-wrap items-end gap-2">
        <Input
          label={`Cantidad (máx ${max})`}
          type="number"
          min={1}
          max={max}
          value={qty}
          onChange={(e) => setQty(Number(e.target.value))}
          className="h-9 w-28"
        />
        <Input
          label="Ubicación en bodega"
          placeholder="Ej. ESTANTE-A3"
          value={location}
          onChange={(e) => setLocation(e.target.value.toUpperCase())}
          className="h-9 w-44"
        />
        <Button
          size="sm"
          loading={pending}
          disabled={!canSubmit}
          onClick={() => onSubmit(clamped, location.trim())}
          className="h-9"
        >
          <Check size={14} />
        </Button>
      </div>
    </div>
  );
}

function PartCard({
  srgId, part, canReceive, canWork,
}: {
  srgId: string; part: PartLedger; canReceive: boolean; canWork: boolean;
}) {
  const move = useRegisterMovement(srgId);
  const submit = (event_type: string) => (quantity: number, location?: string) =>
    move.mutate({ partId: part.id, event_type, quantity, ...(location ? { location } : {}) });

  const rec = RECEPTION_STYLE[part.reception_state];
  const ret = RETURN_STYLE[part.return_state];
  const recComplete = part.reception_state === "COMPLETA";
  const retComplete = part.return_state === "COMPLETA";

  const toInstall = part.received - part.used;
  const toDeclare = part.used - part.returned_declared;
  const toConfirm = part.returned_declared - part.returned_confirmed;

  return (
    <div className="rounded-lg border border-mist bg-white p-4 shadow-card">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="data font-medium text-black">{part.catalog_code}</p>
          <p className="text-small text-mid-gray">{part.name_es} · solicitadas x{part.requested}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <StateBadge label={rec.label} cls={rec.cls} done={recComplete} />
          {part.return_state !== "NO_APLICA" && <StateBadge label={ret.label} cls={ret.cls} done={retComplete} />}
        </div>
      </div>

      <div className="my-3 grid grid-cols-3 gap-2 sm:grid-cols-5">
        <Chip label="Solicitado" value={part.requested} />
        <Chip label="Recibido" value={part.received} />
        <Chip label="Usado" value={part.used} />
        <Chip label="Devuelto" value={part.returned_confirmed} />
        <Chip label="Pendiente" value={part.pending_reception} />
      </div>

      <div className="mb-1 flex justify-between text-caption text-mid-gray">
        <span>Recibido en bodega</span><span className="data">{part.received} / {part.requested}</span>
      </div>
      <Bar pct={part.requested ? part.received / part.requested : 0} complete={recComplete} />

      {part.used > 0 && (
        <>
          <div className="mb-1 mt-3 flex justify-between text-caption text-mid-gray">
            <span>Cores devueltos a bodega</span><span className="data">{part.returned_confirmed} / {part.used}</span>
          </div>
          <Bar pct={part.used ? part.returned_confirmed / part.used : 0} complete={retComplete} />
        </>
      )}

      <div className="mt-4 flex flex-wrap gap-4">
        {canReceive && part.pending_reception > 0 && (
          <MoveControl label="Recibir" icon={<Package size={14} />} max={part.pending_reception} pending={move.isPending} onSubmit={submit("RECEPTION_REGISTERED")} />
        )}
        {canWork && toInstall > 0 && (
          <MoveControl label="Instalar" icon={<Check size={14} />} max={toInstall} pending={move.isPending} onSubmit={submit("WORK_REGISTERED")} />
        )}
        {canWork && toDeclare > 0 && (
          <MoveControl label="Devolver core" icon={<Minus size={14} />} max={toDeclare} pending={move.isPending} onSubmit={submit("CORE_RETURN_DECLARED")} />
        )}
        {canReceive && toConfirm > 0 && (
          <ReturnConfirmControl max={toConfirm} pending={move.isPending} onSubmit={submit("RETURN_CONFIRMED")} />
        )}
      </div>

      {move.isError && <p className="mt-2 text-caption text-[#CC0000]">No se pudo registrar el movimiento. Verificá la cantidad.</p>}
    </div>
  );
}

type PartFormValues = {
  catalog_code: string; name_es: string; quantity: number;
  unit_price: number; part_origin: string; invoice_number: string;
};

const EMPTY_PART: Partial<PartFormValues> = {
  catalog_code: "", name_es: "", quantity: 1,
  unit_price: undefined, part_origin: "", invoice_number: "",
};

function AddPartForm({ srgId }: { srgId: string }) {
  const { register, handleSubmit, reset, setValue, watch, formState: { errors } } =
    useForm<PartFormValues>({ defaultValues: { quantity: 1 } });
  const addPart = useAddPart(srgId);

  const catalogCode = watch("catalog_code");
  const nameEs      = watch("name_es");
  const unitPrice   = watch("unit_price");

  function onSelectPart(p: SparePart) {
    setValue("catalog_code", p.catalog_code, { shouldValidate: true });
    setValue("name_es", p.name, { shouldValidate: true });
    setValue("unit_price", Number(p.unit_price), { shouldValidate: true });
  }

  return (
    <form
      className="space-y-3 rounded-lg border border-light-gray bg-off-white p-4"
      onSubmit={handleSubmit((data) => addPart.mutate(data, { onSuccess: () => reset(EMPTY_PART) }))}
    >
      <input type="hidden" {...register("catalog_code", { required: true })} />
      <input type="hidden" {...register("name_es", { required: true })} />
      <input type="hidden" {...register("unit_price", { required: true })} />

      <div className="grid gap-3 sm:grid-cols-2">
        <SparePartPicker
          value={catalogCode}
          onSelect={onSelectPart}
          error={errors.catalog_code ? "Elegí un repuesto del catálogo" : undefined}
        />
        <div className="grid grid-cols-2 gap-3">
          <Input label="Nombre" value={nameEs ?? ""} readOnly placeholder="—" />
          <Input label="Precio Unit." value={unitPrice ?? ""} readOnly placeholder="—" />
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        <Input label="Cantidad" type="number" min={1}
          error={errors.quantity ? "Requerida" : undefined}
          {...register("quantity", { valueAsNumber: true, min: 1, required: true })} />
        <Input label="Origen Pieza"
          error={errors.part_origin ? "Requerido" : undefined}
          {...register("part_origin", { required: true })} />
        <Input label="Nro. Factura"
          error={errors.invoice_number ? "Requerido" : undefined}
          {...register("invoice_number", { required: true })} />
      </div>

      <div className="flex justify-end">
        <Button size="sm" type="submit" loading={addPart.isPending}>
          <Plus size={14} /> Solicitar Repuesto
        </Button>
      </div>
    </form>
  );
}

export function SrgChecklist({ srg }: { srg: Srg }) {
  const { user } = useAuthStore();
  const role = user?.role;
  const isManager = role === "JEFE_TALLER" || role === "SUPER_ADMIN";
  const canReceive = role === "BODEGUERO" || isManager;
  const canWork = role === "ASESOR" || isManager;
  const canAdd = role === "ASESOR" || isManager;

  const { data: parts = [], isLoading } = useSrgParts(srg.id);

  return (
    <div className="space-y-4">
      {canAdd && <AddPartForm srgId={srg.id} />}

      {isLoading ? (
        <p className="py-4 text-small text-mid-gray">Cargando repuestos...</p>
      ) : parts.length === 0 ? (
        <EmptyState icon={Package} title="Sin repuestos solicitados" className="py-8" />
      ) : (
        <div className="space-y-3">
          {parts.map((part, i) => (
            <div key={part.id} className="animate-rise" style={{ animationDelay: `${i * 50}ms` }}>
              <PartCard srgId={srg.id} part={part} canReceive={canReceive} canWork={canWork} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
