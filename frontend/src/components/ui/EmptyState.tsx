import { type LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export function EmptyState({ icon: Icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center py-16 text-center", className)}>
      {Icon && (
        <div className="mb-4 rounded-lg bg-off-white p-4">
          <Icon size={24} className="text-mid-gray" />
        </div>
      )}
      <p className="text-body font-medium text-dark-gray">{title}</p>
      {description && <p className="mt-1 text-small text-mid-gray">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
