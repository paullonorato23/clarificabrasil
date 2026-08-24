import { faixaDePercentual } from "@/lib/score";

interface ScoreBadgeProps {
  score: number;
  grande?: boolean;
}

/** Selo do Score de Coerência (0–100) com cor por faixa: verde, amarelo ou vermelho. */
export default function ScoreBadge({ score, grande = false }: ScoreBadgeProps) {
  const faixa = faixaDePercentual(score);

  if (grande) {
    return (
      <div className={`inline-flex flex-col items-center rounded-xl px-6 py-4 ${faixa.fundo}`}>
        <span className={`font-data text-5xl font-extrabold ${faixa.texto}`}>{score}</span>
        <span className={`text-xs font-semibold uppercase tracking-wide ${faixa.texto}`}>
          Score de Coerência
        </span>
        <span className={`mt-1 text-xs ${faixa.texto}`}>{faixa.rotulo}</span>
      </div>
    );
  }

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold ${faixa.fundo} ${faixa.texto}`}
      title={`Score de Coerência: ${score}/100 (${faixa.rotulo})`}
    >
      <span className={`h-2 w-2 rounded-full ${faixa.barra}`} />
      {score}
    </span>
  );
}
