"use client";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input, Select, Button, Card, CardContent, H4, Small } from "@/components/ui";
import { useCreateCampaignSrg, useCatalogParams } from "@/hooks/useSrgs";
import { useAuthStore } from "@/store/auth";
import { CONCESIONARIA_OPTIONS } from "@/types/auth";

const schema = z.object({
  ot:             z.string().min(1, "OT requerida").max(20, "Máximo 20 caracteres").regex(/^[A-Z0-9]+$/, "Solo mayúsculas y números"),
  vin:            z.string().length(17, "El VIN debe tener 17 caracteres"),
  placa:          z.string().min(1, "Placa requerida").max(10, "Máximo 10 caracteres"),
  vehicle_model:  z.string().min(1),
  vehicle_year:   z.coerce.number().min(2000).max(2100),
  km_apertura:    z.coerce.number().min(0),
  sede:           z.string().min(1, "Sede requerida"),
  campaign_code:  z.string().min(1),
});

type Form = z.infer<typeof schema>;

export function CampaignForm() {
  const router = useRouter();
  const { user } = useAuthStore();
  const create = useCreateCampaignSrg();

  const { data: models   = [] } = useCatalogParams("VEHICLE_MODEL",  user?.concesionaria);
  const { data: campaigns = [] } = useCatalogParams("CAMPAIGN_CODE",  user?.concesionaria);

  const { register, formState: { errors }, handleSubmit } = useForm<Form>({ resolver: zodResolver(schema) });

  const otField = register("ot");
  function sanitizeOt(e: React.ChangeEvent<HTMLInputElement>) {
    e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
    otField.onChange(e);
  }

  return (
    <Card>
      <CardContent>
        <form
          className="space-y-6"
          onSubmit={handleSubmit(d =>
            create.mutate(d, { onSuccess: srg => router.push(`/srgs/${srg.id}`) })
          )}
          noValidate
        >
          <H4>Datos de la Campaña</H4>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <Input
              label="OT"
              placeholder="Ej. OT2026C500"
              hint="Alfanumérica, en mayúsculas"
              error={errors.ot?.message}
              {...otField}
              onChange={sanitizeOt}
            />
            <Select
              label="Código de Campaña"
              options={[{ value: "", label: "Seleccionar..." }, ...campaigns.map(c => ({ value: c.code, label: c.name }))]}
              error={errors.campaign_code?.message}
              {...register("campaign_code")}
            />
            <Input label="VIN" maxLength={17} placeholder="17 caracteres" error={errors.vin?.message} {...register("vin")} />
            <Input label="Placa" maxLength={10} placeholder="Ej. PXA-1234" error={errors.placa?.message} {...register("placa")} />
            <Select
              label="Modelo"
              options={[{ value: "", label: "Seleccionar..." }, ...models.map(m => ({ value: m.code, label: m.name }))]}
              error={errors.vehicle_model?.message}
              {...register("vehicle_model")}
            />
            <Input label="Año"         type="number" placeholder="2026" error={errors.vehicle_year?.message}   {...register("vehicle_year")} />
            <Input label="Km Apertura" type="number" error={errors.km_apertura?.message}    {...register("km_apertura")} />
            <Select
              label="Sede"
              options={[{ value: "", label: "Seleccionar..." }, ...CONCESIONARIA_OPTIONS]}
              error={errors.sede?.message}
              {...register("sede")}
            />
          </div>

          <Small color="tertiary">La OT y los demás valores se almacenan en mayúsculas.</Small>

          {create.isError && <p className="text-caption text-[#CC0000]">Error al crear la campaña. Verificá los datos.</p>}

          <div className="flex justify-end gap-3">
            <Button variant="secondary" type="button" onClick={() => router.back()}>Cancelar</Button>
            <Button type="submit" loading={create.isPending}>Crear Campaña</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
