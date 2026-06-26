"use client";
import { H3 } from "@/components/ui";
import { SparePartsTab } from "@/modules/catalog/SparePartsTab";

export default function RepuestosPage() {
  return (
    <div className="space-y-6">
      <div>
        <H3>Repuestos</H3>
        <p className="mt-0.5 text-small text-mid-gray">
          Gestión de repuestos de tu sede.
        </p>
      </div>

      <div className="rounded-lg border border-light-gray bg-white p-6 shadow-card">
        <SparePartsTab />
      </div>
    </div>
  );
}
