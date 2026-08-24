import type { StatusPromessa } from "@/lib/types";
import { ROTULOS_STATUS } from "@/lib/format";

const ESTILOS: Record<StatusPromessa, { simbolo: string; classes: string }> = {
  cumprida: { simbolo: "✓", classes: "bg-success-100 text-success-700" },
  em_andamento: { simbolo: "◔", classes: "bg-warning-100 text-warning-700" },
  contraditada: { simbolo: "✗", classes: "bg-danger-100 text-danger-700" },
  sem_acao: { simbolo: "—", classes: "bg-neutral-100 text-neutral-700" },
};

export default function StatusPromessaBadge({ status }: { status: StatusPromessa }) {
  const estilo = ESTILOS[status];
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold ${estilo.classes}`}
    >
      <span aria-hidden>{estilo.simbolo}</span>
      {ROTULOS_STATUS[status]}
    </span>
  );
}
