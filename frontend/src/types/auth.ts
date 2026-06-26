export type UserRole =
  | "SUPER_ADMIN"
  | "JEFE_TALLER"
  | "ASESOR"
  | "BODEGUERO"
  | "AUDITOR";

export type Concesionaria = "SURMOTOR" | "GRANDA_CENTENO" | "SHYRIS";

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: UserRole;
  concesionaria: Concesionaria | "";
  is_active: boolean;
}

export const ROLE_LABELS: Record<UserRole, string> = {
  SUPER_ADMIN:  "Super Admin",
  JEFE_TALLER:  "Jefe de Taller",
  ASESOR:       "Asesor",
  BODEGUERO:    "Bodeguero",
  AUDITOR:      "Auditor",
};

export const CONCESIONARIA_LABELS: Record<Concesionaria, string> = {
  SURMOTOR:       "Surmotor",
  GRANDA_CENTENO: "Granda Centeno",
  SHYRIS:         "Shyris",
};

export const CONCESIONARIA_OPTIONS = (Object.keys(CONCESIONARIA_LABELS) as Concesionaria[])
  .map(value => ({ value, label: CONCESIONARIA_LABELS[value] }));
