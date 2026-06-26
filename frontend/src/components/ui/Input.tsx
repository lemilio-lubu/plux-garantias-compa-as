import { forwardRef, InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, className, id, ...props }, ref) => {
    const inputId = id ?? label?.toLowerCase().replace(/\s+/g, "-");

    return (
      <div className="flex flex-col gap-[6px]">
        {label && (
          <label
            htmlFor={inputId}
            className="eyebrow text-steel"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            // Base
            "h-11 w-full rounded-md border border-mist bg-white px-3",
            "text-body text-ink placeholder:text-steel/70",
            "transition-colors duration-150",
            // Focus — brand amber ring
            "focus:outline-none focus:border-amber focus:ring-2 focus:ring-amber/25",
            // Disabled
            "disabled:cursor-not-allowed disabled:bg-paper disabled:opacity-60",
            // Error
            error && "border-status-retornado focus:border-status-retornado focus:ring-status-retornado/20",
            className
          )}
          {...props}
        />
        {error && (
          <p className="text-caption font-medium text-status-retornado">{error}</p>
        )}
        {hint && !error && (
          <p className="text-caption text-steel">{hint}</p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";
