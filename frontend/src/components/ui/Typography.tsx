import { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

type TextColor = "primary" | "secondary" | "tertiary";

const colorStyles: Record<TextColor, string> = {
  primary:   "text-black",
  secondary: "text-dark-gray",
  tertiary:  "text-mid-gray",
};

interface TypoProps extends HTMLAttributes<HTMLElement> {
  color?: TextColor;
}

export function H1({ color = "primary", className, children, ...props }: TypoProps) {
  return (
    <h1 className={cn("text-h1 font-semibold leading-tight", colorStyles[color], className)} {...props}>
      {children}
    </h1>
  );
}

export function H2({ color = "primary", className, children, ...props }: TypoProps) {
  return (
    <h2 className={cn("text-h2 font-semibold leading-tight", colorStyles[color], className)} {...props}>
      {children}
    </h2>
  );
}

export function H3({ color = "primary", className, children, ...props }: TypoProps) {
  return (
    <h3 className={cn("text-h3 font-semibold", colorStyles[color], className)} {...props}>
      {children}
    </h3>
  );
}

export function H4({ color = "primary", className, children, ...props }: TypoProps) {
  return (
    <h4 className={cn("text-h4 font-medium", colorStyles[color], className)} {...props}>
      {children}
    </h4>
  );
}

export function BodyLg({ color = "secondary", className, children, ...props }: TypoProps) {
  return (
    <p className={cn("text-body-lg", colorStyles[color], className)} {...props}>
      {children}
    </p>
  );
}

export function Body({ color = "secondary", className, children, ...props }: TypoProps) {
  return (
    <p className={cn("text-body", colorStyles[color], className)} {...props}>
      {children}
    </p>
  );
}

export function Small({ color = "tertiary", className, children, ...props }: TypoProps) {
  return (
    <p className={cn("text-small", colorStyles[color], className)} {...props}>
      {children}
    </p>
  );
}

export function Caption({ color = "tertiary", className, children, ...props }: TypoProps) {
  return (
    <p className={cn("text-caption", colorStyles[color], className)} {...props}>
      {children}
    </p>
  );
}
