"use client";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input, Button, Small } from "@/components/ui";
import { useCampaignBody, useUpsertCampaignBody } from "@/hooks/useSrgs";
import { useAuthStore } from "@/store/auth";
import type { Srg } from "@/types/srg";

const schema = z.object({
  update_name: z.string().min(1),
  image_link:  z.string().url("Debe ser una URL válida"),
});

type Form = z.infer<typeof schema>;

export function CampaignBodyForm({ srg }: { srg: Srg }) {
  const { user } = useAuthStore();
  const { data: body } = useCampaignBody(srg.id);
  const upsert = useUpsertCampaignBody(srg.id);
  const canEdit = user?.role !== "BODEGUERO";

  const { register, handleSubmit, formState: { errors } } = useForm<Form>({
    resolver: zodResolver(schema),
    defaultValues: { update_name: body?.update_name ?? "", image_link: body?.image_link ?? "" },
  });

  if (!canEdit) return null;

  return (
    <div className="space-y-4">
      {body ? (
        <div className="rounded-md border border-light-gray p-4 space-y-2">
          <p className="text-small font-medium text-black">{body.update_name}</p>
          <a href={body.image_link} target="_blank" rel="noreferrer"
            className="text-small text-[#3730A3] underline break-all">
            {body.image_link}
          </a>
          <Small color="tertiary">Modificado por: {body.modified_by}</Small>
        </div>
      ) : (
        <Small color="tertiary">Sin cuerpo de campaña registrado.</Small>
      )}

      <form className="space-y-3" onSubmit={handleSubmit(d => upsert.mutate(d))}>
        <Input
          label="Nombre de la Actualización"
          placeholder="ACTUALIZACIÓN ECU V2.3 — SC250"
          error={errors.update_name?.message}
          {...register("update_name")}
        />
        <Input
          label="Link de Imagen de Evidencia"
          placeholder="https://..."
          error={errors.image_link?.message}
          {...register("image_link")}
        />
        <Button size="sm" type="submit" loading={upsert.isPending}>
          {body ? "Actualizar" : "Registrar"}
        </Button>
      </form>
    </div>
  );
}
