"use client";
import { usePathname } from "next/navigation";

const PAGE_TITLES: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/srgs":      "SRGs",
  "/catalog":   "Catálogo",
  "/audits":    "Auditorías",
  "/users":     "Usuarios",
};

function getTitle(pathname: string): string {
  // Exact match first
  if (PAGE_TITLES[pathname]) return PAGE_TITLES[pathname];
  // Prefix match
  for (const [path, title] of Object.entries(PAGE_TITLES)) {
    if (pathname.startsWith(path + "/")) return title;
  }
  return "";
}

interface HeaderProps {
  right?: React.ReactNode;
}

export function Header({ right }: HeaderProps) {
  const pathname = usePathname();
  const title = getTitle(pathname);

  return (
    <header className="flex h-[68px] items-center justify-between border-b border-mist bg-white/80 px-6 backdrop-blur">
      <div className="flex items-center gap-3">
        <span className="h-5 w-[3px] rounded-full bg-amber" aria-hidden />
        <h1 className="font-display text-h4 text-ink">{title}</h1>
      </div>
      {right && <div className="flex items-center gap-3">{right}</div>}
    </header>
  );
}
