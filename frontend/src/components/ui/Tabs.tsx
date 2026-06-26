import { cn } from "@/lib/utils";

export interface Tab { value: string; label: string; }

interface TabsProps {
  tabs:     Tab[];
  value:    string;
  onChange: (v: string) => void;
  className?: string;
}

export function Tabs({ tabs, value, onChange, className }: TabsProps) {
  return (
    <div className={cn("flex gap-1 rounded-md border border-light-gray bg-off-white p-1 w-fit", className)}>
      {tabs.map(tab => (
        <button
          key={tab.value}
          type="button"
          onClick={() => onChange(tab.value)}
          className={cn(
            "rounded px-4 py-1.5 text-small font-medium transition-colors",
            value === tab.value
              ? "bg-white text-black shadow-sm"
              : "text-mid-gray hover:text-dark-gray"
          )}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
