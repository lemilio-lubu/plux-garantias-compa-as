"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm, useFieldArray } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Plus, Trash2, Search } from "lucide-react";
import { Input, Textarea, Button, Card, CardContent, Small } from "@/components/ui";
import { useCreateAudit, useUpdateAudit } from "@/hooks/useAudits";
import { useSrgs } from "@/hooks/useSrgs";
import type { Audit } from "@/types/audit";
import type { Srg } from "@/types/srg";

const schema = z.object({
  srg_id:       z.string().uuid("Seleccioná un SRG válido"),
  ot_factura:   z.string().min(1),
  observations: z.string().min(1),
  additional_emails: z.array(z.object({ email: z.string().email() })),
  attachments:       z.array(z.object({ file_name: z.string().min(1), file_url: z.string().url() })),
});

type Form = z.infer<typeof schema>;

interface Props { audit?: Audit; }

export function AuditForm({ audit }: Props) {
  const router = useRouter();
  const [search, setSearch]     = useState("");
  const [selected, setSelected] = useState<Srg | null>(null);

  const { data: srgs = [] } = useSrgs();
  const create = useCreateAudit();
  const update = useUpdateAudit(audit?.id ?? "");

  const { register, handleSubmit, setValue, formState: { errors }, control } = useForm<Form>({
    resolver: zodResolver(schema),
    defaultValues: {
      srg_id:            audit?.srg_id ?? "",
      ot_factura:        audit?.ot_factura ?? "",
      observations:      audit?.observations ?? "",
      additional_emails: (audit?.additional_emails ?? []).map(e => ({ email: e })),
      attachments:       audit?.attachments ?? [],
    },
  });

  const emails      = useFieldArray({ control, name: "additional_emails" });
  const attachments = useFieldArray({ control, name: "attachments" });

  const filtered = search.trim()
    ? srgs.filter(s => s.ot.includes(search) || s.vin.includes(search))
    : [];

  function selectSrg(srg: Srg) {
    setSelected(srg);
    setValue("srg_id", srg.id);
    setSearch("");
  }

  function onSubmit(data: Form) {
    const payload = {
      ...data,
      additional_emails: data.additional_emails.map(e => e.email),
    };
    if (audit) {
      update.mutate(payload, { onSuccess: () => router.back() });
    } else {
      create.mutate(payload, { onSuccess: a => router.push(`/audits/${a.id}`) });
    }
  }

  const isPending = create.isPending || update.isPending;

  return (
    <Card>
      <CardContent>
        <form className="space-y-6" onSubmit={handleSubmit(onSubmit)} noValidate>
          {/* SRG selector */}
          {!audit && (
            <div className="space-y-2">
              <label className="text-small font-medium text-dark-gray">SRG (buscar por OT o VIN)</label>
              <div className="relative">
                <div className="flex gap-2">
                  <Input
                    placeholder="Ej: 202601739"
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    className="flex-1"
                  />
                  <Button variant="secondary" size="sm" type="button">
                    <Search size={14} />
                  </Button>
                </div>
                {filtered.length > 0 && (
                  <div className="absolute top-full mt-1 z-10 w-full rounded-md border border-light-gray bg-white shadow-card max-h-48 overflow-y-auto">
                    {filtered.map(s => (
                      <button
                        key={s.id} type="button"
                        className="flex w-full items-center gap-3 px-4 py-2.5 text-small hover:bg-off-white text-left"
                        onClick={() => selectSrg(s)}
                      >
                        <span className="font-mono font-medium text-black">{s.ot}</span>
                        <span className="text-mid-gray">{s.srg_type === "WARRANTY" ? "Garantía" : "Campaña"}</span>
                        <span className="text-mid-gray">{s.vin}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
              {selected && (
                <p className="text-small text-[#065F46]">
                  ✓ Seleccionado: OT {selected.ot} — {selected.srg_type === "WARRANTY" ? "Garantía" : "Campaña"}
                </p>
              )}
              {errors.srg_id && <p className="text-caption text-[#CC0000]">{errors.srg_id.message}</p>}
              <input type="hidden" {...register("srg_id")} />
            </div>
          )}

          {/* OT Factura + Observations */}
          <div className="grid gap-4 sm:grid-cols-2">
            <Input label="OT Factura" error={errors.ot_factura?.message} {...register("ot_factura")} />
          </div>
          <Textarea
            label="Observaciones"
            placeholder="OBSERVACIONES EN MAYÚSCULAS..."
            error={errors.observations?.message}
            {...register("observations")}
          />

          {/* Emails */}
          <div className="space-y-2">
            <label className="text-small font-medium text-dark-gray">Correos Adicionales</label>
            {emails.fields.map((f, i) => (
              <div key={f.id} className="flex gap-2">
                <Input
                  type="email"
                  placeholder="correo@ejemplo.com"
                  error={errors.additional_emails?.[i]?.email?.message}
                  className="flex-1"
                  {...register(`additional_emails.${i}.email`)}
                />
                <Button variant="ghost" size="sm" type="button" onClick={() => emails.remove(i)}>
                  <Trash2 size={14} />
                </Button>
              </div>
            ))}
            <Button variant="secondary" size="sm" type="button" onClick={() => emails.append({ email: "" })}>
              <Plus size={14} /> Agregar correo
            </Button>
          </div>

          {/* Attachments */}
          <div className="space-y-2">
            <label className="text-small font-medium text-dark-gray">Archivos de Soporte</label>
            {attachments.fields.map((f, i) => (
              <div key={f.id} className="flex gap-2">
                <Input placeholder="Nombre archivo" className="w-40" {...register(`attachments.${i}.file_name`)} />
                <Input placeholder="https://..." className="flex-1" {...register(`attachments.${i}.file_url`)} />
                <Button variant="ghost" size="sm" type="button" onClick={() => attachments.remove(i)}>
                  <Trash2 size={14} />
                </Button>
              </div>
            ))}
            <Button variant="secondary" size="sm" type="button"
              onClick={() => attachments.append({ file_name: "", file_url: "" })}>
              <Plus size={14} /> Agregar archivo
            </Button>
          </div>

          <Small color="tertiary">Las observaciones se almacenan en mayúsculas automáticamente.</Small>

          {(create.isError || update.isError) && (
            <p className="text-caption text-[#CC0000]">Error al guardar la auditoría.</p>
          )}

          <div className="flex justify-end gap-3">
            <Button variant="secondary" type="button" onClick={() => router.back()}>Cancelar</Button>
            <Button type="submit" loading={isPending}>{audit ? "Guardar Cambios" : "Crear Auditoría"}</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
