"use client";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input, Select, Button, Card, CardContent, Separator } from "@/components/ui";
import { useCreateUser, useUpdateUser } from "@/hooks/useUsers";
import { ROLE_LABELS, type User } from "@/types/auth";

const createSchema = z.object({
  email:        z.string().email(),
  first_name:   z.string().min(1),
  last_name:    z.string().min(1),
  role:         z.string().min(1),
  concesionaria:z.string().min(1),
  password:     z.string().min(8, "Mínimo 8 caracteres"),
});

const editSchema = createSchema.omit({ password: true, email: true }).extend({
  is_active: z.boolean().optional(),
});

type CreateForm = z.infer<typeof createSchema>;
type EditForm   = z.infer<typeof editSchema>;

const ROLE_OPTIONS = Object.entries(ROLE_LABELS).map(([v, l]) => ({ value: v, label: l }));
const CONC_OPTIONS = [
  { value: "SURMOTOR",       label: "Surmotor" },
  { value: "GRANDA_CENTENO", label: "Granda Centeno" },
  { value: "SHYRIS",         label: "Shyris" },
];

interface Props { user?: User; }

export function UserForm({ user }: Props) {
  const router  = useRouter();
  const create  = useCreateUser();
  const update  = useUpdateUser(user?.id ?? "");

  const isEdit = !!user;

  const { register, handleSubmit, formState: { errors } } = useForm<CreateForm | EditForm>({
    resolver: zodResolver(isEdit ? editSchema : createSchema) as never,
    defaultValues: isEdit ? {
      first_name:    user.first_name,
      last_name:     user.last_name,
      role:          user.role,
      concesionaria: user.concesionaria,
    } : {},
  });

  function onSubmit(data: CreateForm | EditForm) {
    if (isEdit) {
      update.mutate(data, { onSuccess: () => router.back() });
    } else {
      create.mutate(data, { onSuccess: () => router.push("/users") });
    }
  }

  return (
    <Card>
      <CardContent>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit as never)} noValidate>
          <div className="grid gap-4 sm:grid-cols-2">
            <Input label="Nombre"   error={(errors as never as Record<string, { message: string }>).first_name?.message} {...register("first_name")} />
            <Input label="Apellido" error={(errors as never as Record<string, { message: string }>).last_name?.message}  {...register("last_name")} />
          </div>

          {!isEdit && (
            <Input
              label="Correo electrónico"
              type="email"
              error={(errors as never as Record<string, { message: string }>).email?.message}
              {...register("email" as never)}
            />
          )}

          <div className="grid gap-4 sm:grid-cols-2">
            <Select
              label="Rol"
              options={[{ value: "", label: "Seleccionar..." }, ...ROLE_OPTIONS]}
              error={(errors as never as Record<string, { message: string }>).role?.message}
              {...register("role")}
            />
            <Select
              label="Concesionaria"
              options={[{ value: "", label: "Seleccionar..." }, ...CONC_OPTIONS]}
              error={(errors as never as Record<string, { message: string }>).concesionaria?.message}
              {...register("concesionaria")}
            />
          </div>

          {!isEdit && (
            <>
              <Separator />
              <Input
                label="Contraseña"
                type="password"
                error={(errors as never as Record<string, { message: string }>).password?.message}
                {...register("password" as never)}
              />
            </>
          )}

          {(create.isError || update.isError) && (
            <p className="text-caption text-[#CC0000]">Error al guardar el usuario.</p>
          )}

          <div className="flex justify-end gap-3">
            <Button variant="secondary" type="button" onClick={() => router.back()}>Cancelar</Button>
            <Button type="submit" loading={create.isPending || update.isPending}>
              {isEdit ? "Guardar Cambios" : "Crear Usuario"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
