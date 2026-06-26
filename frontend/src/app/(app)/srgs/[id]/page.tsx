"use client";
import { use } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Trash2 } from "lucide-react";
import {
  Button, Card, CardContent, CardHeader, CardTitle,
  PageSpinner, Small,
} from "@/components/ui";
import { SrgStatusBadge, SrgTypeBadge } from "@/modules/srg/SrgStatusBadge";
import { SrgStatusTrack } from "@/modules/srg/SrgStatusTrack";
import { SrgStatusFlow } from "@/modules/srg/SrgStatusFlow";
import { SrgChecklist } from "@/modules/srg/SrgChecklist";
import { SrgTimeline } from "@/modules/srg/SrgTimeline";
import { CampaignBodyForm } from "@/modules/srg/CampaignBodyForm";
import { useSrg, useDeleteSrg } from "@/hooks/useSrgs";
import { useAuthStore } from "@/store/auth";

function Field({ label, value }: { label: string; value?: string | number | null }) {
  return (
    <div>
      <p className="text-caption text-mid-gray uppercase tracking-wide">{label}</p>
      <p className="mt-0.5 text-small font-medium text-black">{value ?? "—"}</p>
    </div>
  );
}

export default function SrgDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router  = useRouter();
  const { user } = useAuthStore();
  const { data: srg, isLoading } = useSrg(id);
  const deleteMut = useDeleteSrg();

  if (isLoading) return <PageSpinner />;
  if (!srg) return <p className="text-small text-mid-gray">SRG no encontrado.</p>;

  const canDelete = user?.role === "JEFE_TALLER" || user?.role === "SUPER_ADMIN";

  return (
    <div className="space-y-6">
      {/* Top bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => router.back()}
          className="flex items-center gap-1.5 text-small text-mid-gray hover:text-dark-gray transition-colors"
        >
          <ArrowLeft size={14} /> Volver
        </button>
        {canDelete && (
          <Button
            variant="destructive"
            size="sm"
            loading={deleteMut.isPending}
            onClick={() => deleteMut.mutate(srg.id, { onSuccess: () => router.push("/srgs") })}
          >
            <Trash2 size={14} /> Dar de Baja
          </Button>
        )}
      </div>

      {/* Header card */}
      <Card>
        <CardContent>
          <div className="flex flex-wrap items-start gap-4 justify-between">
            <div className="space-y-1">
              <p className="text-caption text-mid-gray uppercase tracking-wide">OT</p>
              <h2 className="text-h3 font-semibold text-black font-mono">{srg.ot}</h2>
              <div className="flex gap-2 mt-1">
                <SrgTypeBadge   type={srg.srg_type} />
                <SrgStatusBadge status={srg.status} />
              </div>
            </div>
            <div className="text-right space-y-1">
              {srg.fecha_envio_marca && (
                <Small color="tertiary">
                  Enviado: {new Date(srg.fecha_envio_marca).toLocaleDateString("es-EC")}
                </Small>
              )}
              {srg.fecha_aprobacion && (
                <Small color="tertiary">
                  Aprobado: {new Date(srg.fecha_aprobacion).toLocaleDateString("es-EC")}
                </Small>
              )}
            </div>
          </div>

          {/* Status traceability track */}
          <div className="mt-6 border-t border-mist pt-5">
            <SrgStatusTrack srg={srg} />
          </div>

          {/* Status transitions */}
          <div className="mt-5">
            <SrgStatusFlow srg={srg} />
          </div>
        </CardContent>
      </Card>

      {/* General data */}
      <Card>
        <CardHeader><CardTitle>Datos del Vehículo</CardTitle></CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            <Field label="VIN"           value={srg.vin} />
            <Field label="Modelo"        value={srg.vehicle_model} />
            {srg.srg_type === "WARRANTY" && <Field label="Color" value={srg.vehicle_color} />}
            <Field label="Año"           value={srg.vehicle_year} />
            <Field label="Km Apertura"   value={srg.km_apertura} />
            <Field label="Sede"          value={srg.sede} />
          </div>
        </CardContent>
      </Card>

      {/* Warranty-specific */}
      {srg.srg_type === "WARRANTY" && (
        <Card>
          <CardHeader><CardTitle>Garantía</CardTitle></CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
              <Field label="Nro. Garantía"    value={srg.nro_garantia} />
              <Field label="Tipo"              value={srg.warranty_type_name} />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Campaign-specific */}
      {srg.srg_type === "CAMPAIGN" && (
        <Card>
          <CardHeader><CardTitle>Campaña</CardTitle></CardHeader>
          <CardContent>
            <Field label="Código de Campaña" value={srg.campaign_code} />
          </CardContent>
        </Card>
      )}

      {/* Warranty parts ledger — reception / work / returns, available from creation */}
      {srg.srg_type === "WARRANTY" && (
        <Card>
          <CardHeader><CardTitle>Repuestos y recepción</CardTitle></CardHeader>
          <CardContent>
            <SrgChecklist srg={srg} />
          </CardContent>
        </Card>
      )}

      {/* Campaign body — only when APROBADO */}
      {srg.srg_type === "CAMPAIGN" && srg.status === "APROBADO" && (
        <Card>
          <CardHeader><CardTitle>Cuerpo de Campaña</CardTitle></CardHeader>
          <CardContent>
            <CampaignBodyForm srg={srg} />
          </CardContent>
        </Card>
      )}

      {/* Traceability timeline */}
      <Card>
        <CardHeader><CardTitle>Trazabilidad</CardTitle></CardHeader>
        <CardContent><SrgTimeline srgId={srg.id} /></CardContent>
      </Card>
    </div>
  );
}
