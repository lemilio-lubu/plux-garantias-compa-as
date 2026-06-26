"use client";
import { useState } from "react";
import { Tabs, H3 } from "@/components/ui";
import { CatalogParamSection } from "@/modules/catalog/CatalogParamSection";
import { SparePartsTab } from "@/modules/catalog/SparePartsTab";
import { CATALOG_PARAM_LABELS, type CatalogParamType } from "@/types/catalog";

const PARAM_TYPES: CatalogParamType[] = ["VEHICLE_MODEL", "COLOR", "WARRANTY_TYPE", "CAMPAIGN_CODE"];

const MAIN_TABS = [
  { value: "params", label: "Parámetros" },
  { value: "parts",  label: "Repuestos"  },
];

const PARAM_TABS = PARAM_TYPES.map(t => ({ value: t, label: CATALOG_PARAM_LABELS[t] }));

export default function CatalogPage() {
  const [tab,       setTab]       = useState("params");
  const [paramType, setParamType] = useState<CatalogParamType>("VEHICLE_MODEL");

  return (
    <div className="space-y-6">
      <H3>Catálogo</H3>

      <Tabs tabs={MAIN_TABS} value={tab} onChange={setTab} />

      {tab === "params" && (
        <div className="space-y-4">
          <Tabs tabs={PARAM_TABS} value={paramType} onChange={v => setParamType(v as CatalogParamType)} />
          <div className="rounded-lg border border-light-gray bg-white p-6 shadow-card">
            <CatalogParamSection type={paramType} label={CATALOG_PARAM_LABELS[paramType]} />
          </div>
        </div>
      )}

      {tab === "parts" && (
        <div className="rounded-lg border border-light-gray bg-white p-6 shadow-card">
          <SparePartsTab />
        </div>
      )}
    </div>
  );
}
