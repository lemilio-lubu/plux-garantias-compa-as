import { AuditForm } from "@/modules/audit/AuditForm";
import { H3, Small } from "@/components/ui";

export default function NewAuditPage() {
  return (
    <div className="space-y-6">
      <div>
        <H3>Nueva Auditoría</H3>
        <Small color="tertiary" className="mt-1">Vinculá un SRG existente y registrá el checklist de cumplimiento.</Small>
      </div>
      <AuditForm />
    </div>
  );
}
