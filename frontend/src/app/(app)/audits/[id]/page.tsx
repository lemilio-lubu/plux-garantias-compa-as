"use client";
import { use } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Paperclip, Mail } from "lucide-react";
import {
  Card, CardHeader, CardTitle, CardContent,
  PageSpinner, Small, Separator,
} from "@/components/ui";
import { useAudit } from "@/hooks/useAudits";

export default function AuditDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const { data: audit, isLoading } = useAudit(id);

  if (isLoading) return <PageSpinner />;
  if (!audit)    return <p className="text-small text-mid-gray">Auditoría no encontrada.</p>;

  return (
    <div className="space-y-6">
      <button onClick={() => router.back()}
        className="flex items-center gap-1.5 text-small text-mid-gray hover:text-dark-gray transition-colors">
        <ArrowLeft size={14} /> Volver
      </button>

      <Card>
        <CardHeader><CardTitle>Auditoría — OT Factura: {audit.ot_factura}</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-caption uppercase tracking-wide text-mid-gray">Observaciones</p>
            <p className="mt-1 text-small text-black whitespace-pre-wrap">{audit.observations}</p>
          </div>

          <Separator />

          {audit.additional_emails.length > 0 && (
            <div>
              <p className="mb-2 text-caption uppercase tracking-wide text-mid-gray flex items-center gap-1">
                <Mail size={12} /> Correos adicionales
              </p>
              <ul className="space-y-1">
                {audit.additional_emails.map(e => (
                  <li key={e} className="text-small text-dark-gray">{e}</li>
                ))}
              </ul>
            </div>
          )}

          {audit.attachments.length > 0 && (
            <div>
              <p className="mb-2 text-caption uppercase tracking-wide text-mid-gray flex items-center gap-1">
                <Paperclip size={12} /> Archivos de soporte
              </p>
              <ul className="space-y-1.5">
                {audit.attachments.map((a, i) => (
                  <li key={i} className="flex items-center gap-2 text-small">
                    <span className="text-dark-gray">{a.file_name}</span>
                    <a href={a.file_url} target="_blank" rel="noreferrer"
                      className="text-[#3730A3] underline break-all">{a.file_url}</a>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <Separator />
          <Small color="tertiary">
            Creado: {new Date(audit.created_at).toLocaleDateString("es-EC")}
            {" — "}Actualizado: {new Date(audit.updated_at).toLocaleDateString("es-EC")}
          </Small>
        </CardContent>
      </Card>
    </div>
  );
}
