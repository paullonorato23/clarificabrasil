import type { GastoCategoria } from "@/lib/types";
import { formatarMoeda } from "@/lib/format";

/** Gráfico de barras horizontais em CSS puro para os gastos por categoria. */
export default function GastosChart({ gastos }: { gastos: GastoCategoria[] }) {
  const maior = Math.max(...gastos.map((g) => g.valor), 1);
  const ordenados = [...gastos].sort((a, b) => b.valor - a.valor);

  return (
    <div className="space-y-3">
      {ordenados.map((gasto) => (
        <div key={gasto.categoria}>
          <div className="mb-1 flex items-baseline justify-between gap-4 text-sm">
            <span className="text-neutral-700">{gasto.categoria}</span>
            <span className="font-data font-semibold whitespace-nowrap text-neutral-900">
              {formatarMoeda(gasto.valor)}
            </span>
          </div>
          <div className="h-3 overflow-hidden rounded-full bg-neutral-200">
            <div
              className="h-full rounded-full bg-primary-600"
              style={{ width: `${Math.round((gasto.valor / maior) * 100)}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
