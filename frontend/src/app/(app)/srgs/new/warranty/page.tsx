import { WarrantyForm } from "@/modules/srg/WarrantyForm";
import { H3, Small } from "@/components/ui";

export default function NewWarrantyPage() {
  return (
    <div className="space-y-6">
      <div>
        <H3>Nueva Garantía</H3>
        <Small color="tertiary" className="mt-1">Ingresá la OT (alfanumérica, en mayúsculas).</Small>
      </div>
      <WarrantyForm />
    </div>
  );
}
