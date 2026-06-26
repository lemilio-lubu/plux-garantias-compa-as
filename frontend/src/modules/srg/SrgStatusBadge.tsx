import { Badge, srgStatusVariant } from "@/components/ui";
import { STATUS_LABELS, SRG_TYPE_LABELS, type SrgStatus, type SrgType } from "@/types/srg";

export function SrgStatusBadge({ status }: { status: SrgStatus }) {
  return (
    <Badge variant={srgStatusVariant(status)}>
      {STATUS_LABELS[status]}
    </Badge>
  );
}

export function SrgTypeBadge({ type }: { type: SrgType }) {
  return (
    <Badge variant="default" className="bg-[#F8F8F8] text-dark-gray">
      {SRG_TYPE_LABELS[type]}
    </Badge>
  );
}
