import { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

type BadgeVariant =
  | "default"
  | "proceso"
  | "pendiente"
  | "preaprobado"
  | "aprobado"
  | "retornado"
  | "negado";

const variantStyles: Record<BadgeVariant, string> = {
  default:     "border-mist text-steel",
  proceso:     "border-status-proceso/30 text-status-proceso",
  pendiente:   "border-status-pendiente/30 text-status-pendiente",
  preaprobado: "border-status-preaprobado/30 text-status-preaprobado",
  aprobado:    "border-status-aprobado/40 text-status-aprobado",
  retornado:   "border-status-retornado/30 text-status-retornado",
  negado:      "border-mist text-status-negado",
};

const dotStyles: Record<BadgeVariant, string> = {
  default:     "bg-steel",
  proceso:     "bg-status-proceso",
  pendiente:   "bg-status-pendiente",
  preaprobado: "bg-status-preaprobado",
  aprobado:    "bg-status-aprobado",
  retornado:   "bg-status-retornado",
  negado:      "bg-status-negado",
};

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

export function Badge({ variant = "default", className, children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-sm border bg-white px-2 py-0.5",
        "font-mono text-[11px] font-medium uppercase tracking-[0.08em]",
        variantStyles[variant],
        className
      )}
      {...props}
    >
      <span className={cn("h-1.5 w-1.5 rounded-full", dotStyles[variant])} aria-hidden />
      {children}
    </span>
  );
}

/** Convierte un status de SRG en el variant de Badge correspondiente */
export function srgStatusVariant(status: string): BadgeVariant {
  const map: Record<string, BadgeVariant> = {
    PROCESO:     "proceso",
    PENDIENTE:   "pendiente",
    PREAPROBADO: "preaprobado",
    APROBADO:    "aprobado",
    RETORNADO:   "retornado",
    NEGADO:      "negado",
  };
  return map[status] ?? "default";
}
