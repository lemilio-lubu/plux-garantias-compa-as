import { UserForm } from "@/modules/users/UserForm";
import { H3, Small } from "@/components/ui";

export default function NewUserPage() {
  return (
    <div className="space-y-6">
      <div>
        <H3>Nuevo Usuario</H3>
        <Small color="tertiary" className="mt-1">El usuario recibirá acceso según el rol asignado.</Small>
      </div>
      <UserForm />
    </div>
  );
}
