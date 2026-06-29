"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth";
import { Button, Input } from "@/components/ui";
import type { User } from "@/types/auth";

const schema = z.object({
  email:    z.string().email("Email inválido"),
  password: z.string().min(1, "Contraseña requerida"),
});

type FormValues = z.infer<typeof schema>;

interface LoginResponse {
  access:  string;
  refresh: string;
}

// Demo accounts created by `python manage.py seed`. Shared password.
const DEMO_PASSWORD = "Plux2024!";
const DEMO_ACCOUNTS = [
  { role: "Super Admin",    email: "superadmin@plux.com" },
  { role: "Jefe de Taller", email: "jefe@plux.com" },
  { role: "Asesor",         email: "asesor@plux.com" },
  { role: "Bodeguero",      email: "bodeguero@plux.com" },
  { role: "Auditor",        email: "auditor@plux.com" },
];

export function LoginForm() {
  const router = useRouter();
  const { login } = useAuthStore();

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const mutation = useMutation({
    mutationFn: async (values: FormValues) => {
      const { data: tokens } = await api.post<LoginResponse>(
        "/auth/login/",
        values
      );
      const { data: user } = await api.get<User>("/users/me/", {
        headers: { Authorization: `Bearer ${tokens.access}` },
      });
      return { tokens, user };
    },
    onSuccess({ tokens, user }) {
      login({ access: tokens.access, refresh: tokens.refresh }, user);
      router.replace("/dashboard");
    },
  });

  function fillAccount(email: string) {
    setValue("email", email, { shouldValidate: true });
    setValue("password", DEMO_PASSWORD, { shouldValidate: true });
  }

  return (
    <div className="w-full max-w-[420px]">
      <div className="mb-8">
        <p className="eyebrow text-amber-dark">Acceso al panel</p>
        <h1 className="mt-2 font-display text-h2 text-ink">Iniciar sesión</h1>
        <p className="mt-1 text-small text-steel">
          Ingresá con tu cuenta de la concesionaria.
        </p>
      </div>

      <form
        onSubmit={handleSubmit((v) => mutation.mutate(v))}
        className="space-y-4"
        noValidate
      >
        <Input
          label="Correo electrónico"
          type="email"
          placeholder="usuario@concesionaria.com"
          error={errors.email?.message}
          autoComplete="email"
          {...register("email")}
        />

        <Input
          label="Contraseña"
          type="password"
          placeholder="••••••••"
          error={errors.password?.message}
          autoComplete="current-password"
          {...register("password")}
        />

        {mutation.isError && (
          <p className="rounded-md border border-status-retornado/30 bg-[#FBEEF0] px-3 py-2 text-small font-medium text-status-retornado">
            Credenciales incorrectas. Verificá e intentá de nuevo.
          </p>
        )}

        <Button type="submit" className="w-full" loading={mutation.isPending}>
          Ingresar
        </Button>
      </form>

      {/* Demo accounts — one click fills the form */}
      {process.env.NEXT_PUBLIC_ENABLE_DEMO_ACCOUNTS === "true" && (
        <div className="mt-8 rounded-lg border border-mist bg-white p-4">
          <p className="eyebrow text-steel">Cuentas de prueba</p>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {DEMO_ACCOUNTS.map((acc) => (
              <button
                key={acc.email}
                type="button"
                onClick={() => fillAccount(acc.email)}
                className="rounded-sm border border-mist px-2.5 py-1 text-caption font-medium text-steel transition-colors hover:border-amber hover:bg-amber-soft hover:text-ink"
              >
                {acc.role}
              </button>
            ))}
          </div>
          <p className="mt-3 font-mono text-caption text-steel">
            Contraseña: <span className="text-ink">{DEMO_PASSWORD}</span>
          </p>
        </div>
      )}
    </div>
  );
}
