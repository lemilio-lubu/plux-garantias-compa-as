import { CampaignForm } from "@/modules/srg/CampaignForm";
import { H3, Small } from "@/components/ui";

export default function NewCampaignPage() {
  return (
    <div className="space-y-6">
      <div>
        <H3>Nueva Campaña</H3>
        <Small color="tertiary" className="mt-1">Ingresá la OT (alfanumérica, en mayúsculas).</Small>
      </div>
      <CampaignForm />
    </div>
  );
}
