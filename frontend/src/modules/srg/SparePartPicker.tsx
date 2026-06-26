"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { useSpareParts } from "@/hooks/useCatalog";
import type { SparePart } from "@/types/catalog";

interface Props {
  /** Currently selected catalog code, to keep the field in sync with the form. */
  value?: string;
  onSelect: (part: SparePart) => void;
  error?: string;
}

/**
 * Searchable spare-part picker. The asesor types a code (or name) and selects
 * from the dealership catalog; the parent form autofills name and unit price.
 */
export function SparePartPicker({ value, onSelect, error }: Props) {
  const { data: parts = [], isLoading } = useSpareParts();
  const [query, setQuery] = useState(value ?? "");
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Keep the visible text in sync when the form resets the selection.
  useEffect(() => {
    if (!value) setQuery("");
  }, [value]);

  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, []);

  const matches = useMemo(() => {
    const q = query.trim().toLowerCase();
    const list = q
      ? parts.filter(
          (p) =>
            p.catalog_code.toLowerCase().includes(q) ||
            p.name.toLowerCase().includes(q),
        )
      : parts;
    return list.slice(0, 8);
  }, [parts, query]);

  function pick(part: SparePart) {
    onSelect(part);
    setQuery(part.catalog_code);
    setOpen(false);
  }

  return (
    <div className="flex flex-col gap-[6px]" ref={ref}>
      <label className="eyebrow text-steel">Repuesto (código)</label>
      <div className="relative">
        <Search
          size={15}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-steel/70"
        />
        <input
          className={cn(
            "h-11 w-full rounded-md border border-mist bg-white pl-9 pr-3",
            "text-body text-ink placeholder:text-steel/70 transition-colors duration-150",
            "focus:outline-none focus:border-amber focus:ring-2 focus:ring-amber/25",
            error &&
              "border-status-retornado focus:border-status-retornado focus:ring-status-retornado/20",
          )}
          placeholder={isLoading ? "Cargando catálogo..." : "Buscar por código o nombre..."}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
        />

        {open && (
          <ul className="absolute z-20 mt-1 max-h-60 w-full overflow-auto rounded-md border border-mist bg-white py-1 shadow-card">
            {matches.length === 0 ? (
              <li className="px-3 py-2 text-small text-steel">Sin coincidencias</li>
            ) : (
              matches.map((p) => (
                <li key={p.id}>
                  <button
                    type="button"
                    onClick={() => pick(p)}
                    className="flex w-full items-center justify-between gap-3 px-3 py-2 text-left text-small hover:bg-paper"
                  >
                    <span className="min-w-0 truncate">
                      <span className="font-mono font-medium text-ink">{p.catalog_code}</span>{" "}
                      <span className="text-steel">{p.name}</span>
                    </span>
                    <span className="shrink-0 font-mono text-steel">${p.unit_price}</span>
                  </button>
                </li>
              ))
            )}
          </ul>
        )}
      </div>
      {error && <p className="text-caption font-medium text-status-retornado">{error}</p>}
    </div>
  );
}
