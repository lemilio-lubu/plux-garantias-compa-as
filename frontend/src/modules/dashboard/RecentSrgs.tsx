"use client";
import { useRouter } from "next/navigation";
import {
  Table, TableHead, TableBody, TableRow, TableHeader, TableCell,
  EmptyState, PageSpinner,
} from "@/components/ui";
import { SrgStatusBadge, SrgTypeBadge } from "@/modules/srg/SrgStatusBadge";
import { useSrgs } from "@/hooks/useSrgs";
import { FileText } from "lucide-react";

export function RecentSrgs() {
  const router = useRouter();
  const { data = [], isLoading } = useSrgs();

  const recent = [...data]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 8);

  if (isLoading) return <PageSpinner />;

  if (recent.length === 0)
    return <EmptyState icon={FileText} title="Sin SRGs registrados" className="py-8" />;

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableHeader>OT</TableHeader>
          <TableHeader>Tipo</TableHeader>
          <TableHeader>Estado</TableHeader>
          <TableHeader>VIN</TableHeader>
          <TableHeader>Modelo</TableHeader>
          <TableHeader>Fecha</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {recent.map(srg => (
          <TableRow key={srg.id} onClick={() => router.push(`/srgs/${srg.id}`)}>
            <TableCell className="font-mono font-medium text-black">{srg.ot}</TableCell>
            <TableCell><SrgTypeBadge   type={srg.srg_type} /></TableCell>
            <TableCell><SrgStatusBadge status={srg.status} /></TableCell>
            <TableCell className="font-mono text-mid-gray">{srg.vin}</TableCell>
            <TableCell>{srg.vehicle_model}</TableCell>
            <TableCell className="text-mid-gray">
              {new Date(srg.created_at).toLocaleDateString("es-EC")}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
