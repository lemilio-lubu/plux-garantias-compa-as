"use client";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input, Select, Button, Card, CardContent, H4, Small } from "@/components/ui";
import { useCreateWarrantySrg, useCatalogParams } from "@/hooks/useSrgs";
import { useAuthStore } from "@/store/auth";
import { CONCESIONARIA_OPTIONS } from "@/types/auth";

const schema = z.object({
  ot:                z.string().min(1, "OT requerida").max(20, "Máximo 20 caracteres").regex(/^[A-Z0-9]+$/, "Solo mayúsculas y números"),
  vin:               z.string().length(17, "El VIN debe tener 17 caracteres"),
  vehicle_model:     z.string().min(1),
  vehicle_color:     z.string().min(1),
  vehicle_year:      z.coerce.number().min(2000).max(2100),
  km_apertura:       z.coerce.number().min(0),
  sede:              z.string().min(1, "Sede requerida"),
  nro_garantia:      z.string().min(1),
  warranty_type_code:z.string().min(1),
  warranty_type_name:z.string().min(1),
});

type Form = z.infer<typeof schema>;

export function WarrantyForm() {
  const router = useRouter();
  const { user } = useAuthStore();
  const create = useCreateWarrantySrg();

  const { data: models  = [] } = useCatalogParams("VEHICLE_MODEL",  user?.concesionaria);
  const { data: colors  = [] } = useCatalogParams("COLOR",           user?.concesionaria);
  const { data: wtypes  = [] } = useCatalogParams("WARRANTY_TYPE",   user?.concesionaria);

  const { register, handleSubmit, setValue, watch, formState: { errors } } = useForm<Form>({
    resolver: zodResolver(schema),
  });

  const wtCode = watch("warranty_type_code");
  const otField = register("ot");

  function sanitizeOt(e: React.ChangeEvent<HTMLInputElement>) {
    e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
    otField.onChange(e);
  }

  function onSelectWarrantyType(code: string) {
    const found = wtypes.find(t => t.code === code);
    setValue("warranty_type_code", code);
    setValue("warranty_type_name", found?.name ?? "");
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
          {/* Datos Generales */}
          <div>
            <H4 className="mb-4">Datos Generales</H4>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <Input
                label="OT"
                placeholder="Ej. OT2026A001"
                hint="Alfanumérica, en mayúsculas"
                error={errors.ot?.message}
                {...otField}
                onChange={sanitizeOt}
              />
              <Input label="Nro. Garantía" error={errors.nro_garantia?.message} {...register("nro_garantia")} />
              <Select
                label="Tipo Garantía"
                options={[{ value: "", label: "Seleccionar..." }, ...wtypes.map(t => ({ value: t.code, label: t.name }))]}
                error={errors.warranty_type_code?.message}
                onChange={e => onSelectWarrantyType(e.target.value)}
                value={wtCode ?? ""}
              />
              <Input label="VIN" maxLength={17} placeholder="17 caracteres" error={errors.vin?.message} {...register("vin")} />
              <Select
                label="Modelo"
                options={[{ value: "", label: "Seleccionar..." }, ...models.map(m => ({ value: m.code, label: m.name }))]}
                error={errors.vehicle_model?.message}
                {...register("vehicle_model")}
              />
              <Select
                label="Color"
                options={[{ value: "", label: "Seleccionar..." }, ...colors.map(c => ({ value: c.code, label: c.name }))]}
                error={errors.vehicle_color?.message}
                {...register("vehicle_color")}
              />
              <Input label="Año" type="number" placeholder="2026" error={errors.vehicle_year?.message} {...register("vehicle_year")} />
              <Input label="Km Apertura" type="number" error={errors.km_apertura?.message} {...register("km_apertura")} />
              <Select
                label="Sede"
                options={[{ value: "", label: "Seleccionar..." }, ...CONCESIONARIA_OPTIONS]}
                error={errors.sede?.message}
                {...register("sede")}
              />
            </div>
          </div>

          <Small color="tertiary">Todos los valores se almacenan en mayúsculas automáticamente.</Small>

          {create.isError && <p className="text-caption text-[#CC0000]">Error al crear el SRG. Verificá los datos.</p>}

          <div className="flex justify-end gap-3">
            <Button variant="secondary" type="button" onClick={() => router.back()}>Cancelar</Button>
            <Button type="submit" loading={create.isPending}>Crear Garantía</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
