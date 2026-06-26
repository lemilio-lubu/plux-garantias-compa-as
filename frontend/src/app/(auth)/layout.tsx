export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid min-h-screen lg:grid-cols-[1.05fr_1fr]">
      {/* Brand panel — the service-bay console identity */}
      <aside className="relative hidden flex-col justify-between overflow-hidden bg-ink p-12 text-white lg:flex">
        <div className="hazard-strip absolute inset-x-0 top-0 h-1.5 opacity-90" />

        <div className="flex items-center gap-2.5">
          <span className="h-3 w-3 rounded-full bg-amber shadow-[0_0_12px_rgba(245,179,1,0.7)]" />
          <span className="font-display text-2xl font-bold tracking-tight">Plux</span>
        </div>

        <div className="max-w-md">
          <p className="eyebrow text-amber/80">Garantías &amp; Campañas de Recall</p>
          <h2 className="mt-4 font-display text-[40px] font-semibold leading-[1.08] tracking-tight">
            El taller, bajo
            <br />
            control total.
          </h2>
          <p className="mt-5 text-body leading-relaxed text-white/60">
            Trazá cada solicitud de garantía y campaña desde la apertura de la
            OT hasta la aprobación, con checklist por rol y registro de auditoría.
          </p>

          {/* Status flow — a real sequence, shown as stations */}
          <div className="mt-9 flex items-center gap-2">
            {["Proceso", "Pendiente", "Preaprob.", "Aprobado"].map((step, i) => (
              <div key={step} className="flex items-center gap-2">
                <div className="flex flex-col items-center gap-1.5">
                  <span
                    className={
                      "h-2.5 w-2.5 rounded-full " +
                      (i === 3 ? "bg-amber shadow-[0_0_8px_rgba(245,179,1,0.7)]" : "bg-white/25")
                    }
                  />
                  <span className="eyebrow text-[9px] text-white/40">{step}</span>
                </div>
                {i < 3 && <span className="mb-4 h-px w-6 bg-white/15" />}
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-6 eyebrow text-white/30">
          <span>Surmotor</span>
          <span>Granda Centeno</span>
          <span>Shyris</span>
        </div>
      </aside>

      {/* Form area */}
      <main className="flex items-center justify-center bg-paper px-6 py-12">
        {children}
      </main>
    </div>
  );
}
