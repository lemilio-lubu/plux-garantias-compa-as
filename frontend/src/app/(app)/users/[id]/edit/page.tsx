"use client";
import { use } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { UserForm } from "@/modules/users/UserForm";
import { H3, Small, PageSpinner } from "@/components/ui";
import { useUser } from "@/hooks/useUsers";

export default function EditUserPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const { data: user, isLoading } = useUser(id);

  if (isLoading) return <PageSpinner />;
  if (!user) return <p className="text-small text-mid-gray p-6">Usuario no encontrado.</p>;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <button
          onClick={() => router.back()}
          className="flex items-center gap-1.5 text-small text-mid-gray hover:text-dark-gray transition-colors"
        >
          <ArrowLeft size={14} /> Volver
        </button>
      </div>
      <div>
        <H3>Editar Usuario</H3>
        <Small color="tertiary" className="mt-1">
          Modificá los datos del usuario. El correo y la contraseña no se pueden cambiar por seguridad.
        </Small>
      </div>
      <UserForm user={user} />
    </div>
  );
}
