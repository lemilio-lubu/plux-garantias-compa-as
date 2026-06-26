import { forwardRef, TextareaHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, hint, className, id, ...props }, ref) => {
    const inputId = id ?? label?.toLowerCase().replace(/\s+/g, "-");

    return (
      <div className="flex flex-col gap-[6px]">
        {label && (
          <label htmlFor={inputId} className="text-small font-medium text-dark-gray">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={inputId}
          className={cn(
            "w-full rounded-md border border-light-gray bg-white px-3 py-3",
            "text-body text-black placeholder:text-mid-gray resize-y min-h-[96px]",
            "transition-colors duration-150",
            "focus:outline-none focus:border-black",
            "disabled:cursor-not-allowed disabled:bg-off-white disabled:opacity-60",
            error && "border-[#CC0000] focus:border-[#CC0000]",
            className
          )}
          {...props}
        />
        {error && <p className="text-caption text-[#CC0000]">{error}</p>}
        {hint && !error && <p className="text-caption text-mid-gray">{hint}</p>}
      </div>
    );
  }
);

Textarea.displayName = "Textarea";
