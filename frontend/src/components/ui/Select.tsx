import { forwardRef, SelectHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  hint?: string;
  options: { value: string; label: string }[];
  placeholder?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, hint, options, placeholder, className, id, ...props }, ref) => {
    const selectId = id ?? label?.toLowerCase().replace(/\s+/g, "-");

    return (
      <div className="flex flex-col gap-[6px]">
        {label && (
          <label htmlFor={selectId} className="text-small font-medium text-dark-gray">
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={selectId}
          className={cn(
            "h-12 w-full rounded-md border border-light-gray bg-white px-3",
            "text-body text-black appearance-none cursor-pointer",
            "transition-colors duration-150",
            "focus:outline-none focus:border-black",
            "disabled:cursor-not-allowed disabled:bg-off-white disabled:opacity-60",
            error && "border-[#CC0000] focus:border-[#CC0000]",
            className
          )}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="text-caption text-[#CC0000]">{error}</p>}
        {hint && !error && <p className="text-caption text-mid-gray">{hint}</p>}
      </div>
    );
  }
);

Select.displayName = "Select";
